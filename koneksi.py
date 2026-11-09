"""Lapisan jaringan LAN/Wi-Fi (TCP). Paket berformat JSON per baris."""
import ipaddress
import json
import os
import socket
import threading

from BRIDGE.config import PORT
from util import out


class Koneksi:
    def __init__(self, peran, on_terhubung, on_putus, on_paket, port=PORT):
        self.peran = peran
        self.port = port
        self.on_terhubung, self.on_putus, self.on_paket = on_terhubung, on_putus, on_paket
        self.conn = None
        self.status = "terputus"  # menghubungkan :| | terhubung :) | terputus :(
        self.peer_ip = None
        self.peer_peran = None
        self.ip_sendiri = self._ip_lokal()
        self._kirim_lock = threading.Lock()
        self._aktif = True

    @staticmethod
    def _ip_lokal():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("10.255.255.255", 1))
            return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
        finally:
            s.close()

    # --- validasi (DFD 1.2) ---
    def validasi_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            return "format IP tidak valid"
        if ip in (self.ip_sendiri, "127.0.0.1") and not os.environ.get("BRIDGE_DEBUG"):
            return "alamat perangkat sendiri"
        if self.status == "terhubung":
            return "tujuan lebih dari satu (sudah terhubung dengan satu perangkat)"
        return None

    # --- menyambung keluar ---
    def hubungkan(self, ip, port=None):
        self.status = "menghubungkan"
        try:
            s = socket.create_connection((ip, port or self.port), timeout=5)
            s.settimeout(None)
        except Exception as e:
            self.status = "terputus"
            return False, str(e)
        self._pasang(s, ip)
        return True, ""

    # --- menunggu sambungan masuk ---
    def mulai_listener(self):
        threading.Thread(target=self._listener, daemon=True).start()

    def _listener(self):
        try:
            srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind(("0.0.0.0", self.port))
            srv.listen(1)
        except Exception as e:
            out("[KESALAHAN] Tidak dapat membuka port %d: %s" % (self.port, e))
            return
        while self._aktif:
            try:
                s, addr = srv.accept()
            except Exception:
                continue
            if self.status == "terhubung":  # versi SKPL hanya dua perangkat boss
                s.close()
                continue
            self._pasang(s, addr[0])

    def _pasang(self, s, ip):
        self.conn, self.peer_ip, self.status = s, ip, "terhubung"
        try:
            self.kirim({"type": "hello", "peran": self.peran})
        except Exception:
            pass
        threading.Thread(target=self._penerima, args=(s,), daemon=True).start()
        self.on_terhubung(ip)

    # --- kirim / terima ---
    def kirim(self, obj):
        """Melempar exception bila gagal."""
        data = (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")
        with self._kirim_lock:
            self.conn.sendall(data)

    def _penerima(self, s):
        buf = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                buf += chunk
                while b"\n" in buf:
                    baris, buf = buf.split(b"\n", 1)
                    try:
                        p = json.loads(baris.decode("utf-8"))
                    except Exception:
                        out("[INFO] Menerima data yang tidak dapat dibaca; diabaikan.")
                        continue
                    if p.get("type") == "hello":
                        self.peer_peran = p.get("peran")
                    else:
                        self.on_paket(p)
        except Exception:
            pass
        if s is self.conn:
            self.putus()

    def putus(self):
        if self.status != "terputus":
            self.status = "terputus"
            try:
                self.conn.shutdown(socket.SHUT_RDWR)  # pastikan sisi lain tahu
            except Exception:
                pass
            try:
                self.conn.close()
            except Exception:
                pass
            self.on_putus()

    def tutup(self):
        self._aktif = False
        self.putus()
