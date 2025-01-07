import subprocess
import os

# Konfigurasi nama printer
PRINTER_NAME = "EPSON_TM_U220B"  # Sesuaikan dengan nama printer Anda

# Fungsi untuk mengirim data bitmap langsung ke printer
def print_bitmap():
    """Mengirim data bitmap langsung ke printer Epson TM-U220B."""
    try:
        # Perintah ESC/POS untuk mencetak bitmap raster
        # ESC * m nL nH d1...dk
        esc_pos_command = b'\x1B*\x00\x07\x00'  # Mode 8-dot, 7 bytes (50 dots horizontal)
        
        # Bitmap untuk 50 dots horizontal (7 bytes)
        bitmap_data = [
            0b11111111,  # Byte 1: 8 dots hitam
            0b11111111,  # Byte 2: 8 dots hitam
            0b11111111,  # Byte 3: 8 dots hitam
            0b11111111,  # Byte 4: 8 dots hitam
            0b11111111,  # Byte 5: 8 dots hitam
            0b11111111,  # Byte 6: 8 dots hitam
            0b11000000,  # Byte 7: 2 dots hitam, 6 dots putih
        ]

        # Gabungkan perintah ESC/POS dan data bitmap
        data_to_send = esc_pos_command + bytes(bitmap_data)

        # Buat file sementara untuk menyimpan data bitmap
        temp_file_path = "/tmp/bitmap_print_data.bin"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(data_to_send)

        # Kirim data ke printer menggunakan lp
        command = f'lp -d {PRINTER_NAME} {temp_file_path}'
        subprocess.run(command, shell=True, check=True)

        # Hapus file sementara
        os.remove(temp_file_path)

        print("Bitmap data sent to printer.")

    except subprocess.CalledProcessError as e:
        print(f"Error sending bitmap data to printer: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Panggil fungsi untuk mencetak bitmap
if __name__ == "__main__":
    print_bitmap()
