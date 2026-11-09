NAMA_PROJECT = "BRIDGE"
DESKRIPSI = "Bagai jembatan Bridge diharapkan mampu menjembatani komunikasi antara Tunanetra dan Tunarungu"

ANGGOTA = [
    "Aurora",
    "Dimas Aditya",
    "Dimas Bagus",
    "Sulthon",
    "Syamsul"
]

FITUR = [
    "Komunikasi dua arah antara Tunanetra dan Tunarungu",
    "Riwayat percakapan",
]

print("=" * 30)
print(f"Selamat datang di {NAMA_PROJECT}")
print(DESKRIPSI)
print("=" * 30)

print("\nAnggota tim:")
for nama in ANGGOTA:
    print(f"- {nama}")

print("\nFitur:")
for fitur in FITUR:
    print(f"- {fitur}")