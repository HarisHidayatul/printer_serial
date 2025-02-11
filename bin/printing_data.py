from package.printer_control import printer_control

printing = printer_control(0x04b8, 0x0202)

byte_printer = [[0,0],[0,1],[150,2],[50,4],[7,2]]
printing.printing_byte(byte_printer)