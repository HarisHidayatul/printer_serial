#include <Arduino.h>

byte pwmPin = 2;          // Definisikan PIN yang digunakan untuk PWM
byte inputValue = 0;      // Variabel untuk menyimpan nilai input dari serial
String inputString = "";  // Variabel untuk menyimpan string input serial

byte pins_arduino[12] = {
  38,  //PIN 1  sebagai Addr IC3
  22,  //PIN 2  sebagai Addr IC2
  23,  //PIN 3  sebagai Addr IC1
  24,  //PIN 4  sebagai BIN3
  25,  //PIN 5  sebagai BIN2
  26,  //PIN 6  sebagai BIN1
  27,  //PIN 7  sebagai d
  28,  //PIN 8  sebagai b
  29,  //PIN 10 sebagai a
  40,  //PIN 11 sebagai c
  42   //PIN 12 sebagai e
};

byte dots_pin[5] = {
  // 29,  // a
  // 28,  // b
  // 40,  // c
  // 27,  // d
  // 42   // e

  // FLIP
  42,  // e menjadi a
  27,  // d menjadi b
  40,  // c menjadi c
  28,  // b menjadi d
  29   // a menjadi e
};
byte address_pin[6] = {
  38,  // Addr IC3
  22,  // Addr IC2
  23,  // Addr IC1
  24,  // BIN3
  25,  // BIN2
  26   // BIN1
};

// byte address[20][6] = {
//   // Address {ADDR IC3, Addr IC2, Addr IC1, BIN3, BIN2, BIN1}
//   // Address[0] -> Alamat 1
//   // Address[1] -> Alamat 2
//   // ....
//   // Address[19] -> Alamat 20
//   { 1, 1, 0, 0, 0, 1 },  // Alamat 1
//   { 1, 1, 0, 0, 1, 0 },  // Alamat 2
//   { 1, 1, 0, 0, 1, 1 },  // Alamat 3
//   { 1, 1, 0, 1, 0, 0 },  // Alamat 4
//   { 1, 1, 0, 1, 0, 1 },  // Alamat 5
//   { 1, 1, 0, 1, 1, 0 },  // Alamat 6
//   { 1, 1, 0, 1, 1, 1 },  // Alamat 7

//   { 1, 0, 1, 0, 0, 1 },  // Alamat 8
//   { 1, 0, 1, 0, 1, 0 },  // Alamat 9
//   { 1, 0, 1, 0, 1, 1 },  // Alamat 10
//   { 1, 0, 1, 1, 0, 0 },  // Alamat 11
//   { 1, 0, 1, 1, 0, 1 },  // Alamat 12
//   { 1, 0, 1, 1, 1, 0 },  // Alamat 13
//   { 1, 0, 1, 1, 1, 1 },  // Alamat 14

//   { 0, 1, 1, 0, 0, 1 },  // Alamat 15
//   { 0, 1, 1, 0, 1, 0 },  // Alamat 16
//   { 0, 1, 1, 0, 1, 1 },  // Alamat 17
//   { 0, 1, 1, 1, 0, 0 },  // Alamat 18
//   { 0, 1, 1, 1, 0, 1 },  // Alamat 19
//   { 0, 1, 1, 1, 1, 0 },  // Alamat 20
// };

byte address[20][6] = {
  // FLIP
  // Address {ADDR IC3, Addr IC2, Addr IC1, BIN3, BIN2, BIN1}
  { 0, 1, 1, 1, 1, 0 },  // Alamat 20
  { 0, 1, 1, 1, 0, 1 },  // Alamat 19
  { 0, 1, 1, 1, 0, 0 },  // Alamat 18
  { 0, 1, 1, 0, 1, 1 },  // Alamat 17
  { 0, 1, 1, 0, 1, 0 },  // Alamat 16
  { 0, 1, 1, 0, 0, 1 },  // Alamat 15
  { 1, 0, 1, 1, 1, 1 },  // Alamat 14
  { 1, 0, 1, 1, 1, 0 },  // Alamat 13
  { 1, 0, 1, 1, 0, 1 },  // Alamat 12
  { 1, 0, 1, 1, 0, 0 },  // Alamat 11
  { 1, 0, 1, 0, 1, 1 },  // Alamat 10
  { 1, 0, 1, 0, 1, 0 },  // Alamat 9
  { 1, 0, 1, 0, 0, 1 },  // Alamat 8
  { 1, 1, 0, 1, 1, 1 },  // Alamat 7
  { 1, 1, 0, 1, 1, 0 },  // Alamat 6
  { 1, 1, 0, 1, 0, 1 },  // Alamat 5
  { 1, 1, 0, 1, 0, 0 },  // Alamat 4
  { 1, 1, 0, 0, 1, 1 },  // Alamat 3
  { 1, 1, 0, 0, 1, 0 },  // Alamat 2
  { 1, 1, 0, 0, 0, 1 }   // Alamat 1
};


// Definisi karakter dalam bentuk array (little endian)
const uint8_t characters_number[][7] = {
  { 0b00001110,
    0b00010001,
    0b00010001,
    0b00010001,
    0b00010001,
    0b00010001,
    0b00001110 },  // 0
  { 0b00001100,
    0b00010100,
    0b00000100,
    0b00000100,
    0b00000100,
    0b00000100,
    0b00011111 },  // 1
  { 0b00001110,
    0b00010001,
    0b00000010,
    0b00000100,
    0b00001000,
    0b00010000,
    0b00011111 },  // 2
  { 0b00001110,
    0b00010001,
    0b00000001,
    0b00000011,
    0b00000001,
    0b00000001,
    0b00011110 },  // 3
  { 0b00000100,
    0b00001001,
    0b00010001,
    0b00011111,
    0b00000001,
    0b00000001,
    0b00000001 },  // 4
  { 0b00011111,
    0b00010000,
    0b00011110,
    0b00000001,
    0b00000001,
    0b00000001,
    0b00011110 },  // 5
  { 0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000 },  // 6
  { 0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000 },  // 7
  { 0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000 },  // 8
  { 0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000 }  // 9
};
void writeString(int *array_character, int size, int pwm_def, int delay_msec) {
  clearInput();
  analogWrite(pwmPin, pwm_def);
  delay(100);
  delay(delay_msec);
  int start_character = 0;
  for (int i = 0; i < 7; i++) {
    // Baris
    for (int j = 0; j < size; j++) {
      // Kolom berdasar baris
      for (int k = 0; k < 6; k++) {
        digitalWrite(address_pin[k], address[j][k]);
      }
      int l = 0;
      for (int k = 4; k >= 0; k--) {
        digitalWrite(dots_pin[l], bitRead(characters_number[array_character[j]][i], k));
        l++;
      }
      delay(delay_msec);
      // clearInput();
    }
  }
  delay(delay_msec);
  delay(delay_msec);
  analogWrite(pwmPin, 0);
  delay(100);
  clearInput();
}
void writeCoordinateABCDE(int col, byte hex_abcde) {
  // koordinate ini melakukan printing
  if (col < 20) {
    for (int i = 0; i < 6; i++) {
      digitalWrite(address_pin[i], address[col][i]);
    }
    int j = 0;
    for (int i = 4; i >= 0; i--) {
      if (bitRead(hex_abcde, i)) {
        Serial.print('1');
      } else {
        Serial.print('0');
      }
      Serial.print('(');
      Serial.print(dots_pin[j]);
      Serial.print(") ");
      digitalWrite(dots_pin[j], bitRead(hex_abcde, i));
      j++;
      // digitalWrite(dots_pin[i-2],bitRead(hex_abcde,i));
    }
  }
}
void writeCoordinate(int x) {
  // koordinate ini dimulai dari 0 sampai 99 sesuai dot pada printer
  int modX = x % 5;  // nilai modX mewakili dot abcde, jika a maka bernilai 0, b bernilai 1, c berilai 2, dst
  int divX = x / 5;  // nilai divX merupakan posisi address ( Alamat )
  if (divX < 20) {
    for (int i = 0; i < 6; i++) {
      digitalWrite(address_pin[i], address[divX][i]);
    }
    for (int j = 0; j < 5; j++) {
      if (j == modX) {
        digitalWrite(dots_pin[j], HIGH);
      } else {
        digitalWrite(dots_pin[j], LOW);
      }
    }
  }
}
void runPWM(int pwm_def) {
  analogWrite(pwmPin, pwm_def);
  for (int j = 0; j < 1; j++) {
    for (int i = 0; i < 100; i++) {
      writeCoordinate(i);
      delay(50);
    }
  }
  /*
  for (int i = 0; i < 20; i++) {
    for (int z = 0; z < 100; z++) {
      for (int j = 0; j < 6; j++) {
        // Mengatur Address
        digitalWrite(address_pin[j], address[i][j]);
      }
      for (int k = 0; k < 5; k++) {
        for (int l = 0; l < 5; l++) {
          if (k == l) {
            digitalWrite(dots_pin[k], HIGH);
          } else {
            digitalWrite(dots_pin[l], LOW);
          }
        }
        delay(1);
      }
    }
  }
  */

  analogWrite(pwmPin, 0);
}
void clearInput() {
  for (int i = 0; i < 12; i++) {
    digitalWrite(pins_arduino[i], LOW);
  }
}
void runCharacterNumber(int pwm_def) {
  analogWrite(pwmPin, pwm_def);
  int coordinate = 0;
  clearInput();
  delay(2000);
  for (int i = 0; i < 7; i++) {
    writeCoordinateABCDE(5, characters_number[0][i]);
    Serial.println();
    delay(20);
  }
  clearInput();
  delay(2000);
  analogWrite(pwmPin, 0);
}
void setup() {
  // Memulai komunikasi serial
  Serial.begin(9600);

  for (int i = 0; i < 12; i++) {
    pinMode(pins_arduino[i], OUTPUT);
  }
  for (int i = 0; i < 12; i++) {
    digitalWrite(pins_arduino[i], LOW);
  }

  // Set PIN 2 sebagai output
  pinMode(pwmPin, OUTPUT);

  // Menunggu input pertama
  Serial.println("Masukkan nilai PWM (0-255):");
}

void loop() {
  // Cek apakah ada data yang diterima lewat serial

  if (Serial.available() > 0) {
    // Menyimpan karakter input dalam inputString
    char receivedChar = Serial.read();

    /*
    static bool header_active = false;
    static int number_serial = 0;
    static int index = 0;

    if (header_active) {
      if (receivedChar == '#') {
        header_active = false;
        index = 0;
      } else {
        int receivedNumber = receivedChar - 48;
        if (receivedNumber > 0)
          number_serial = number_serial + receivedChar
      }
    } else {
      if (receivedChar == '@') {
        header_active = true;
        index = 0;
      }
    }
    */


    // Cek apakah karakter yang diterima adalah enter (newline)
    if (receivedChar == '\n' || receivedChar == '\r') {
      // Jika sudah selesai menerima input, konversi ke integer
      inputValue = inputString.toInt();

      // Pastikan nilai input antara 0 dan 255
      if (inputValue > 0 && inputValue <= 255) {
        // Mengubah nilai PWM pada pin 2
        //analogWrite(pwmPin, inputValue);
        // Menampilkan nilai PWM yang diterapkan
        Serial.print("PWM di PIN 2 diubah ke: ");
        Serial.println(inputValue);
        // runPWM(inputValue);
        // runCharacterNumber(inputValue);
        int print_char[] = { 0, 1, 2, 3, 4 };
        writeString(print_char, 5, inputValue, 10);


        // Kosongkan inputString untuk input selanjutnya
        inputString = "";
        Serial.println("Masukkan nilai PWM (0-255):");
      } else {
        // Jika nilai input tidak valid
        //Serial.println("Nilai harus antara 0 dan 255.");
      }
    } else {
      // Menambahkan karakter yang diterima ke inputString
      inputString += receivedChar;
    }
  }
}