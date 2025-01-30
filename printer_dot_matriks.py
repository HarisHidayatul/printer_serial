from escpos.printer import Usb

# Konfigurasi USB untuk Epson TM-U220B
p = Usb(0x04b8, 0x0202)  # Vendor ID: 0x04b8, Product ID: 0x0202

# Inisialisasi printer
p.text("\n")

# Data bitmap untuk 10 dots horizontal per baris, 200 baris
bitmap_data = [0xFF] * (2 * 200)  # 2 byte per baris, 200 baris

# ESC/POS Command: Print raster bit image
# Format: ESC * m nL nH d1...dk
# m = 0 (8-dot single-density), nL = 2, nH = 0 (lebar 2 bytes)
# C8 200 Baris Maksimal
p._raw(b'\x1B*\x00\x02\x00')  # ESC * 0 2 0
p._raw(bytes(bitmap_data))  # Data bitmap
p.text("\n")

# Feed kertas dan potong (opsional)
# p.cut()