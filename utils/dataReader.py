import csv
from typing import Iterable, TextIO
from collections import Counter
from utils.encounter import Encounter

def dataRead(file: TextIO) -> list:
    with open(file, newline='') as source:
        reader = csv.reader(source)
        data = [[row[1],row[2],row[3],row[4],row[6],row[5]] for row in reader]
    return data

def dataPrint(data: Iterable) -> None:
    for row in data:
        for index,item in enumerate(row):
            if item == '':
                row[index] = 'None'
                
        print(f'Time:{row[0]:25}Action:{row[1]:25}Member:{row[2]:25}Item:{row[3]:25}Roll:{row[4]:25}Quantity:{row[5]:25}')

def encounterSplitter(data: Iterable) -> list:
    output = []
    newEncounter = True
    for row in data:
        if (newEncounter and row[1] == "ObtainLoot" and row[2] == "Your Character"):
            newEncounter = False
            encounterData = []
            encounterData.append(row)
            addedLoot = list()
            # Loot obtained without an AddLoot is personal loot and should be not be considered to be obtainedLoot
            obtainedLoot = list()
            continue
        elif (newEncounter and row[1] == "AddLoot" and row[2] == ''):
            newEncounter = False
            encounterData = []
            encounterData.append(row)
            addedLoot = list()
            addedLoot.append(row[3])
            obtainedLoot = list()
            continue

        if (not newEncounter and row[1] == "AddLoot" and row[2] == ''):
            addedLoot.append(row[3])
            encounterData.append(row)
        elif (not newEncounter and row[1] == "ObtainLoot" and len(addedLoot) > 0):
            obtainedLoot.append(row[3])
            encounterData.append(row)
            if len(Counter(addedLoot) - Counter(obtainedLoot)) == 0:
                newEncounter = True
                output.append(Encounter(encounterData))
        elif (not newEncounter):
            encounterData.append(row)
        else:
            continue
        
    return output

