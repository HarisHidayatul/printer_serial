import serial
import time
import subprocess

# Fungsi untuk mengirimkan data ke printer menggunakan perintah 'lp'
def send_to_printer(data):
    try:
        # Menyaring data yang valid dan mengirimkan ke printer
        echo_command = f'echo -e "{data}" | lp -d EPSON_TM_U220B'
        print(f"Executing command: {echo_command}")  # Debug: Menampilkan perintah yang akan dijalankan
        process = subprocess.Popen(echo_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print("Data sent to printer successfully")
        else:
            print(f"Error while sending to printer: {stderr.decode()}")
    except Exception as e:
        print(f"Error while sending to printer: {e}")

# Fungsi untuk memonitor status printer
def monitor_printer_status():
    try:
        # Mengecek status printer dengan perintah lpstat
        result = subprocess.run(["lpstat", "-p", "EPSON_TM_U220B"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error checking printer status: {result.stderr}")
        else:
            print(f"Printer status: {result.stdout}")
    except Exception as e:
        print(f"Error while checking printer status: {e}")

# Fungsi utama untuk membuka serial port dan memproses data
def main():
    port_name = "/dev/ttyACM0"  # Ganti dengan port serial yang sesuai
    baud_rate = 9600  # Baud rate sesuai dengan pengaturan Arduino

    try:
        # Membuka koneksi serial ke Arduino
        arduino = serial.Serial(port_name, baud_rate, timeout=1)
        print(f"Connected to Arduino at {port_name}")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return

    last_data_received_time = time.time()

    while True:
        try:
            # Jika ada data yang tersedia di port serial
            if arduino.in_waiting > 0:
                data_from_arduino = arduino.readline().decode('ascii', errors='ignore').strip()
                print(f"Data received from Arduino: {data_from_arduino}")

                # Mengganti kata 'cut' dengan karakter newline jika ada
                modified_data = data_from_arduino.replace("cut", "\n")

                # Mengirim data ke printer
                send_to_printer(modified_data)

                # Memperbarui waktu terakhir data diterima
                last_data_received_time = time.time()
            else:
                # Jika tidak ada data yang diterima dalam 3 detik, cek status printer
                if time.time() - last_data_received_time >= 3:
                    monitor_printer_status()
                    last_data_received_time = time.time()

        except Exception as e:
            print(f"Error reading from serial port: {e}")
            break

        time.sleep(1)  # Tunggu sebentar sebelum membaca lagi

if __name__ == "__main__":
    main()
