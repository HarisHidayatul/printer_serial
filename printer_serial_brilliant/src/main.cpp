#include <Arduino.h>
#define INTERRUPT_PIN 2
#define size_array_temp 1000

#define id_machine 0

// ID Operation Machine
#define send_arduino_id 0

uint8_t data[2][size_array_temp];
volatile bool captureData = false;
unsigned int indexCaptureData = 0;
unsigned int indexSendData = 0;

const char hex_char[16] = {
  '0',
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9',
  'A',
  'B',
  'C',
  'D',
  'E',
  'F'
};

char send_data[17] = "";

void interruptHandler() {
  captureData = true;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(500000);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), interruptHandler, RISING);
  for(int i=0;i<size_array_temp;i++){
    for(int j=0;j<2;j++){
      data[j][i] = 0x00;
    }
  }
  for(int i =0;i<17;i++){
    send_data[i] = NULL;
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if(captureData){
    while(digitalRead(INTERRUPT_PIN)){
      indexCaptureData++;
      indexCaptureData = indexCaptureData%1000; // Maksimum 1000 data
      data[0][indexCaptureData] = PINA;  // Capture PORTA
      data[1][indexCaptureData] = PINC;  // Capture PORTC
      delayMicroseconds(500);
    }
    captureData = false;
  }else{
    // Lakukan pengiriman data 
    if(indexCaptureData != indexSendData)
    {
      for(int i=0;i<17;i++){
        send_data[i] = NULL;
      }
      send_data[0] = '@';
      
      // Masukkan kode machine
      send_data[1] = ((id_machine/10)%10)+48;
      send_data[2] = (id_machine%10)+48;

      // Masukkan kode operasi
      send_data[3] = ((send_arduino_id/100)%10)+48;
      send_data[4] = ((send_arduino_id/10)%10)+48;
      send_data[5] = ((send_arduino_id)%10)+48;
      
      // Kirim data index ke berapa
      send_data[6] = ((indexSendData/1000)%10)+48;
      send_data[7] = ((indexSendData/100)%10)+48;
      send_data[8] = ((indexSendData/10)%10)+48;
      send_data[9] = ((indexSendData)%10)+48;

      // Kirim data dengan PINA dulu kemudian PINC
      send_data[10] = hex_char[(data[0][indexSendData]/16)%16];
      send_data[11] = hex_char[data[0][indexSendData]%16];

      send_data[12] = hex_char[(data[1][indexSendData]/16)%16];
      send_data[13] = hex_char[data[1][indexSendData]%16];

      // Hitung Hex CRC
      uint8_t crc_hex = send_data[0];
      for(int i =1;i<=13;i++){
        crc_hex = crc_hex ^ send_data[i];
      }
      send_data[14] = hex_char[(crc_hex/16)%16];
      send_data[15] = hex_char[crc_hex%16];

      send_data[16] = '#';

      for(int i =0;i<17;i++){
        Serial.write(send_data[i]);
      }
      Serial.write('\n');

      data[0][indexSendData] = 0x00;
      data[1][indexSendData] = 0x00;
      indexSendData++;
      indexSendData = indexSendData%1000;
    }
  }
}