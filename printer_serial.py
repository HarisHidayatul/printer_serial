import cups
import time

# Nama printer yang digunakan
PRINTER_NAME = "EPSON_TM_U220B"  # Ganti dengan nama printer Anda

def check_printer_status(printer_name):
    """Memeriksa status printer dan mengembalikan pesan kesalahan atau status lainnya."""
    try:
        # Membuat koneksi ke server CUPS
        conn = cups.Connection()

        # Mendapatkan status printer
        printer_status = conn.getPrinterAttributes(printer_name)

        # Memeriksa status printer (status 3 berarti offline)
        status = printer_status.get('printer-state', None)
        reason = printer_status.get('printer-state-reasons', None)

        if status == 3:
            # Printer offline
            return "Printer offline"
        elif status == 5:
            # Printer error
            return f"Printer error: {reason}"
        elif status == 4:
            # Printer idle, tetapi dapat mengalami masalah
            return "Printer idle"
        elif status == 2:
            # Printer ready
            return "Printer ready"
        else:
            return "Unknown status"

    except Exception as e:
        print(f"Error checking printer status: {e}")
        return "Error checking printer status"

def main():
    """Program utama untuk memeriksa status printer secara berkala."""
    while True:
        status = check_printer_status(PRINTER_NAME)
        print(f"Printer Status: {status}")
        time.sleep(5)  # Cek status setiap 5 detik

if __name__ == "__main__":
    main()
