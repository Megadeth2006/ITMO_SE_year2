import ctypes
import os
import random


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]


def download_library():
    lib_name = "point_lib.so" ## захардкодил
    lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), lib_name)

    try:
        # Загрузка C-библиотеки
        c_lib = ctypes.CDLL(lib_path)
        print(f"Библиотека успешно загружена: {lib_path}")
    except Exception as e:
        print(f"Ошибка: не удалось загрузить библиотеку: {lib_path}")
        print(f"Детали ошибки: {e}")
        exit()


    c_lib.process.argtypes = (ctypes.POINTER(Point), ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    c_lib.process.restype = None
    return c_lib


if __name__ == "__main__":

    c_lib = download_library()

    f = open("points.txt", "w")
    arr_len = 1000 // 2  
    range_min = -1000
    range_max = 1000
    for i in range(arr_len):
        f.write(f"{random.randint(range_min, range_max)},{random.randint(range_min, range_max)} {random.randint(range_min, range_max)},{random.randint(range_min, range_max)}\n")
    f.close()

    
    data = []
    with open("points.txt", "r") as f:
        for line in f:
            x1, y1, x2, y2 = map(int, line.strip().replace(',', ' ').split())
            data.append(Point(x1, y1))
            data.append(Point(x2, y2))

    ArrayType = Point * len(data)  
    c_array = ArrayType(*data)  

    
    results = (ctypes.c_double * (len(c_array) // 2))() 
    c_lib.process(c_array, len(c_array), results)


    for i in range(0, arr_len * 2, 2):
        print(
            f"расстояние между точками ({c_array[i].x}, {c_array[i].y}) и ({c_array[i + 1].x}, {c_array[i + 1].y}) = {results[i // 2]}")
