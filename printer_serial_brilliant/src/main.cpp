#include <Arduino.h>

#define INTERRUPT_PIN_0 2  // Interrupt 0 -> Pin 2
#define INTERRUPT_PIN_1 3  // Interrupt 1 -> Pin 3
#define INTERRUPT_PIN_2 21 // Interrupt 2 -> Pin 21

#define size_array_temp 255  // Maksimum 255 data untuk uint8_t
#define id_machine 0
#define send_arduino_id 0

volatile uint8_t data[size_array_temp][4];  // Buffer ukuran 255
volatile int16_t data_timer[size_array_temp];

volatile uint8_t temp_data_pinA = 0;
volatile uint8_t temp_data_pinC = 0;
volatile int16_t capture_timer = 0;

volatile uint8_t indexCaptureData = 0;
volatile uint8_t indexSendData = 0;

const char hex_char[16] = {'0', '1', '2', '3', '4', '5', '6', '7', 
  '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};

char send_data[16] = "";  // Perbesar buffer agar cukup menampung data

void captureData() {
  data[indexCaptureData][0] = PINA;
  data[indexCaptureData][1] = PINC;
  data[indexCaptureData][2] = indexCaptureData;
  data_timer[indexCaptureData] = capture_timer;
  indexCaptureData++;
}

void ISR_Interrupt0() { captureData(); }
void ISR_Interrupt1() { captureData(); }
void ISR_Interrupt2() { captureData(); }

// Fungsi untuk mengatur Timer1 dengan interval 100us
void setTimer1() {
  cli();  // Nonaktifkan interrupt sementara

  TCCR1A = 0;
  TCCR1B = (1 << WGM12) | (1 << CS11) | (1 << CS10);  // Mode CTC, Prescaler 64
  OCR1A = 24;  // 100µs
  TIMSK1 = (1 << OCIE1A);  // Aktifkan interrupt Timer1 Compare Match A

  sei();  // Aktifkan kembali interrupt
}

// ISR untuk Timer1
ISR(TIMER1_COMPA_vect) {
  ++capture_timer;
}

void setup() {
  Serial.begin(500000);
  DDRA = 0x00;  PORTA = 0xFF;  // Set PORTA sebagai input dengan pull-up
  DDRC = 0x00;  PORTC = 0xFF;  // Set PORTC sebagai input dengan pull-up

  setTimer1();  // Timer dengan interval 100us

  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN_0), ISR_Interrupt0, RISING);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN_1), ISR_Interrupt1, RISING);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN_2), ISR_Interrupt2, RISING);

  memset(send_data, 0, sizeof(send_data));
  memset(data, 0, sizeof(data));
  memset(data_timer, 0, sizeof(data_timer));
}

void loop() {
  if (indexSendData != indexCaptureData) {
    for (int i = 0; i < 3; i++) {
      send_data[0] = '@';
      send_data[1] = ((data[indexSendData][2] / 100) % 10) + '0';
      send_data[2] = ((data[indexSendData][2] / 10) % 10) + '0';
      send_data[3] = (data[indexSendData][2] % 10) + '0';

      send_data[4] = hex_char[(data[indexSendData][0] >> 4) & 0xF];
      send_data[5] = hex_char[data[indexSendData][0] & 0xF];
      send_data[6] = hex_char[(data[indexSendData][1] >> 4) & 0xF];
      send_data[7] = hex_char[data[indexSendData][1] & 0xF];

      // Kirim data_timer (int16_t) dalam format hex (4 karakter)
      int16_t timer_value = data_timer[indexSendData];

      send_data[8] = hex_char[(timer_value >> 12) & 0xF];
      send_data[9] = hex_char[(timer_value >> 8) & 0xF];
      send_data[10] = hex_char[(timer_value >> 4) & 0xF];
      send_data[11] = hex_char[timer_value & 0xF];

      // Hitung CRC sederhana (XOR semua karakter sebelumnya)
      uint8_t crc_hex = send_data[0];
      for (int j = 1; j <= 11; j++) {
        crc_hex ^= send_data[j];
      }

      send_data[12] = hex_char[(crc_hex >> 4) & 0xF];
      send_data[13] = hex_char[crc_hex & 0xF];

      send_data[14] = '#';

      Serial.write(send_data, 15);
      Serial.write('\n');
    }
    indexSendData++;
  }
}
