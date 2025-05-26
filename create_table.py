import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
# PostgreSQL bağlantısı
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    sslmode=os.getenv('DB_SSL_MODE')
)

cursor = conn.cursor()

# Önce tüm tabloları sil (test için)
cursor.execute("DROP TABLE IF EXISTS tatil, olum, dogum, olay, gun CASCADE;")
conn.commit()

# SQL komutları (çok satırlı string)
create_tables_sql = """
-- Gün tablosu
CREATE TABLE IF NOT EXISTS gun (
    id SERIAL PRIMARY KEY,
    gun INTEGER NOT NULL CHECK (gun >= 1 AND gun <= 31),
    ay INTEGER NOT NULL CHECK (ay >= 1 AND ay <= 12),
    UNIQUE (gun, ay)
);

-- Olaylar tablosu
CREATE TABLE IF NOT EXISTS olay (
    id SERIAL PRIMARY KEY,
    gun_id INTEGER REFERENCES gun(id) ON DELETE CASCADE,
    gun INTEGER NOT NULL,
    ay INTEGER NOT NULL,
    yil INTEGER,
    icerik TEXT NOT NULL
);

-- Doğumlar tablosu
CREATE TABLE IF NOT EXISTS dogum (
    id SERIAL PRIMARY KEY,
    gun_id INTEGER REFERENCES gun(id) ON DELETE CASCADE,
    gun INTEGER NOT NULL,
    ay INTEGER NOT NULL,
    yil INTEGER,
    icerik TEXT NOT NULL
);

-- Ölümler tablosu
CREATE TABLE IF NOT EXISTS olum (
    id SERIAL PRIMARY KEY,
    gun_id INTEGER REFERENCES gun(id) ON DELETE CASCADE,
    gun INTEGER NOT NULL,
    ay INTEGER NOT NULL,
    yil INTEGER,
    icerik TEXT NOT NULL
);

-- Tatiller tablosu
CREATE TABLE IF NOT EXISTS tatil (
    id SERIAL PRIMARY KEY,
    gun_id INTEGER REFERENCES gun(id) ON DELETE CASCADE,
    gun INTEGER NOT NULL,
    ay INTEGER NOT NULL,
    icerik TEXT NOT NULL
);
"""

# SQL'leri çalıştır
cursor.execute(create_tables_sql)
conn.commit()

# Günleri otomatik ekle
for ay in range(1, 13):
    for gun in range(1, 32):
        # 30 günlük aylar için kontrol
        if gun == 31 and ay in [4, 6, 9, 11]:
            continue
        # Şubat ayı için kontrol
        if ay == 2 and gun > 29:
            continue
        
        cursor.execute(
            "INSERT INTO gun (gun, ay) VALUES (%s, %s)",
            (gun, ay)
        )

conn.commit()

print("✅ Tüm tablolar başarıyla oluşturuldu ve günler eklendi.")

# Bağlantıyı kapat
cursor.close()
conn.close()