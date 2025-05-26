import json
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

# .env dosyasından Supabase bağlantı bilgilerini yükle
load_dotenv()

def veritabanina_baglan():
    # Supabase bağlantısı için gerekli yapılandırma
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        sslmode='require'  # Supabase için SSL zorunlu
    )

def gun_id_getir(cursor, gun, ay):
    cursor.execute(
        "SELECT id FROM gun WHERE gun = %s AND ay = %s",
        (gun, ay)
    )
    return cursor.fetchone()[0]

def yil_ve_icerik_ayir(metin):
    parcalar = metin.split(" - ", 1)
    if len(parcalar) == 2:
        try:
            yil = int(parcalar[0])
            icerik = parcalar[1]
            return yil, icerik
        except ValueError:
            return None, metin
    return None, metin

def verileri_toplu_ekle(cursor, tablo_adi, veriler):
    if not veriler:  # Boş veri listesi kontrolü
        return
        
    # Sütun isimleri
    if tablo_adi == 'tatil':
        sutunlar = ['gun_id', 'gun', 'ay', 'icerik']
    else:
        sutunlar = ['gun_id', 'gun', 'ay', 'yil', 'icerik']
    
    # Supabase için insert sorgusunu oluştur
    insert_query = f"INSERT INTO {tablo_adi} ({','.join(sutunlar)}) VALUES %s"
    
    try:
        # Toplu insert işlemi - Supabase'e veri aktarımı
        execute_values(cursor, insert_query, veriler, page_size=1000)
        print(f"{tablo_adi} tablosuna {len(veriler)} satır veri Supabase'e eklendi")
    except psycopg2.Error as e:
        print(f"Supabase'e veri eklenirken hata oluştu: {e}")
        raise

def json_verileri_aktar():
    conn = None
    try:
        # Supabase'e bağlan
        conn = veritabanina_baglan()
        cursor = conn.cursor()

        with open('turkce_tum_gunler.json', 'r', encoding='utf-8') as f:
            veriler = json.load(f)

        # Her tablo için verileri topla
        olay_verileri = []
        dogum_verileri = []
        olum_verileri = []
        tatil_verileri = []

        # Verileri hazırla
        for gun_verisi in veriler:
            gun, ay = map(int, gun_verisi['tarih'].split('-'))
            gun_id = gun_id_getir(cursor, gun, ay)

            # Olaylar
            for olay in gun_verisi['olaylar']:
                yil, icerik = yil_ve_icerik_ayir(olay)
                olay_verileri.append((gun_id, gun, ay, yil, icerik))

            # Doğumlar
            for dogum in gun_verisi['dogumlar']:
                yil, icerik = yil_ve_icerik_ayir(dogum)
                dogum_verileri.append((gun_id, gun, ay, yil, icerik))

            # Ölümler
            for olum in gun_verisi['olumler']:
                yil, icerik = yil_ve_icerik_ayir(olum)
                olum_verileri.append((gun_id, gun, ay, yil, icerik))

            # Tatiller
            for tatil in gun_verisi['tatiller']:
                tatil_verileri.append((gun_id, gun, ay, tatil))

        # Verileri Supabase'e toplu şekilde ekle
        verileri_toplu_ekle(cursor, 'olay', olay_verileri)
        conn.commit()
        
        verileri_toplu_ekle(cursor, 'dogum', dogum_verileri)
        conn.commit()
        
        verileri_toplu_ekle(cursor, 'olum', olum_verileri)
        conn.commit()
        
        verileri_toplu_ekle(cursor, 'tatil', tatil_verileri)
        conn.commit()

        print("Tüm veriler başarıyla Supabase'e aktarıldı.")
    
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    json_verileri_aktar() 