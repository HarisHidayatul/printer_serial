from escpos.printer import Usb

# Konfigurasi USB untuk Epson TM-U220B (sesuaikan dengan ID Vendor dan ID Produk)
# ID Vendor dan Produk bisa didapatkan dari `lsusb`
p = Usb(0x04b8, 0x0202)  # Vendor ID: 0x04b8, Product ID: 0x0202

# Inisialisasi printer
# p.text("Printing 10 dots horizontal for 200 lines")
p.text("\n")

# Data bitmap untuk 10 dots horizontal per baris, 256 baris
bitmap_data = []
for _ in range(200):
    bitmap_data.append(0xFF)  # Byte pertama (semua titik hitam)

# ESC/POS Command: Print raster bit image
# Format: ESC * m nL nH d1...dk
# m = Mode (0 = 8-dot single-density), nL = Width in bytes (2), nH = High byte (0)
# C8 200 Baris Maksimal
p._raw(b'\x1B*\x00\xC8\x00')  # ESC * 0 2 0 (10 dots / 8 = 2 bytes)
p._raw(bytes(bitmap_data))    # Data bitmap
p._raw(bytes(bitmap_data))    # Data bitmap
p._raw(bytes(bitmap_data))    # Data bitmap
p._raw(bytes(bitmap_data))    # Data bitmap
p._raw(bytes(bitmap_data))    # Data bitmap
p._raw(bytes(bitmap_data))    # Data bitmap
p.text("\n")
# Feed kertas dan potong
# p.text("256 lines of 10 horizontal dots printed\n\n")

# print("256 lines of 10 dots horizontal printed successfully!")
