import cups
import time
import os
import subprocess

# Fungsi untuk melakukan pencetakan dengan lp dan memeriksa status
def print_and_check_status():
    try:
        # Tentukan nama printer (ganti dengan nama printer Anda)
        printer_name = "EPSON_TM_U220B"

        # Perintah untuk mencetak menggunakan lp
        print_command = "echo -e 'Test print from Raspberry Pi\n\n\n' | lp -d {}".format(printer_name)
        
        # Jalankan perintah untuk mencetak
        subprocess.run(print_command, shell=True)

        # Tunggu sebentar agar CUPS memproses pekerjaan cetak
        time.sleep(2)

        # Koneksi ke CUPS
        conn = cups.Connection()

        # Ambil daftar pekerjaan cetak yang sedang berjalan
        jobs = conn.getJobs()

        # Periksa apakah ada pekerjaan cetak yang berhasil
        if jobs:
            for job_id, job_info in jobs.items():
                if job_info["printer"] == printer_name and job_info["status"] == "completed":
                    print(1)  # Pencetakan berhasil
                    return
        # Jika tidak ada pekerjaan cetak atau status tidak "completed"
        print(0)  # Pencetakan gagal
    except Exception as e:
        print(0)  # Jika ada kesalahan
        print(f"Error: {e}")

# Panggil fungsi untuk melakukan pencetakan dan pengecekan status
print_and_check_status()
