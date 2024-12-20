import subprocess

# Nama printer yang digunakan
printer_name = "EPSON_TM_U220B"  # Ganti dengan nama printer yang sesuai

def check_printer_status(printer_name):
    try:
        # Menjalankan perintah lpstat untuk mendapatkan status printer
        result = subprocess.run(['lpstat', '-p', printer_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            print(f"Error checking printer status: {result.stderr.decode()}")
            return "offline"

        status = result.stdout.decode()
        if "is ready" in status:
            return "online"
        elif "is printing" in status:
            return "printing"
        elif "is stopped" in status or "is idle" in status:
            return "offline"
        elif "is on hold" in status:
            return "on hold"
        elif "is in error" in status:
            return "error"
        else:
            return "unknown"
    except Exception as e:
        print(f"Error checking printer status: {e}")
        return "offline"

def print_status(printer_name):
    printer_status = check_printer_status(printer_name)
    print(f"Printer Status: {printer_status}")

if __name__ == "__main__":
    print_status(printer_name)
