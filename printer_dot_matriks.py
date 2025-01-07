from escpos.printer import Usb

# Konfigurasi USB untuk Epson TM-U220B (sesuaikan dengan ID Vendor dan ID Produk)
# ID Vendor dan Produk bisa didapatkan dari `lsusb`
p = Usb(0x04b8, 0x0202)  # Vendor ID: 0x04b8, Product ID: 0x0202

# Inisialisasi printer
p.text("Printing full horizontal line of dots\n\n")

# Data bitmap untuk baris penuh dots horizontal
# 576 dots (576 / 8 = 72 bytes) dengan semua bits aktif (semua hitam)
bitmap_data = [0b11111111] * 72  # Semua bit dalam 72 byte diisi penuh (semua hitam)

# ESC/POS Command: Print raster bit image
# Format: ESC * m nL nH d1...dk
# m = Mode (0 = 8-dot single-density), nL = Width in bytes (72), nH = High byte (0)
p._raw(b'\x1B*\x00\x48\x00')  # ESC * 0 72 0 (576 dots / 8 = 72 bytes)
p._raw(bytes(bitmap_data))    # Data bitmap

# Feed kertas dan potong
p.text("\n\n")
p.text(f"Total horizontal dots printed: 576\n\n")  # Jumlah total dot horizontal (maksimum 576)

print("Full horizontal line of dots printed successfully!")
