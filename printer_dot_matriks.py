from escpos.printer import Usb

# Konfigurasi USB untuk Epson TM-U220B (sesuaikan dengan ID Vendor dan ID Produk)
# ID Vendor dan Produk bisa didapatkan dari `lsusb`
p = Usb(0x04b8, 0x0202)  # Vendor ID: 0x04b8, Product ID: 0x0202

# Fungsi untuk membuat data bitmap berdasarkan jumlah titik horizontal
def create_bitmap(num_dots):
    """Membuat data bitmap untuk jumlah titik horizontal tertentu."""
    # Menghitung jumlah byte yang diperlukan
    num_bytes = (num_dots + 7) // 8  # Menambah 7 untuk pembulatan ke atas

    # Membuat data bitmap dengan titik hitam (1) pada semua posisi
    bitmap = [0b11111111] * (num_bytes - 1)  # Semua byte penuh
    remaining_bits = num_dots % 8  # Sisa titik setelah byte penuh
    if remaining_bits > 0:
        bitmap.append((1 << remaining_bits) - 1)  # Tambahkan byte terakhir dengan sisa titik

    return bitmap

# Inisialisasi printer
p.text("Printing multiple rows with increasing dots\n\n")

# Baris 1: 50 dots
bitmap_data_1 = create_bitmap(50)
p._raw(b'\x1B*\x00\x07\x00')  # ESC * 0 7 0
p._raw(bytes(bitmap_data_1))  # Data bitmap baris 1
p.text("\n")

# Baris 2: 100 dots
bitmap_data_2 = create_bitmap(100)
p._raw(b'\x1B*\x00\x13\x00')  # ESC * 0 19 0
p._raw(bytes(bitmap_data_2))  # Data bitmap baris 2
p.text("\n")

# Baris 3: 150 dots
bitmap_data_3 = create_bitmap(150)
p._raw(b'\x1B*\x00\x1E\x00')  # ESC * 0 30 0
p._raw(bytes(bitmap_data_3))  # Data bitmap baris 3
p.text("\n")

# Baris 4: 200 dots
bitmap_data_4 = create_bitmap(200)
p._raw(b'\x1B*\x00\x28\x00')  # ESC * 0 40 0
p._raw(bytes(bitmap_data_4))  # Data bitmap baris 4
p.text("\n")

# Baris 5: 1000 dots
bitmap_data_5 = create_bitmap(1000)
p._raw(b'\x1B*\x00\xF4\x00')  # ESC * 0 244 0
p._raw(bytes(bitmap_data_5))  # Data bitmap baris 5

# Feed kertas dan potong
p.text("\n\n")

print("Dots printed successfully!")