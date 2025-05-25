import wikipediaapi
import json
from datetime import datetime

def ay_adini_getir(ay):
    ay_isimleri = [
        "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
        "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
    ]
    return ay_isimleri[ay - 1]

def tatile_ozel_ayikla(bolum):
    maddeler = []
    for satir in bolum.text.split('\n'):
        satir = satir.strip()
        if satir and not satir.startswith("==") and not satir.lower().startswith("kaynakça"):
            maddeler.append(satir.lstrip("*•-— ").strip())
    return maddeler

def wiki_ayarla():
    return wikipediaapi.Wikipedia(
        language='tr',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='BugunNeOlduScraper/1.0 (hakan@ornekmail.com)'
    )

def bolumu_ayikla(bolum):
    maddeler = []
    current_year = None
    
    lines = bolum.text.split('\n')
    i = 0
    
    while i < len(lines):
        satir = lines[i].strip()
        
        # Yıl kontrolü - sadece yıl olan satırlar için
        if satir and satir[:4].isdigit() and 1000 <= int(satir[:4]) <= 2024:
            current_year = satir[:4]
            
            # Eğer yıl satırında direkt olay varsa ekle
            event = satir[4:].strip().lstrip('*•-— :')
            if event:
                maddeler.append(f"{current_year} - {event}")
                
            # Sonraki satırlardaki bullet pointleri kontrol et
            next_line_idx = i + 1
            while (next_line_idx < len(lines) and 
                   lines[next_line_idx].strip() and 
                   (lines[next_line_idx].strip().startswith(('*', '•', '-', '—')) or 
                    lines[next_line_idx].strip()[0].isspace())):
                bullet_event = lines[next_line_idx].strip().lstrip('*•-— ')
                if bullet_event:
                    maddeler.append(f"{current_year} - {bullet_event}")
                next_line_idx += 1
            i = next_line_idx - 1
        
        i += 1
    
    return maddeler

def gun_verisini_getir(wiki, ay, gun):
    sayfa_basligi = f"{ay_adini_getir(ay)}_{gun}"
    sayfa = wiki.page(sayfa_basligi)

    if not sayfa.exists():
        print(f"❌ Sayfa bulunamadı: {sayfa_basligi}")
        return None

    gun_verisi = {
        "tarih": f"{gun:02d}-{ay:02d}",
        "olaylar": [],
        "dogumlar": [],
        "olumler": [],
        "tatiller": []
    }

    for bolum in sayfa.sections:        
        baslik = bolum.title.lower()
        if "olaylar" in baslik:
            gun_verisi["olaylar"] = bolumu_ayikla(bolum)
        elif "doğumlar" in baslik:
            gun_verisi["dogumlar"] = bolumu_ayikla(bolum)
        elif "ölümler" in baslik:
            gun_verisi["olumler"] = bolumu_ayikla(bolum)
        elif any(kelime in baslik for kelime in ["tatil", "özel gün", "kutlama"]):            
            gun_verisi["tatiller"] = tatile_ozel_ayikla(bolum)

    return gun_verisi

def jsona_kaydet(data, dosya_adi):
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=6)

# Tüm yıl için veri çek
if __name__ == "__main__":
    wiki = wiki_ayarla()
    tum_veriler = []
    
    # Her ay için
    for ay in range(1, 13):
        # Her gün için
        max_gun = 31
        if ay in [4, 6, 9, 11]:  # 30 günlük aylar
            max_gun = 30
        elif ay == 2:  # Şubat
            max_gun = 29
        
        for gun in range(1, max_gun + 1):
            try:
                veri = gun_verisini_getir(wiki, ay, gun)
                if veri:
                    tum_veriler.append(veri)
                    print(f"✅ {veri['tarih']} eklendi.")
                else:
                    print(f"⚠️ {gun:02d}-{ay:02d} için veri bulunamadı.")
            except Exception as e:
                print(f"❌ Hata oluştu: {gun:02d}-{ay:02d} - {e}")
            
            # Her 10 günde bir kaydet (hata durumunda veri kaybını önlemek için)
            if len(tum_veriler) % 10 == 0:
                jsona_kaydet(tum_veriler, 'turkce_tum_gunler.json')
                print("💾 Ara kayıt yapıldı.")
    
    # Son kayıt
    jsona_kaydet(tum_veriler, 'turkce_tum_gunler.json')
    print("🎉 Tüm yıl başarıyla kaydedildi.")
