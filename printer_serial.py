import usb.core
import usb.util

# Vendor ID dan Product ID printer Epson TM-U220B
VENDOR_ID = 0x04b8
PRODUCT_ID = 0x0202

# Cari perangkat USB
printer = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if printer is None:
    raise ValueError("Printer tidak ditemukan")

# Atur konfigurasi printer
printer.set_configuration()

# Kirim perintah untuk memeriksa status kertas (ESC/POS: DLE EOT 4)
printer.write(1, b'\x10\x04\x04')  # Endpoint 1 biasanya digunakan untuk menulis data

# Baca respons dari printer
try:
    response = printer.read(0x81, 16, timeout=1000)  # Endpoint 0x81 biasanya untuk membaca data
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
