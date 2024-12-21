import serial

def print_receipt():
    try:
        # Hubungkan ke printer
        printer = serial.Serial('/dev/usb/lp0', baudrate=9600, timeout=1)

        # ESC/POS Commands
        printer.write(b'\x1b\x40')  # Initialize printer
        printer.write(b'Hello, this is a test print!\n')
        printer.write(b'\n\n\n')  # Line feeds for spacing
        printer.close()

        print("Print successful!")
    except Exception as e:
        print(f"Error: {e}")

print_receipt()
