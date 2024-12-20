import os

PRINTER_DEVICE = "/dev/usb/lp0"

try:
    # Kirim perintah status ke printer
    with open(PRINTER_DEVICE, "wb") as printer:
        printer.write(b'\x10\x04\x04')

    # Baca respons dari printer
    with open(PRINTER_DEVICE, "rb") as printer:
        response = printer.read(16)
        print(f"Response: {response.hex()}")

        # Interpretasi respons
        if response.startswith(b'\x12'):
            print("Kertas cukup.")
        elif response.startswith(b'\x1e'):
            print("Kertas hampir habis.")
        elif response.startswith(b'\x72'):
            print("Kertas habis.")
        elif response.startswith(b'\x7e'):
            print("Kertas habis total.")
        else:
            print("Status tidak diketahui.")
except PermissionError:
    print("Permission denied. Try running with sudo.")
except Exception as e:
    print(f"Error: {e}")
