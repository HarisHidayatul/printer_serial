import cups
import time
import subprocess

# Fungsi untuk melakukan pencetakan dengan lp dan memeriksa status
def print_and_check_status():
    try:
        # Tentukan nama printer (ganti dengan nama printer Anda)
        printer_name = "EPSON_TM_U220B"

        # Perintah untuk mencetak menggunakan lp
        print_command = "echo 'Test print from Raspberry Pi\n\n\n' | lp -d {}".format(printer_name)
        
        # Jalankan perintah untuk mencetak
        subprocess.run(print_command, shell=True)

        # Tunggu sebentar agar CUPS memproses pekerjaan cetak
        time.sleep(5)  # Menunggu lebih lama agar printer memproses

        # Koneksi ke CUPS
        conn = cups.Connection()

        # Ambil daftar pekerjaan cetak yang sedang berjalan
        jobs = conn.getJobs()

        # Periksa apakah ada pekerjaan cetak yang berhasil
        if jobs:
            for job_id, job_info in jobs.items():
                print(f"Job ID: {job_id}, Status: {job_info['status']}")  # Debugging: menampilkan status pekerjaan
                if job_info["printer"] == printer_name and job_info["status"] == "completed":
                    return 1  # Pencetakan berhasil

        # Jika pekerjaan cetak tidak ditemukan atau tidak "completed"
        return 0  # Pencetakan gagal

    except Exception as e:
        # Jika ada kesalahan, kembalikan 0
        print(f"Error: {e}")  # Debugging: menampilkan error
        return 0

# Panggil fungsi untuk melakukan pencetakan dan pengecekan status
status = print_and_check_status()

# Tampilkan status hasil pencetakan
print(status)
