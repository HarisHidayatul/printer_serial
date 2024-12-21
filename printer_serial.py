import cups

# Fungsi untuk mengirimkan print job
def test_print():
    try:
        # Koneksi ke CUPS
        conn = cups.Connection()

        # Dapatkan daftar printer yang terhubung
        printers = conn.getPrinters()

        # Tentukan nama printer (ganti dengan nama printer Anda)
        printer_name = "EPSON_TM_U220B"

        # Periksa apakah printer tersedia
        if printer_name in printers:
            # Mencetak satu karakter
            conn.printText(printer_name, "A")
            print(1)  # Berhasil
        else:
            print(0)  # Printer tidak ditemukan
    except Exception as e:
        print(0)  # Jika ada kesalahan
        print(f"Error: {e}")

# Jalankan tes print
test_print()
