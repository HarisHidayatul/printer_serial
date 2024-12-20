import serial
import subprocess
import time
import cups

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
            print("Retrying in 3 seconds...")
            time.sleep(3)

def send_to_printer(data):
    """Mengirim data ke printer menggunakan CUPS."""
    try:
        # Gunakan subprocess untuk mencetak data
        command = f'echo -e "{data}" | lp -d {PRINTER_NAME}'
        subprocess.run(command, shell=True, check=True)
        print(f"Data sent to printer: {data}")
    except subprocess.CalledProcessError as e:
        print(f"Error sending data to printer: {e}")

def check_printer_status():
    """Memeriksa status printer menggunakan CUPS."""
    try:
        conn = cups.Connection()
        printer_status = conn.getPrinterAttributes(PRINTER_NAME)
        status = printer_status.get('printer-state', None)
        return status == 3  # Status 3 berarti printer offline
    except Exception as e:
        print(f"Error checking printer status: {e}")
        return False

def read_from_arduino(arduino):
    """Membaca data dari Arduino dan mencetaknya."""
    while True:
        try:
            if arduino.in_waiting > 0:
                # Membaca data dari Arduino
                data = arduino.readline().decode('ascii', errors='ignore').strip()
                print(f"Data received from Arduino: {data}")

                # Cek status printer sebelum mencetak
                if check_printer_status():
                    print("Printer is offline. Cannot print.")
                else:
                    send_to_printer(data)
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
            arduino = connect_to_arduino()  # Reconnect jika ada masalah

if __name__ == "__main__":
    arduino = connect_to_arduino()
    read_from_arduino(arduino)
