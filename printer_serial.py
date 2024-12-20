import cups

def check_printer_status(printer_name):
    try:
        # Membuat koneksi ke server CUPS
        conn = cups.Connection()

        # Mendapatkan status printer
        printer_status = conn.getPrinterAttributes(printer_name)

        # Memeriksa status printer (status 3 berarti offline)
        status = printer_status.get('printer-state', None)

        # Menampilkan status printer
        if status == 3:
            return "Printer offline"
        elif status == 2:
            return "Printer idle"
        elif status == 4:
            return "Printer printing"
        else:
            return "Unknown status"
    except Exception as e:
        return f"Error checking printer status: {e}"

def print_test_page(printer_name, message):
    try:
        # Menentukan printer
        conn = cups.Connection()
        
        # Mengirim perintah untuk mencetak
        conn.printFile(printer_name, "/dev/null", "Test Print", {"text": message})
        print(f"Successfully printed: {message}")
    except Exception as e:
        print(f"Error printing: {e}")

if __name__ == "__main__":
    printer_name = "EPSON_TM_U220B"  # Ganti dengan nama printer yang sesuai
    
    # Periksa status printer
    status = check_printer_status(printer_name)
    print(f"Printer Status: {status}")
    
    # Jika printer online, lakukan pencetakan
    if "idle" in status.lower() or "printing" in status.lower():
        print_test_page(printer_name, "Test print from Python using CUPS.")
    else:
        print("Printer is not online, cannot print.")
