import serial
import time
import subprocess

# Fungsi untuk menghapus null byte dari data
def remove_null_bytes(data):
    return data.replace('\0', '')

# Fungsi untuk meng-escape karakter khusus di dalam data
def escape_shell_characters(data):
    # Mengganti karakter yang dapat menyebabkan masalah dalam shell
    special_chars = ['$', '`', '"', "'", '\\']
    for char in special_chars:
        data = data.replace(char, '\\' + char)  # Menambahkan escape sebelum karakter khusus
    return data

# Tentukan port serial Arduino
arduino_port = "/dev/ttyACM0"
baud_rate = 9600

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
                subprocess.run(echo_command, shell=True, check=True)
                print("Data sent to printer successfully")
            except Exception as e:
                print(f"Error while sending to printer: {e}")

    except Exception as e:
        print(f"Error reading data from Arduino: {e}")
        break

    time.sleep(1)  # Tunggu sebentar sebelum membaca lagi
