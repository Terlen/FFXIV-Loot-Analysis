import csv
from typing import TextIO

def dataRead(file: TextIO) -> list:
    with open(file, newline='') as source:
        reader = csv.reader(source)
        data = [row for row in reader]
    return data