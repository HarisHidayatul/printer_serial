import os

def print_data(data):
    command = f'echo "{data}" | lp -d EPSON_TM_U220B'
    os.system(command)

# Test print
print_data("Test print from Raspberry Pi")