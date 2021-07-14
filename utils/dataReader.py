import csv
from typing import TextIO

def dataRead(file: TextIO) -> list:
    with open(file, newline='') as source:
        reader = csv.reader(source)
        data = [[row[1],row[2],row[3],row[4],row[6]] for row in reader]
    return data