import serial
import subprocess
import shlex  # Untuk mengamankan argumen shell

# Konfigurasi port serial
PORT_NAME = "/dev/ttyUSB0"  # Sesuaikan dengan port Arduino Anda
BAUD_RATE = 9600  # Sesuaikan dengan baud rate Arduino Anda

# Konfigurasi printer
PRINTER_NAME = "EPSON_TM_U220B"  # Sesuaikan dengan nama printer Anda

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

def main():
    """Membaca data dari Arduino dan mencetaknya ke printer."""
    arduino = connect_to_arduino()
    while True:
        try:
            if arduino.in_waiting > 0:
                # Membaca data dari Arduino
                data = arduino.readline().decode('ascii', errors='ignore').strip()
                print(f"Data received from Arduino: {data}")
                # Kirim data ke printer
                send_to_printer(data)
        except Exception as e:
            print(f"Error: {e}")
            arduino = connect_to_arduino()  # Reconnect jika ada masalah

if _name_ == "_main_":
    main()