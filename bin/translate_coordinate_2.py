from package.open_close_file import open_close_file
from package.coordinate_generate_2 import coordinate_generate_2

def main():
    coordinate_raw = open_close_file("file_processing/coordinate_raw.csv")
    coordinate_generate = coordinate_generate_2()
    for read_coordinate in coordinate_raw.read_csv_file():
        address = read_coordinate[0]
        abcde = read_coordinate[1]
        timer = read_coordinate[2]
        coordinate_generate.set_address(address,abcde,timer)    
    # print(coordinate_translate.data_coordinate_generate())
    coordinate_generate.set_address("0","00000","99999")    
if __name__ == "__main__":
    main()