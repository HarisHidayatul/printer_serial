import serial

# Ganti dengan port printer yang sesuai
printer_port = '/dev/usb/lp0'

# Membuka koneksi serial ke printer
with serial.Serial(printer_port, 9600) as printer:
    # ESC/POS command untuk memulai pencetakan
    printer.write(b'\x1B\x40')  # Reset printer
    printer.write(b'Hello, Printer!\n')  # Kirim teks ke printer
    printer.write(b'\x1D\x56\x41')  # Feed paper dan cut (perintah ESC/POS untuk potong kertas)
