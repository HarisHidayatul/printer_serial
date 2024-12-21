import subprocess

def is_printer_connected(vendor_id, product_id):
    result = subprocess.run(['lsusb'], stdout=subprocess.PIPE, text=True)
    devices = result.stdout.splitlines()
    for device in devices:
        if f"{vendor_id}:{product_id}" in device:
            return True
    return False

# Ganti vendor_id dan product_id sesuai printer Anda
VENDOR_ID = "04b8"  # EPSON Vendor ID
PRODUCT_ID = "0202"  # Contoh Product ID untuk TM-U220B

if is_printer_connected(VENDOR_ID, PRODUCT_ID):
    print("Printer is connected.")
else:
    print("Printer is not connected.")
