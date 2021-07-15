import csv
from typing import Iterable, TextIO
from collections import Counter

def dataRead(file: TextIO) -> list:
    with open(file, newline='') as source:
        reader = csv.reader(source)
        data = [[row[1],row[2],row[3],row[4],row[6]] for row in reader]
    return data

def dataPrint(data: Iterable) -> None:
    for row in data:
        for index,item in enumerate(row):
            if item == '':
                row[index] = 'None'
                
        print(f'Time:{row[0]:25}Action:{row[1]:25}Member:{row[2]:25}Item:{row[3]:25}Roll:{row[4]:25}')

def encounterSplitter(data: Iterable) -> list:
    output = []
    newEncounter = True
    for row in data:
        if (newEncounter and row[2] == "ObtainLoot" and row[3] == "Your Character"):
            newEncounter = False
            encounter = []
            encounter.append(row)
            addedLoot = list()
            # Loot obtained without an AddLoot is personal loot and should be not be considered to be obtainedLoot
            obtainedLoot = list()
        elif (newEncounter and row[2] == "AddLoot" and row[3] == ''):
            newEncounter = False
            encounter = []
            encounter.append(row)
            addedLoot = list(row[4])
            obtainedLoot = list()
        elif (not newEncounter and row[2] == "AddLoot" and row[3] == ''):
            addedLoot.append(row[4])
            encounter.append(row)
        elif (not newEncounter and row[2] == "ObtainLoot" and len(addedLoot) > 0):
            obtainedLoot.append(row[4])
            encounter.append(row)
            if len(Counter(obtainedLoot) - Counter(addedLoot)) == 0:
                newEncounter = True
                output.append(encounter)
        else:
            encounter.append(row)
    return output

