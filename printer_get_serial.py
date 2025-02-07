import serial
import sys

# Konfigurasi port dan baudrate
PORT = "COM6"  # Ganti sesuai dengan port yang digunakan
BAUDRATE = 500000

class data_arduino:
    def __init__(self):
        self.isValidData = False
        self.deviceID = 0
        self.operationCode = 0
        self.index_data = 0
        self.data = 0
        
def main():
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            print(f"Membuka port {PORT} dengan baudrate {BAUDRATE}")
            while True:
                try:
                    data = ser.readline().decode('utf-8').strip()
                    if data:
                        print(f"Received: {data}")
                        char_array = list(data)  # Pecah menjadi array karakter
                                                
                        # Loop setiap karakter dalam array
                        for char in char_array:
                            
                            print(f"{char}")

                except KeyboardInterrupt:
                    print("\nMenutup koneksi serial...")
                    break
    except serial.SerialException as e:
        print(f"Gagal membuka port: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
