from escpos.printer import Usb

# Konfigurasi USB untuk Epson TM-U220B (sesuaikan dengan ID Vendor dan ID Produk)
# ID Vendor dan Produk bisa didapatkan dari `lsusb`
p = Usb(0x04b8, 0x0202)  # Vendor ID: 0x04b8, Product ID: 0x0202

# Inisialisasi printer
p.text("Printing 50 dots horizontal\n\n")

# Data bitmap untuk 50 dots horizontal (7 bytes)
bitmap_data = [
    0b11111111,  # Byte 1: 8 dots (semua hitam)
    0b11111111,  # Byte 2: 8 dots (semua hitam)
    0b11111111,  # Byte 3: 8 dots (semua hitam)
    0b11111111,  # Byte 4: 8 dots (semua hitam)
    0b11111111,  # Byte 5: 8 dots (semua hitam)
    0b11111111,  # Byte 6: 8 dots (semua hitam)
    0b11000000,  # Byte 7: 2 dots hitam, 6 dots putih
]

# ESC/POS Command: Print raster bit image
# Format: ESC * m nL nH d1...dk
# m = Mode (0 = 8-dot single-density), nL = Width in bytes (7), nH = High byte (0)
p._raw(b'\x1B*\x00\x07\x00')  # ESC * 0 7 0
p._raw(bytes(bitmap_data))    # Data bitmap

# Feed kertas dan potong
p.text("\n\n")
p.cut()

print("50 dots horizontal printed successfully!")
