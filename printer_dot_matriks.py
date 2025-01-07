from escpos.printer import Usb

# Konfigurasi USB untuk Epson TM-U220B (sesuaikan dengan ID Vendor dan ID Produk)
# ID Vendor dan Produk bisa didapatkan dari `lsusb`
p = Usb(0x04b8, 0x0202)  # Vendor ID: 0x04b8, Product ID: 0x0202

# Fungsi untuk membuat data bitmap berdasarkan jumlah titik
def create_bitmap(width, height):
    """Membuat data bitmap untuk gambar dengan lebar dan tinggi tertentu."""
    num_bytes = (width + 7) // 8  # Menambah 7 untuk pembulatan ke atas
    bitmap = []
    
    # Setiap baris gambar (tinggi)
    for _ in range(height):
        # Semua byte penuh (semua titik hitam)
        bitmap.extend([0b11111111] * (num_bytes - 1))  # Semua byte penuh
        remaining_bits = width % 8  # Sisa titik setelah byte penuh
        if remaining_bits > 0:
            bitmap.append((1 << remaining_bits) - 1)  # Tambahkan byte terakhir dengan sisa titik
    
    return bitmap

# Inisialisasi printer
p.text("Printing 576 dots horizontal and 200 dots vertical\n\n")

# Data bitmap untuk 576 dots horizontal dan 200 dots vertikal
bitmap_data = create_bitmap(576, 200)

# ESC/POS Command: Print raster bit image
# Format: ESC * m nL nH d1...dk
# m = Mode (0 = 8-dot single-density), nL = Width in bytes (576/8), nH = High byte (0)
p._raw(b'\x1B*\x00\x90\x00')  # ESC * 0 144 0 (576 dots / 8 = 72 bytes)
p._raw(bytes(bitmap_data))    # Data bitmap

# Feed kertas dan potong
p.text("\n\n")

print("576 dots horizontal and 200 dots vertical printed successfully!")
