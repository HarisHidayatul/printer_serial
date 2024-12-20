import subprocess

def check_printer():
    # Jalankan perintah lsusb dan ambil hasilnya
    result = subprocess.run(['lsusb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Jika perintah berhasil
    if result.returncode == 0:
        # Periksa setiap baris output lsusb
        for line in result.stdout.splitlines():
            # Mencari printer Epson berdasarkan ID vendor (misalnya 0x04b8 untuk Epson)
            if 'EPSON' in line:
                print("Printer Epson ditemukan:", line)
                return True
        print("Printer Epson tidak ditemukan.")
        return False
    else:
        print("Error menjalankan lsusb:", result.stderr)
        return False

# Memanggil fungsi untuk memeriksa keberadaan printer
if __name__ == "__main__":
    check_printer()
