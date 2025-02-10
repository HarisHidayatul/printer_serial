from package.open_close_file import open_close_file
from package.coordinate_generate import coordinate_generate

def main():    
    coordinate_raw = open_close_file("file_processing/coordinate_raw.csv")
    coordinate_translate = coordinate_generate()
    for read_coordinate in coordinate_raw.read_csv_file():
        address = read_coordinate[0]
        abcde = read_coordinate[1]
        isEnter = read_coordinate[2].strip().lower() == "true"
        coordinate_translate.set_address(int(address),abcde,bool(isEnter))
    for loop_3d in coordinate_translate.data_coordinate_generate():
        for loop_2d in coordinate_translate.data_coordinate_generate():
            for loop_char in loop_2d:
                print(loop_char,end='')
            print()
        print()
    # print(coordinate_translate.data_coordinate_generate())
if __name__ == "__main__":
    main()