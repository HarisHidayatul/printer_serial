import cups
import time

def remove_completed_jobs():
    try:
        # Koneksi ke CUPS
        conn = cups.Connection()

        # Ambil daftar pekerjaan cetak yang sedang berjalan atau sudah selesai
        jobs = conn.getJobs()

        # Jika ada pekerjaan yang terdaftar
        if jobs:
            for job_id, job_info in jobs.items():
                # Memeriksa apakah pekerjaan sudah selesai
                if job_info.get('state') == 'completed':
                    # Hapus pekerjaan yang sudah selesai
                    print(f"Removing completed job: {job_id}")
                    conn.cancelJob(job_id)
        else:
            print("No print jobs found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    remove_completed_jobs()
