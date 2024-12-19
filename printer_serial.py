import serial
import time
import os

# Tentukan port serial yang digunakan untuk Arduino (sesuaikan dengan port yang digunakan Raspberry Pi)
port_name = "/dev/ttyACM0"  # Ganti dengan port serial yang sesuai
baud_rate = 9600  # Baud rate yang digunakan pada Arduino

def read_from_arduino():
    try:
        # Membuka koneksi serial dengan Arduino
        arduino = serial.Serial(port_name, baud_rate, timeout=1)
        print(f"Connected to Arduino at {port_name}")

        while True:
            # Cek jika ada data yang tersedia dari Arduino
            if arduino.in_waiting > 0:
                data_from_arduino = arduino.read(arduino.in_waiting)  # Baca semua data yang ada
                decoded_data = data_from_arduino.decode('ascii', errors='ignore')  # Decode menjadi string ASCII
                print(f"Data received from Arduino: {decoded_data}")

                # Kirim data ke printer
                command = f'echo "{decoded_data}" | lp -d EPSON_TM_U220B'
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

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_from_arduino()
