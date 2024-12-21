import cups
import time
import os

# Fungsi untuk mengirimkan karakter ke printer
def send_character_to_printer(character):
    try:
        # Koneksi ke CUPS
        conn = cups.Connection()

        # Tentukan nama printer (ganti dengan nama printer Anda)
        printer_name = "EPSON_TM_U220B"

        # Periksa apakah printer tersedia
        printers = conn.getPrinters()
        if printer_name in printers:
            # Buat file teks sementara untuk dicetak
            temp_file = "/tmp/test_print.txt"

            while True:
                with open(temp_file, "w") as f:
                    f.write(character)  # Tulis karakter untuk tes print

                # Mencetak file
                job_id = conn.printFile(printer_name, temp_file, "Test Print", {})

                # Tunggu sebentar untuk memastikan print job diproses
                time.sleep(2)

                # Jika job_id berhasil, cetak 1, hapus file dan keluar
                if job_id:
                    print(1)  # Berhasil
                    os.remove(temp_file)  # Hapus file setelah berhasil dicetak
                    break  # Keluar dari loop
                else:
                    print(0)  # Gagal
                    os.remove(temp_file)  # Hapus file sementara jika gagal
                    time.sleep(2)  # Tunggu sebelum mencoba lagi
        else:
            print(0)  # Printer tidak ditemukan
    except Exception as e:
        print(0)  # Jika ada kesalahan
        print(f"Error: {e}")

# Kirim karakter "A" ke printer
send_character_to_printer("A")
