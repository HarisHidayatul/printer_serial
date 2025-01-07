from escpos.printer import Usb

# Konfigurasi USB untuk Epson TM-U220B (sesuaikan dengan ID Vendor dan ID Produk)
# ID Vendor dan Produk bisa didapatkan dari `lsusb`
p = Usb(0x04b8, 0x0202)  # Vendor ID: 0x04b8, Product ID: 0x0202

# Inisialisasi printer
p.text("Printing 10 dots horizontal\n\n")

# Data bitmap untuk 10 dots horizontal
# 10 dots = 2 bytes (karena 10/8 = 1 byte penuh + 2 dots tambahan)
bitmap_data = [
    0b11111111,  # Byte 1: 8 dots penuh (semua hitam)
    0b11111111,  # Byte 2: 8 dots penuh (semua hitam)
    0b11111111,  # Byte 3: 8 dots penuh (semua hitam)
    0b11111111,  # Byte 4: 8 dots penuh (semua hitam)
    0b11111111,  # Byte 5: 8 dots penuh (semua hitam)
    0b11111111,  # Byte 6: 8 dots penuh (semua hitam)
    0b11111111,  # Byte 7: 8 dots penuh (semua hitam)
    0b11111111,  # Byte 8: 8 dots penuh (semua hitam)
    0b11111111,  # Byte 9: 8 dots penuh (semua hitam)
    0b11111111,  # Byte 10: 8 dots penuh (semua hitam)
]

# ESC/POS Command: Print raster bit image
# Format: ESC * m nL nH d1...dk
# m = Mode (0 = 8-dot single-density), nL = Width in bytes (2), nH = High byte (0)
p._raw(b'\x1B*\x00\x0A\x00')  # ESC * 0 2 0 (10 dots / 8 = 2 bytes)
p._raw(bytes(bitmap_data))    # Data bitmap

# Feed kertas dan potong
p.text("\n\n")
p.text("Total horizontal dots printed: 10\n\n")

print("10 dots horizontal printed successfully!")
