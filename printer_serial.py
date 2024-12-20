import cups
import os

def get_printer_status(printer_name):
    conn = cups.Connection()
    printers = conn.getPrinters()

    # Verifikasi keberadaan perangkat USB
    usb_devices = os.popen('lsusb').read()
    if "EPSON" not in usb_devices:
        return "Printer not connected"

    if printer_name in printers:
        status = printers[printer_name]['printer-state']
        if status == 3:
            return "Ready"
        elif status == 4:
            return "Paused"
        elif status == 5:
            return "Error"
    return "Unknown"

printer_name = "EPSON_TM_U220B"
status = get_printer_status(printer_name)
print(f"Printer {printer_name} status: {status}")
