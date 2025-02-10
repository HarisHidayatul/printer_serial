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

        self.header_found = False
        self.tail_found = False
        self.data_temp = ""

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
    
    def process_string_data(self, charData):
        # print(charData)
        if self.header_found:
            self.data_temp += charData
            if charData == '#':
                self.tail_found: True
                if len(self.data_temp) == 17:
                    if self.verify_xor_checksum(self.data_temp):
                        self.isValidData = True
                        self.stringData = self.data_temp
                        self.deviceID = int(self.data_temp[1:3])  # Indeks 2 sampai 3
                        self.operationCode = int(self.data_temp[3:6])  # Indeks 4 sampai 6
                        self.index_data = int(self.data_temp[6:10])  # Indeks 7 sampai 10
                        self.data = self.data_temp[10:14]  # Indeks 11 sampai 14
                        self.process_convert_address()
                        # print(self.stringData)
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
                self.header_found = False
                self.tail_found = False
                self.data_temp = ""
        else:
            if charData == '@':
                self.header_found = True
                self.data_temp += charData
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