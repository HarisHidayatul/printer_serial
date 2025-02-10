import serial
import sys
import tkinter as tk
import threading
import time

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
        self.isEnter = False

    def process_convert_address(self):
        biner_data_PORTA = self.hex_to_binary(self.data[0:2])[::-1]  # Balik hasil biner dimulai dari 0 sampai 7
        biner_data_PORTC = self.hex_to_binary(self.data[2:4])[::-1]  # Balik hasil biner dimulai dari 0 sampai 7
        # print(biner_data_PORTA)
        # print(biner_data_PORTC)
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
                #  42,  // e menjadi a // PIN 12
                #  27,  // d menjadi b // PIN 7
                #  40,  // c menjadi c // PIN 11
                #  28,  // b menjadi d // PIN 8
                #  29   // a menjadi e // PIN 10
                self.address = loop_address
                a_data = biner_data_PORTC[7]
                b_data = biner_data_PORTA[6]
                c_data = biner_data_PORTC[6]
                d_data = biner_data_PORTA[7]
                e_data = biner_data_PORTC[5]
                self.abcde = a_data + b_data + c_data + d_data + e_data
                # print(self.abcde)
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
                            if self.process_convert_address():
                                # Ini untuk address yang telah terdefinisi
                                # return True
                                self.isEnter = False
                            else:
                                # Ini untuk address yang tidak terdefinisi
                                # Buat agar menjadi enter
                                # return False
                                self.isEnter = True
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
        # print(calculated_checksum)
    
        # Bandingkan hasil XOR yang dihitung dengan yang diberikan
        return calculated_checksum == given_checksum
class coordinate_generate:
    def __init__(self):
        self.data = [0] * 100
        self.temp_address = 0
        self.temp_abcde = "00000"
        self.isBegin = True
        self.spacePrint = 0
    # def print_data(self):

    def print_char_biner(self, char_print):
        for print_data in char_print:
            if int(print_data) == 0:
                print(' ',end='')
            else:
                print('X',end='')
            self.spacePrint = self.spacePrint + 1
            if self.spacePrint >= 5:
                self.spacePrint = 0
                print(' ',end='')

    def print_abcde(self, abcde):
        for loop_abcde in abcde:
            self.print_char_biner(loop_abcde)
            # print(loop_abcde, end='')
    def print_address(self, address, abcde):
        if self.isBegin:
            if address != 0:
                for i in range(0,5):
                    # print('0',end='')
                    self.print_abcde('0')
        for i in range(0, (int(address)-int(self.temp_address)-1)*5):  # 11 karena range tidak termasuk nilai stop
            # print('0', end='')
            self.print_char_biner('0')
        self.isBegin = False
        self.print_abcde(abcde)
        self.temp_address = int(address)
        self.temp_abcde = abcde
    def set_address(self, address, abcde, isEnter):
        # return abcde[2]
        # if int(address) > int(self.temp_address):
        if isEnter:
            if self.isBegin:
                for i in range(0,5):
                    # print('0',end='')
                    self.print_char_biner('0')
            for i in range(0,(19-int(self.temp_address))*5):
                # print('0', end='')
                self.print_char_biner('0')
            print("") # Lakukan print enter dan data temp hapus
            self.temp_address = 0
            self.temp_abcde = "00000"
            self.isBegin = True
        else:
            if address < self.temp_address:
                self.set_address(address=address,abcde=abcde, isEnter=True)
                self.set_address(address=address,abcde=abcde, isEnter=False)
            if (self.temp_address != address):
                self.print_address(address=address, abcde=abcde)
            else:
                if (self.isBegin):
                    self.print_address(address=address, abcde=abcde)
            
def main():
    coordinate = coordinate_generate()
    # coordinate.set_address(0,"01011",1)
    # coordinate.set_address(0,"01011",0)
    # coordinate.set_address(1,"00101",0)
    # coordinate.set_address(1,"00101",0)
    # coordinate.set_address(2,"00111",0)
    # coordinate.set_address(18,"00111",0)
    # coordinate.set_address(19,"00111",0)
    # coordinate.set_address(3,"00111",0)
    # array_1000x2 = [[0] * 2 for _ in range(1000)]
    # index_receive = 0
    # arduino = data_arduino()
    # if arduino.process_string_data("@000000913168074#"):
    #     array_1000x2[index_receive][0] = arduino.address
    #     array_1000x2[index_receive][1] = arduino.abcde
    #     index_receive = (index_receive + 1) % 1000
    # print(array_1000x2, index_receive)

    
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            print(f"Membuka port {PORT} dengan baudrate {BAUDRATE}")
            while True:
                try:
                    data = ser.readline().decode('utf-8').strip()
                    if data:
                        # print(f"Received: {data}")
                        arduino = data_arduino()
                        if arduino.process_string_data(data):
                            coordinate.set_address(arduino.address,arduino.abcde,arduino.isEnter)
                            # print(arduino.address,arduino.abcde)
                        # char_array = list(data)  # Pecah menjadi array karakter
                                                
                        # # Loop setiap karakter dalam array
                        # for char in char_array:
                            
                        #     print(f"{char}")

                except KeyboardInterrupt:
                    print("\nMenutup koneksi serial...")
                    break
    except serial.SerialException as e:
        print(f"Gagal membuka port: {e}")
        sys.exit(1)
    

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