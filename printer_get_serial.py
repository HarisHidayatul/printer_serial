import serial
import sys

# Konfigurasi port dan baudrate
PORT = "COM6"  # Ganti sesuai dengan port yang digunakan
BAUDRATE = 500000

class data_arduino:
    ADDRESS = (
        # FLIP
        # Address {ADDR IC3, Addr IC2, Addr IC1, BIN3, BIN2, BIN1}
        (0, 1, 1, 1, 1, 0),  # Alamat 20
        (0, 1, 1, 1, 0, 1),  # Alamat 19
        (0, 1, 1, 1, 0, 0),  # Alamat 18
        (0, 1, 1, 0, 1, 1),  # Alamat 17
        (0, 1, 1, 0, 1, 0),  # Alamat 16
        (0, 1, 1, 0, 0, 1),  # Alamat 15
        (1, 0, 1, 1, 1, 1),  # Alamat 14
        (1, 0, 1, 1, 1, 0),  # Alamat 13
        (1, 0, 1, 1, 0, 1),  # Alamat 12
        (1, 0, 1, 1, 0, 0),  # Alamat 11
        (1, 0, 1, 0, 1, 1),  # Alamat 10
        (1, 0, 1, 0, 1, 0),  # Alamat 9
        (1, 0, 1, 0, 0, 1),  # Alamat 8
        (1, 1, 0, 1, 1, 1),  # Alamat 7
        (1, 1, 0, 1, 1, 0),  # Alamat 6
        (1, 1, 0, 1, 0, 1),  # Alamat 5
        (1, 1, 0, 1, 0, 0),  # Alamat 4
        (1, 1, 0, 0, 1, 1),  # Alamat 3
        (1, 1, 0, 0, 1, 0),  # Alamat 2
        (1, 1, 0, 0, 0, 1),  # Alamat 1
    )

    def __init__(self):
        self.isValidData = False
        self.deviceID = 0
        self.operationCode = 0
        self.index_data = 0
        self.data = "" #data berbentuk hex
        self.stringData = ""
        self.address = 0
        self.abcde = "00000"

    def process_convert_address(self):
        biner_data_PORTA = self.hex_to_binary(self.data[0:2])[::-1]  # Balik hasil biner
        biner_data_PORTC = self.hex_to_binary(self.data[2:4])[::-1]  # Balik hasil biner
        print(biner_data_PORTA)
        print(biner_data_PORTC)
        address_found = True
        index_address_found = 0
        for loop_address in range(20):
            address_found = True
            for index_biner_address in range(6):
                if int(self.ADDRESS[loop_address][index_biner_address]) == int(biner_data_PORTA[index_biner_address]):
                    address_found = address_found & True
                else:
                    address_found = address_found & False
            if address_found:
                self.address = loop_address
                a_data = 
                b_data = 
                c_data = 
                d_data = 
                e_data = 
                break
        if address_found:
            return True
        return False
    def hex_to_binary(self,hex_string):
        return ''.join(f"{int(char, 16):04b}" for char in hex_string.upper())
    
    def process_string_data(self, stringData):
        header_found = False
        tail_found = False
        data_temp = ""
        for data in stringData:
            if header_found:
                data_temp += data
                if data == '#':
                    tail_found: True
                    if len(data_temp) == 17:
                        if self.verify_xor_checksum(data_temp):
                            self.isValidData = True
                            self.stringData = data_temp
                            self.deviceID = int(data_temp[1:3])  # Indeks 2 sampai 3
                            self.operationCode = int(data_temp[3:6])  # Indeks 4 sampai 6
                            self.index_data = int(data_temp[6:10])  # Indeks 7 sampai 10
                            self.data = data_temp[10:14]  # Indeks 11 sampai 14
                            self.process_convert_address()
                            return True
                        else:
                            return False
            else:
                if data == '@':
                    header_found = True
                    data_temp += data
        return False
    def verify_xor_checksum(self,data):
        # Pastikan format data sesuai
        if not (data.startswith('@') and data.endswith('#') and len(data) > 3):
            return False

        # Pisahkan payload dan checksum
        payload = data[0:-3]  # Mengambil bagian antara @ dan checksum
        given_checksum = data[-3:-1]  # Ambil checksum yang diberikan (dua karakter sebelum '#')
    
        # print(given_checksum)
        # Hitung XOR dari semua karakter payload
        xor_result = 0
        for char in payload:
            xor_result ^= ord(char)  # XOR dengan nilai ASCII masing-masing karakter

        # Konversi hasil XOR ke bentuk hex (uppercase untuk dibandingkan)
        calculated_checksum = f"{xor_result:02X}"
        print(calculated_checksum)
    
        # Bandingkan hasil XOR yang dihitung dengan yang diberikan
        return calculated_checksum == given_checksum

    
def main():
    arduino = data_arduino()
    print(arduino.process_string_data("@000000913168074#"))
    """
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
    """

if __name__ == "__main__":
    main()

"""
@00000090816807E#
@00000090916807F#
@000000910168077#
@000000911168076#
@000000912168075#
@000000913168074#
"""