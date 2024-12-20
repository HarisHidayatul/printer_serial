import usb.core
import usb.util
import subprocess
import time

# Vendor ID dan Product ID printer Epson TM-U220B
VENDOR_ID = 0x04b8
PRODUCT_ID = 0x0202

# Fungsi untuk mengakses perangkat USB dengan sudo
def access_usb_device():
    result = subprocess.run(['sudo', 'python3', 'printer_serial.py'], capture_output=True, text=True)
    print(result.stdout)

# Fungsi utama untuk mengakses printer dan memeriksa status
def check_printer_status():
    # Cari perangkat USB
    printer = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

    if printer is None:
        raise ValueError("Printer tidak ditemukan")

    # Atur konfigurasi printer
    printer.set_configuration()

    # Kirim perintah untuk memeriksa status kertas (ESC/POS: DLE EOT 4)
    try:
        # Endpoint 1 biasanya digunakan untuk menulis data
        printer.write(1, b'\x10\x04\x04')

        # Baca respons dari printer (endpoint 0x81 biasanya untuk membaca data)
        response = printer.read(0x81, 16, timeout=1000)
        status = bytes(response).hex()
        print(f"Status printer: {status}")

        # Interpretasi status berdasarkan dokumentasi ESC/POS
        if status.startswith("12"):
            print("Kertas cukup.")
        elif status.startswith("1e"):
            print("Kertas hampir habis.")
        elif status.startswith("72"):
            print("Kertas habis.")
        elif status.startswith("7e"):
            print("Kertas habis total.")
        else:
            print("Status tidak diketahui.")
    except usb.core.USBTimeoutError:
        print("Timeout saat membaca status printer.")
    except usb.core.USBError as e:
        print(f"Error USB: {e}")

if __name__ == "__main__":
    try:
        check_printer_status()
    except ValueError as e:
        print(e)
