import subprocess

def test_print(printer_name):
    try:
        # Mengirim perintah print menggunakan lp
        result = subprocess.run(
            ["lp", "-d", printer_name, "-o", "raw", "/dev/null"],  # /dev/null berarti tidak ada dokumen yang dicetak
            check=True,  # Jika perintah gagal, akan memunculkan exception
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("1")  # Berhasil mencetak
    except subprocess.CalledProcessError:
        print("0")  # Gagal mencetak

# Ganti dengan nama printer Anda
printer_name = "EPSON_TM_U220B"
test_print(printer_name)
