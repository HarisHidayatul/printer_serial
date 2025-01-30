from escpos.printer import Usb

# Konfigurasi USB untuk Epson TM-U220B
p = Usb(0x04b8, 0x0202)  # Vendor ID: 0x04b8, Product ID: 0x0202

# Inisialisasi printer
p.text("\n")

# Lebar gambar dalam bytes (200 bytes = 1600 dots horizontal)
width_bytes = 200  
height = 1000  

# Buat bitmap dengan warna hitam penuh (semua titik dicetak)
bitmap_data = [0xFF] * (width_bytes * height)

# Kirim dalam blok maksimal 255 baris per kali cetak
max_block_height = 255  
for i in range(0, height, max_block_height):
    block_size = min(max_block_height, height - i)  # Jika sisa baris kurang dari 255, sesuaikan
    nL = width_bytes % 256  # 200 % 256 = 200 (0xC8)
    nH = width_bytes // 256  # 200 // 256 = 0 (0x00)

    # ESC/POS Command: Print raster bit image
    p._raw(bytes([0x1B, 0x2A, 0x00, nL, nH]))  # ESC * 0 200 0
    p._raw(bytes(bitmap_data[i * width_bytes:(i + block_size) * width_bytes]))  # Kirim data sesuai blok
    p.text("\n")  # Baris baru setelah setiap blok

# Feed kertas dan potong (opsional)
# p.cut()
