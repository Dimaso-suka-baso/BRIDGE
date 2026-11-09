# =====================================
# PENGEMBANGAN DATABASE CHAT BRIDGE
# =====================================

import sqlite3
from datetime import datetime

DB_NAME = "bridge_chat.db"


def buat_database():
    koneksi = sqlite3.connect(DB_NAME)
    cursor = koneksi.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pesan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pengirim TEXT NOT NULL,
            penerima TEXT NOT NULL,
            isi_pesan TEXT NOT NULL,
            waktu TEXT NOT NULL
        )
    """)

    koneksi.commit()
    koneksi.close()
    print("Database BRIDGE berhasil dibuat!")


def simpan_pesan(pengirim, penerima, isi_pesan):
    koneksi = sqlite3.connect(DB_NAME)
    cursor = koneksi.cursor()

    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO pesan (pengirim, penerima, isi_pesan, waktu)
        VALUES (?, ?, ?, ?)
    """, (pengirim, penerima, isi_pesan, waktu))

    koneksi.commit()
    koneksi.close()
    print("Pesan berhasil disimpan!")


if __name__ == "__main__":
    buat_database()