import serial
import subprocess
import time

# Fungsi untuk menghapus null byte
def remove_null_bytes(data):
    return data.replace('\x00', '')

# Fungsi untuk meng-escape karakter khusus di dalam data
def escape_shell_characters(data):
    # Mengganti karakter yang dapat menyebabkan masalah dalam shell
    special_chars = ['$', '`', '"', "'", '\\', '\n', '\r', '\t']
    for char in special_chars:
        data = data.replace(char, '\\' + char)  # Menambahkan escape sebelum karakter khusus
    return data

# Tentukan port serial Arduino
arduino_port = "/dev/ttyACM0"  # Sesuaikan dengan port yang digunakan oleh Arduino
baud_rate = 9600  # Sesuaikan dengan baud rate Arduino

# Membuka koneksi serial ke Arduino
try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Found Arduino at {arduino_port}")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# Membaca data dari Arduino
while True:
    try:
        if arduino.in_waiting > 0:
            data = arduino.read(arduino.in_waiting).decode('ascii', errors='ignore')  # Membaca data serial
            print(f"Data received from Arduino: {data}")

            # Menghapus null byte jika ada
            cleaned_data = remove_null_bytes(data)
            print(f"Cleaned data: {cleaned_data}")

            # Meng-escape karakter khusus sebelum mengirim ke printer
            escaped_data = escape_shell_characters(cleaned_data)
            print(f"Escaped data: {escaped_data}")

            # Mengirim data ke printer
            try:
                # Menyaring data yang valid dan mengirimkan ke printer
                echo_command = f"echo -e \"{escaped_data}\" | lp -d EPSON_TM_U220B"
                print(f"Executing command: {echo_command}")  # Debug: Menampilkan perintah yang akan dijalankan
                process = subprocess.Popen(echo_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()

                if process.returncode == 0:
                    print("Data sent to printer successfully")
                else:
                    print(f"Error while sending to printer: {stderr.decode()}")
            except Exception as e:
                print(f"Error while sending to printer: {e}")

    except Exception as e:
        print(f"Error reading data from Arduino: {e}")
        break

    time.sleep(1)  # Tunggu sebentar sebelum membaca lagi
