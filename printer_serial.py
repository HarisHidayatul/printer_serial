import os
import cups
import time

# Nama printer yang digunakan
printer_name = "EPSON_TM_U220B"  # Ganti dengan nama printer yang sesuai

def check_printer_status(printer_name):
    try:
        # Membuat koneksi ke server CUPS
        conn = cups.Connection()

        # Mendapatkan status printer
        printer_status = conn.getPrinterAttributes(printer_name)

        # Menampilkan status printer secara detail
        print(f"Printer status details: {printer_status}")

        # Memeriksa status printer
        status = printer_status.get('printer-state', None)
        if status is None:
            return "Error: Unable to fetch printer status"

        # Status Printer
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

def print_test_message():
    # Pesan uji untuk dicetak
    message = "Test print from Raspberry Pi\n\n\n"
    
    # Menggunakan perintah lp untuk mencetak
    command = f'echo -e "{message}" | lp -d {printer_name}'
    
    # Eksekusi perintah untuk mencetak
    result = os.system(command)
    if result == 0:
        print("Print successful")
    else:
        print("Print failed")

def main():
    while True:
        # Cek status printer setiap 5 detik
        printer_status = check_printer_status(printer_name)
        print(f"Printer Status: {printer_status}")
        
        # Jika printer dalam status idle, coba cetak
        if printer_status == "Printer idle":
            print("Printer is idle. Printing test message...")
            print_test_message()
        else:
            print("Printer is not idle, cannot print.")
        
        # Tunggu 5 detik sebelum memeriksa status printer lagi
        time.sleep(5)

if __name__ == "__main__":
    main()
