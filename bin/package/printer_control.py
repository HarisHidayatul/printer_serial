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
    def printing_byte(self,array_byte):
        # Array byte ini dihitung secara horizontal
        bitmap_data = [0x00] * 200
        loop_index = 0
        for loop_byte in array_byte:
            bitmap_data[loop_index] = loop_byte
            loop_index = loop_index + 1
        self.printer._raw(b'\x1B*\x00\xC8\x00')
        self.printer._raw(bytes(bitmap_data))    # Data bitmap
        self.printer.text("\n")