import csv
from typing import Iterable, TextIO
from collections import Counter
from utils.encounter import Encounter

specialUnicodeChar = u'\ue0bb'
stringList = ["added to the loot list","casts his lot","casts her lot","cast your lot","You roll Greed","You roll Need","rolls Greed","rolls Need", "obtains", "You obtain"]

def logLineFilter(lines: list) -> list:
    filteredLog = []
    for line in lines:
        if any(substring in line for substring in stringList):
            filteredLog.append(line)
    return filteredLog

def findCapitalLetters(string):
    return [index for index, character in enumerate(string) if character.isupper()]

def cleanItemName(line, lineFormat):
    if lineFormat == "AddLoot":
        startIndexofItemName = line.find(specialUnicodeChar)
        endIndexofItemName =line.find(" has")
        substring = line[startIndexofItemName+1:endIndexofItemName]
        firstCapitalIndex = findCapitalLetters(substring)[0]
        return substring[firstCapitalIndex:]
    elif lineFormat == 'CastLoot' or lineFormat == "ObtainLoot":
        startIndexofItemName = line.find(specialUnicodeChar)
        if startIndexofItemName == -1:
            itemCapitalIndex = findCapitalLetters(line)[1]
            endIndexofItemName = line.find(".")
            substring = line[itemCapitalIndex: endIndexofItemName]
            return substring
        endIndexofItemName = line.find(".")
        substring = line[startIndexofItemName+1: endIndexofItemName]
        firstCapitalIndex = findCapitalLetters(substring)[0]
        return substring[firstCapitalIndex:]
    elif lineFormat == "GreedLoot" or lineFormat == "NeedLoot":
        startIndexofItemName = line.find(specialUnicodeChar)
        endIndexofItemName = line.find(".")
        substring = line[startIndexofItemName+1: endIndexofItemName]
        firstCapitalIndex = findCapitalLetters(substring)[0]
        return substring[firstCapitalIndex:]

def getItemQuantity(line):
    if line.find(specialUnicodeChar) == -1:
        itemCapitalIndex = findCapitalLetters(line)[1]
        substring = line[:itemCapitalIndex-1]
        words = substring.split(' ')
        return words[-1]
    else:
        return '1'


def getRollValue(line):
    words = line.rstrip().split(" ")
    return words[-1][:-1]


def getCharacterName(line, lineFormat):
    words = line.split(" ")
    return words[0] + " " + words[1]


def stringsToCSV(lines: list, logger: str) -> list:
    for line in lines:
        if stringList[0] in line:
            lineType = "AddLoot"
            formattedLine = ["0:0:0", lineType, "", cleanItemName(line, lineType), '1', '0']
        elif stringList[1] in line or stringList[2] in line:
            lineType = "CastLoot"
            formattedLine = ["0:0:0", lineType, getCharacterName(line, lineType), cleanItemName(line, lineType), '1', '0']
        elif stringList[3] in line:
            lineType = "CastLoot"
            formattedLine = ["0:0:0", lineType, logger, cleanItemName(line, lineType), '1', '0']
        elif stringList[4] in line:
            lineType = "GreedLoot"
            formattedLine = ["0:0:0", lineType, logger, cleanItemName(line, lineType), '1', getRollValue(line)]
        elif stringList[5] in line:
            lineType = "NeedLoot"
            formattedLine = ["0:0:0", lineType, logger, cleanItemName(line, lineType), '1', getRollValue(line)]
        elif stringList[6] in line:
            lineType = "GreedLoot"
            formattedLine = ["0:0:0", lineType, getCharacterName(line, lineType), cleanItemName(line, lineType), '1', getRollValue(line)]
        elif stringList[7] in line:
            lineType = "NeedLoot"
            formattedLine = ["0:0:0", lineType, getCharacterName(line, lineType), cleanItemName(line, lineType), '1', getRollValue(line)]
        elif stringList[8] in line:
            lineType = "ObtainLoot"
            formattedLine = ["0:0:0", lineType, getCharacterName(line, lineType), cleanItemName(line, lineType), '1', '0']
        elif stringList[9] in line:
            lineType = "ObtainLoot"
            formattedLine = ["0:0:0", lineType, logger, cleanItemName(line, lineType), getItemQuantity(line), '0']
        yield formattedLine




def textParser(file: TextIO, logger: str) -> list:
    data = []
    with open(file, encoding= "utf-8",newline='') as source:
        lines = [line for line in source]
        filteredLines = logLineFilter(lines)
        for line in stringsToCSV(filteredLines, logger):
            data.append(line)
    return data



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

