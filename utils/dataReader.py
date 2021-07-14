import csv
from typing import Iterable, TextIO

def dataRead(file: TextIO) -> list:
    with open(file, newline='') as source:
        reader = csv.reader(source)
        data = [[row[1],row[2],row[3],row[4],row[6]] for row in reader]
    return data

def dataPrint(data: Iterable) -> None:
    for item in data:
        print(f'Time:{item[0]}, Action:{item[1]}, Member:{item[2]}, Item:{item[3]}, Roll:{item[4]}')