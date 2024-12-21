import cups

# Fungsi untuk memeriksa status pekerjaan cetak terakhir
def check_print_status():
    try:
        # Tentukan nama printer (ganti dengan nama printer Anda)
        printer_name = "EPSON_TM_U220B"

        # Koneksi ke CUPS
        conn = cups.Connection()

        # Ambil daftar pekerjaan cetak yang sedang berjalan atau sudah selesai
        jobs = conn.getJobs()

        # Jika ada pekerjaan yang terdaftar
        if jobs:
            # Mengambil pekerjaan terakhir yang tercatat
            last_job_id = list(jobs.keys())[-1]
            job_info = jobs[last_job_id]

            # Debugging status dan state pekerjaan
            print(f"Last Job ID: {last_job_id}, Status: {job_info.get('status', 'No Status')}, State: {job_info.get('state', 'No State')}")

            # Memeriksa apakah pekerjaan terakhir sudah selesai
            if job_info.get('state') == 'completed':
                print("Print Job Completed Successfully.")
                return 1  # Pencetakan berhasil
            else:
                print("Print Job Not Completed Yet.")
                return 0  # Pencetakan belum selesai atau gagal
        else:
            print("No print jobs found.")
            return 1

    except Exception as e:
        # Jika ada kesalahan, kembalikan 0
        print(f"Error: {e}")
        return 0

# Panggil fungsi untuk memeriksa status pekerjaan cetak terakhir
status = check_print_status()

# Tampilkan status hasil pengecekan
print(status)
