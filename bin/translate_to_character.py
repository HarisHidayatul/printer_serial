from package.open_close_file import open_close_file

coordinate_raw = open_close_file("file_processing/result_raw_data.txt")

enter_detect = False
data_detect = False
temp_data = []
for loop_row in coordinate_raw.read_txt_file_to_array():
    if enter_detect:
        if loop_row.strip() == "":
            if data_detect:
                break
            else:
                continue
        else:
            data_detect = True
            temp_data.append(loop_row)
    else:
        if loop_row.strip() == "":
            # print("Enter")
            enter_detect = True
for loop_data in temp_data:
    print(loop_data)

# List untuk menyimpan koordinat (x, y)
coordinates = []

# Baris terbawah menjadi y = 0
max_y = len(temp_data) - 1

for y, row in enumerate(reversed(temp_data)):  # Balik agar baris terbawah jadi y = 0
    for x, char in enumerate(row):
        if char == 'X':
            coordinates.append([x, y])  # Simpan koordinat (x, y)

# Output hasil
print(coordinates)

    # else:
        # print(loop_row)
# print(coordinate_raw.read_txt_file_to_array())