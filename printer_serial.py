import subprocess

def check_printer_status(printer_name):
    try:
        # Menjalankan perintah lpstat untuk mendapatkan status printer
        result = subprocess.run(['lpstat', '-p', printer_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"Error checking printer status: {result.stderr.decode()}")
            return "offline"
        
        # Jika printer statusnya offline, lpstat akan menampilkan 'printer-state' = 3
        status = result.stdout.decode()
        if "is ready" in status:
            return "online"
        else:
            return "offline"
    except Exception as e:
        print(f"Error checking printer status: {e}")
        return "offline"
