import json
import psycopg2
import re

def veritabanina_baglan():
    return psycopg2.connect(
        dbname='wikipedia_days',
        user='postgres',
        password='1234',
        host='localhost',
        port='5432'
    )

def gun_id_getir(cursor, gun, ay):
    cursor.execute(
        "SELECT id FROM gun WHERE gun = %s AND ay = %s",
        (gun, ay)
    )
    return cursor.fetchone()[0]

def yil_ve_icerik_ayir(metin):
    # "2023 - Bu bir olay" formatındaki metinden yıl ve içeriği ayırır
    parcalar = metin.split(" - ", 1)
    if len(parcalar) == 2:
        try:
            yil = int(parcalar[0])
            icerik = parcalar[1]
            return yil, icerik
        except ValueError:
            return None, metin
    return None, metin

def verileri_ekle(cursor, gun_id, gun, ay, veriler, tablo_adi):
    for veri in veriler:
        if tablo_adi == 'tatil':
            cursor.execute(
                f"INSERT INTO {tablo_adi} (gun_id, gun, ay, icerik) VALUES (%s, %s, %s, %s)",
                (gun_id, gun, ay, veri)
            )
        else:
            yil, icerik = yil_ve_icerik_ayir(veri)
            cursor.execute(
                f"INSERT INTO {tablo_adi} (gun_id, gun, ay, yil, icerik) VALUES (%s, %s, %s, %s, %s)",
                (gun_id, gun, ay, yil, icerik)
            )

def json_verileri_aktar():
    conn = veritabanina_baglan()
    cursor = conn.cursor()

    with open('turkce_tum_gunler.json', 'r', encoding='utf-8') as f:
        veriler = json.load(f)

    for gun_verisi in veriler:
        # Tarih bilgisini parçala (format: "01-01")
        gun, ay = map(int, gun_verisi['tarih'].split('-'))
        
        # Gün ID'sini al
        gun_id = gun_id_getir(cursor, gun, ay)

        # Verileri ilgili tablolara ekle
        verileri_ekle(cursor, gun_id, gun, ay, gun_verisi['olaylar'], 'olay')
        verileri_ekle(cursor, gun_id, gun, ay, gun_verisi['dogumlar'], 'dogum')
        verileri_ekle(cursor, gun_id, gun, ay, gun_verisi['olumler'], 'olum')
        verileri_ekle(cursor, gun_id, gun, ay, gun_verisi['tatiller'], 'tatil')

    conn.commit()
    print("✅ Veriler başarıyla PostgreSQL'e aktarıldı.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    json_verileri_aktar()
