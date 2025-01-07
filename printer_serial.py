import serial
import subprocess
import shlex  # Untuk mengamankan argumen shell
import cups
import time

# Konfigurasi port serial
PORT_NAME = "/dev/ttyUSB0"  # Sesuaikan dengan port Arduino Anda
BAUD_RATE = 9600  # Sesuaikan dengan baud rate Arduino Anda

# Konfigurasi printer
PRINTER_NAME = "EPSON_TM_U220B"  # Sesuaikan dengan nama printer Anda

# Fungsi untuk mencoba terhubung ke Arduino melalui port serial
def connect_to_arduino():
    """Mencoba terhubung ke Arduino melalui port serial."""
    while True:
        try:
            arduino = serial.Serial(PORT_NAME, BAUD_RATE, timeout=1)
            print(f"Connected to Arduino at {PORT_NAME}")
            return arduino
        except serial.SerialException as e:
            print(f"Error connecting to Arduino: {e}")
            print("Retrying...")

# Fungsi untuk mengirim data ke printer
def send_to_printer(data):
    """Mengirim data langsung ke printer."""
    try:
        # Gunakan shlex.quote untuk menangani karakter khusus dengan aman
        safe_data = shlex.quote(data)
        command = f'echo {safe_data} | lp -d {PRINTER_NAME}'
        subprocess.run(command, shell=True, check=True)
        print(f"Data sent to printer: {data}")
    except subprocess.CalledProcessError as e:
        print(f"Error sending data to printer: {e}")

# Fungsi untuk memeriksa status pekerjaan cetak terakhir
def check_print_status():
    try:
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
                return 0  # Pencetakan berhasil
            else:
                print("Print Job Not Completed Yet.")
                return 1  # Pencetakan belum selesai atau gagal
        else:
            print("No print jobs found.")
            return 0

    except Exception as e:
        # Jika ada kesalahan, kembalikan 1
        print(f"Error: {e}")
        return 1

# Fungsi utama untuk membaca data dari Arduino dan memeriksa status printer
def main():
    """Membaca data dari Arduino dan mencetaknya ke printer, serta memeriksa status printer."""
    arduino = connect_to_arduino()
    last_received_time = time.monotonic()  # Waktu terakhir data diterima menggunakan monotonic
    check_interval = 3  # Interval dalam detik untuk memeriksa status printer

    while True:
        try:
            current_time = time.monotonic()  # Mendapatkan waktu saat ini

            # Cek jika ada data yang diterima dari Arduino
            if arduino.in_waiting > 0:
                # Membaca data dari Arduino
                data = arduino.readline().decode('ascii', errors='ignore').strip()
                print(f"Data received from Arduino: {data}")
                # Kirim data ke printer
                send_to_printer(data)
                last_received_time = current_time  # Update waktu terakhir data diterima

            # Cek status printer jika tidak ada data yang diterima dalam 3 detik
            if current_time - last_received_time > check_interval:
                print("No data received in the last 3 seconds. Checking printer status...")
                status = check_print_status()
                print(f"Printer status: {status}")

        except Exception as e:
            print(f"Error: {e}")
            arduino = connect_to_arduino()  # Reconnect jika ada masalah

if __name__ == "__main__":
    main()
