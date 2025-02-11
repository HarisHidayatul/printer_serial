from escpos.printer import Usb
class printer_control:
    def __init__(self, vendor_id, product_id):
        # Inisialisasi printer
        try:
            # Inisialisasi printer
            # Vendor ID: 0x04b8, Product ID: 0x0202 Pada Raspi Saya
            # vendor_id = 0x04B8  Epson product_id = 0x0202  # TM-U220B #Pada PC saya
            self.printer = Usb(vendor_id, product_id)
            print("Printer berhasil dihubungkan.")
        except Exception as e:
            print(f"Error: Tidak dapat menghubungkan printer. {e}")
            self.printer = None  # Hindari error jika printer tidak terhubung
    def printing_byte(array_byte):
        for loop_byte in array_byte:

bitmap_data = []
for _ in range(200):
    bitmap_data.append(0xFF)  # Byte pertama (semua titik hitam)

# ESC/POS Command: Print raster bit image
# Format: ESC * m nL nH d1...dk
# m = Mode (0 = 8-dot single-density), nL = Width in bytes (2), nH = High byte (0)
# C8 200 Baris Maksimal
p._raw(b'\x1B*\x00\xC8\x00')  # ESC * 0 2 0 (10 dots / 8 = 2 bytes)
p._raw(bytes(bitmap_data))    # Data bitmap
p.text("\n")
# Feed kertas dan potong
# p.text("256 lines of 10 horizontal dots printed\n\n")

# print("256 lines of 10 dots horizontal printed successfully!")
