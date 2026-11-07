BALASAN_CEPAT = ["Ya, saya mengerti.", "Tolong kirim teks.", "Terima kasih."]

def bacakan(teks, suara_aktif):
    
    if suara_aktif:
        print(f"🔊 [SUARA SISTEM MEMBACAKAN]: '{teks}'")

def jalankan():
    suara_aktif = True
    print("=== Prototipe Chat Sederhana ===")

    while True:
        print("\nMenu: [1] Kirim  [2] Terima  [3] Balas Cepat  [4] Suara On/Off  [0] Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            pesan = input("Tulis pesan: ")
            print(f"-> Pesan Terkirim: {pesan}")
            
        elif pilihan == "2":
            pesan = input("Tulis pesan masuk: ")
            print(f"<- Pesan Masuk: {pesan}")
            bacakan(pesan, suara_aktif)
            
        elif pilihan == "3":
            print("1. Ya, mengerti | 2. Tolong kirim teks | 3. Terima kasih")
            nomor = input("Pilih nomor balasan (1-3): ")
            if nomor in ["1", "2", "3"]:
                print(f"-> Pesan Terkirim: {BALASAN_CEPAT[int(nomor) - 1]}")
            else:
                print("Pilihan tidak valid.")
                
        elif pilihan == "4":
            suara_aktif = not suara_aktif
            print(f"Fitur Suara: {'AKTIF' if suara_aktif else 'MATI'}")
            
        elif pilihan == "0":
            print("Keluar dari program. Terima kasih!")
            break
            
        else:
            print("Menu tidak dikenal.")

if __name__ == "__main__":
    jalankan()