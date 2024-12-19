import serial
import os
import time
from win32print import OpenPrinter, GetPrinter, PRINTER_STATUS, PRINTER_INFO_2

# Tentukan port serial yang digunakan untuk Arduino (sesuaikan dengan port yang digunakan Raspberry Pi)
port_name = "/dev/ttyACM0"  # Ganti dengan port serial yang sesuai
baud_rate = 9600  # Baud rate yang digunakan pada Arduino

# Nama printer yang digunakan
printer_name = "EPSON_TM_U220B"  # Ganti dengan nama printer yang sesuai

def check_printer_status(printer_name):
    try:
        # Buka printer
        printer = OpenPrinter(printer_name)
        printer_info = GetPrinter(printer, 2)  # Mendapatkan informasi printer
        status = printer_info[0][PRINTER_STATUS]
        
        # Menentukan apakah status printer mengindikasikan masalah
        has_problem = (status & (0x00000002 | 0x00000010 | 0x00000020 | 0x00000040)) != 0
        return has_problem
    except Exception as e:
        print(f"Error checking printer status: {e}")
        return False

def connect_to_arduino():
    while True:
        try:
            # Membuka koneksi serial dengan Arduino
            arduino = serial.Serial(port_name, baud_rate, timeout=1)
            print(f"Connected to Arduino at {port_name}")
            return arduino
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            print("Waiting for 3 seconds before retrying...")
            time.sleep(3)  # Tunggu 3 detik sebelum mencoba lagi

def connect_to_printer():
    while True:
        try:
            # Cek apakah printer terhubung
            printer_status = check_printer_status(printer_name)
            if not printer_status:
                print(f"Printer {printer_name} is connected.")
                return True
            else:
                print(f"Printer {printer_name} is disconnected. Waiting for 3 seconds...")
                time.sleep(3)  # Tunggu 3 detik sebelum mencoba lagi
        except Exception as e:
            print(f"Error checking printer status: {e}")
            time.sleep(3)  # Tunggu 3 detik sebelum mencoba lagi

def read_from_arduino():
    arduino = connect_to_arduino()  # Coba sambungkan ke Arduino
    while True:
        # Cek jika ada data yang tersedia dari Arduino
        if arduino.in_waiting > 0:
            data_from_arduino = arduino.read(arduino.in_waiting)  # Baca semua data yang ada
            decoded_data = data_from_arduino.decode('ascii', errors='ignore')  # Decode menjadi string ASCII
            print(f"Data received from Arduino: {decoded_data}")

            # Kirim data ke printer
            command = f'echo "{decoded_data}" | lp -d {printer_name}'
            print(f"Executing command: {command}")
            try:
                # Eksekusi perintah untuk mencetak ke printer
                result = os.system(command)
                if result == 0:
                    print("Data sent to printer successfully")
                else:
                    print("Error while sending to printer")
            except Exception as e:
                print(f"Error while sending to printer: {e}")

        # Cek status printer dan kirim ke Arduino
        printer_status = check_printer_status(printer_name)
        status_to_send = "1" if printer_status else "0"

        # Kirim status printer ke Arduino
        arduino.write(status_to_send.encode())
        print(f"Sent printer status to Arduino: {status_to_send}")

        # Cek jika Arduino terputus
        if not arduino.is_open:
            print("Arduino disconnected. Trying to reconnect...")
            arduino = connect_to_arduino()  # Sambungkan kembali ke Arduino

        # Cek status printer secara berkala
        if not check_printer_status(printer_name):
            print("Printer disconnected. Trying to reconnect...")
            connect_to_printer()  # Sambungkan kembali ke printer

if __name__ == "__main__":
    read_from_arduino()
