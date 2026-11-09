"""Konfigurasi BRIDGE."""
import os

PORT = 5050
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
HIST_FILE = os.path.join(DATA_DIR, "bridge_history.json")
CONTACT_FILE = os.path.join(DATA_DIR, "bridge_contacts.json")
TTS_RIWAYAT_TUNANETRA = 10  # tunanetra mendengar 10 chat terakhir
