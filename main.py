"""Prototipe chat yang ramah untuk pengguna tunarungu dan tunanetra."""

import base64
import subprocess
import sys


BALASAN_CEPAT = [
    "Ya, saya mengerti.",
    "Tolong kirim pesan teks.",
    "Saya akan membalas sebentar lagi.",
    "Terima kasih.",
]


def bacakan(teks):
    """Bacakan teks memakai fitur suara bawaan Windows jika tersedia."""
    if sys.platform != "win32":
        print("Fitur suara otomatis tersedia pada Windows. Pesan tetap tampil di layar.")
        return

    encoded_text = base64.b64encode(teks.encode("utf-8")).decode("ascii")
    script = (
        "Add-Type -AssemblyName System.Speech; "
        f"$text = [Text.Encoding]::UTF8.GetString("
        f"[Convert]::FromBase64String('{encoded_text}')); "
        "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$speaker.Speak($text)"
    )
    encoded_script = base64.b64encode(script.encode("utf-16le")).decode("ascii")

    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-EncodedCommand", encoded_script],
            check=True,
        )
    except FileNotFoundError as error:
        print(f"Tidak dapat menemukan PowerShell untuk membacakan pesan: {error}")
    except subprocess.CalledProcessError as error:
        print(f"Gagal membacakan pesan dengan suara sistem: {error}")


def tampilkan_menu(suara_aktif):
    status_suara = "aktif" if suara_aktif else "nonaktif"
    print("\n=== BRIDGE - Prototipe Chat Aksesibel ===")
    print(f"Pembaca pesan: {status_suara}")
    print("1. Kirim pesan teks")
    print("2. Simulasikan pesan masuk")
    print("3. Pilih balasan cepat")
    print("4. Aktifkan/nonaktifkan pembaca pesan")
    print("0. Keluar")


def jalankan():
    suara_aktif = True
    print("Selamat datang di BRIDGE.")
    print("Ini hanya prototipe: pesan tidak dikirim melalui WhatsApp.")
    if suara_aktif:
        bacakan("Selamat datang di Bridge. Pesan tidak dikirim melalui WhatsApp.")

    while True:
        tampilkan_menu(suara_aktif)
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            pesan = input("Tulis pesan: ").strip()
            if pesan:
                print(f"Pesan terkirim (simulasi): {pesan}")
            else:
                print("Pesan tidak boleh kosong.")
        elif pilihan == "2":
            pesan = input("Tulis pesan masuk untuk simulasi: ").strip()
            if pesan:
                print(f"Pesan masuk: {pesan}")
                if suara_aktif:
                    bacakan(f"Pesan masuk. {pesan}")
            else:
                print("Pesan tidak boleh kosong.")
        elif pilihan == "3":
            for nomor, balasan in enumerate(BALASAN_CEPAT, start=1):
                print(f"{nomor}. {balasan}")
            nomor = input("Pilih balasan: ").strip()
            if nomor.isdigit() and 1 <= int(nomor) <= len(BALASAN_CEPAT):
                print(f"Balasan terkirim (simulasi): {BALASAN_CEPAT[int(nomor) - 1]}")
            else:
                print("Pilihan balasan tidak valid.")
        elif pilihan == "4":
            suara_aktif = not suara_aktif
            print(f"Pembaca pesan sekarang {'aktif' if suara_aktif else 'nonaktif'}.")
        elif pilihan == "0":
            print("Terima kasih sudah mencoba BRIDGE.")
            break
        else:
            print("Menu tidak dikenal. Silakan pilih lagi.")


if __name__ == "__main__":
    jalankan()


# =====================================
# PENGEMBANGAN APLIKASI BRIDGE
# =====================================

# BRIDGE dirancang untuk komunikasi inklusif.
# Aplikasi membantu pengguna tunarungu dan tunanetra.
# Fitur suara membantu pengguna tunanetra.
# Fitur teks membantu pengguna tunarungu.
# Pengembangan selanjutnya mencakup database chat.
# Data percakapan dapat disimpan secara permanen.
# Keamanan dan kenyamanan pengguna menjadi prioritas.