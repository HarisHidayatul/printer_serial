from escpos.printer import Usb

# Konfigurasi USB untuk Epson TM-U220B
p = Usb(0x04b8, 0x0202)  # Vendor ID: 0x04b8, Product ID: 0x0202

# Inisialisasi printer
p.text("\n")

# Data bitmap 1000 bytes (semua titik hitam)
bitmap_data = [0xFF] * 1000  

# ESC/POS Command: Print raster bit image
# m = Mode (0 = 8-dot single-density)
# nL = 1000 % 256 = 232 (0xE8)
# nH = 1000 // 256 = 3 (0x03)
p._raw(b'\x1B*\x00\xE8\x03')  # ESC * 0 1000 (width) 
p._raw(bytes(bitmap_data))    # Data bitmap

# Feed kertas dan potong
p.text("\n")