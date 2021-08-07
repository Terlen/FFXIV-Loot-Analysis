import csv
from typing import Iterable, TextIO
from collections import Counter
from utils.encounter import Encounter

specialUnicodeChar = u"\ue0bb"
stringList = ["added to the loot list","casts his lot","casts her lot","cast your lot","You roll Greed","You roll Need","rolls Greed","rolls Need", "obtains", "You obtain"]

def logLineFilter(lines: list) -> list:
    filteredLog = []
    for line in lines:
        if any(substring in line for substring in stringList):
            filteredLog.append(line.rstrip())
    return filteredLog

def findCapitalLetters(string):
    return [index for index, character in enumerate(string) if character.isupper()]

def cleanItemName(line, lineFormat):
    print(line)
    if lineFormat == "AddLoot":
        startIndexofItemName = line.find(specialUnicodeChar)
        endIndexofItemName =line.find(" has")
        substring = line[startIndexofItemName+1:endIndexofItemName]
        firstCapitalIndex = findCapitalLetters(substring)[0]
        return substring[firstCapitalIndex:]
    elif lineFormat == "CastLoot" or lineFormat == "ObtainLoot":
        startIndexofItemName = line.find(specialUnicodeChar)
        if startIndexofItemName == -1:
            itemCapitalIndex = findCapitalLetters(line)
            print(itemCapitalIndex)
            # Handle case where item has no captial letters (gil, crafting materials)
            if itemCapitalIndex == [7]:
                reversedLine = line[::-1]
                indexOfObtain = reversedLine.find("niatbo")
                reversedSlice = reversedLine[:indexOfObtain]
                if reversedSlice[-1] == ' ':
                    indexOfItem = indexOfObtain -1
                    substring = line[len(line)-indexOfItem:]
                    if len(substring.split(' ')) == 2:
                        return substring.split(' ')[1]
                    else:
                        return substring
                elif reversedSlice[-1] == 's':
                    indexOfItem = indexOfObtain -2
                    substring = line[len(line)-indexOfItem:]
                    if len(substring.split(' ')) == 2:
                        return substring.split(' ')[1]
                    else:
                        return substring
            else:
                itemCapitalIndex = itemCapitalIndex[1]
                endIndexofItemName = -1
                substring = line[itemCapitalIndex: endIndexofItemName]
                return substring
        else:
            endIndexofItemName = -1
            substring = line[startIndexofItemName+1: endIndexofItemName]
            return substring
    elif lineFormat == "GreedLoot" or lineFormat == "NeedLoot":
        startIndexofItemName = line.find(specialUnicodeChar)
        reversedString = line[::-1]
        endIndexofItemName = len(line) - 1 - reversedString.find(".")

        substring = line[startIndexofItemName+1: endIndexofItemName]
        return substring

def getItemQuantity(line):
    if line.find(specialUnicodeChar) == -1:
        itemCapitalIndex = findCapitalLetters(line)
        if itemCapitalIndex == [7]:
            words = line.split(' ')
            return words[-2]
        else:
            substring = line[:itemCapitalIndex[1]-1]
            words = substring.split(' ')
            return words[-1]
    else:
        return "1"


def getRollValue(line):
    words = line.rstrip().split(" ")
    return words[-1][:-1]


def getCharacterName(line, lineFormat):
    if line.find("]") == -1:
        words = line.split(" ")
        return words[0] + " " + words[1]
    else:
        noTimestamp = line[line.find("]")+1:]
        words = noTimestamp.split(" ")
        return words[0] + " " + words[1]

def addLoot(data, itemName, index):
    lineType = "AddLoot"
    formattedLine = ["0:0:0", lineType, "", itemName, "0", "1"]
    data.insert(len(data), formattedLine)


def stringsToCSV(lines: list, logger: str, data : list) -> list:
    items = []
    for index,line in enumerate(lines):
        if stringList[0] in line:
            lineType = "AddLoot"
            itemName = cleanItemName(line, lineType)
            formattedLine = ["0:0:0", lineType, "", itemName, "1", "0"]
            items.append(itemName)
        elif stringList[1] in line or stringList[2] in line:
            lineType = "CastLoot"
            itemName = cleanItemName(line, lineType)
            if itemName in items:
                formattedLine = ["0:0:0", lineType, getCharacterName(line, lineType), itemName, "1", "0"]
            elif itemName not in items:
                addLoot(data, itemName, index)
                formattedLine = ["0:0:0", lineType, getCharacterName(line, lineType), itemName, "1", "0"]
                items.append(itemName)
                
        elif stringList[3] in line:
            lineType = "CastLoot"
            itemName = cleanItemName(line, lineType)
            if itemName in items:
                formattedLine = ["0:0:0", lineType, logger, itemName, "1", "0"]
            elif itemName not in items:
                addLoot(data, itemName, index)
                formattedLine = ["0:0:0", lineType, logger, itemName, "1", "0"]
                items.append(itemName)
        elif stringList[4] in line:
            lineType = "GreedLoot"
            formattedLine = ["0:0:0", lineType, logger, cleanItemName(line, lineType), "1", getRollValue(line)]
        elif stringList[5] in line:
            lineType = "NeedLoot"
            formattedLine = ["0:0:0", lineType, logger, cleanItemName(line, lineType), "1", getRollValue(line)]
        elif stringList[6] in line:
            lineType = "GreedLoot"
            formattedLine = ["0:0:0", lineType, getCharacterName(line, lineType), cleanItemName(line, lineType), "1", getRollValue(line)]
        elif stringList[7] in line:
            lineType = "NeedLoot"
            formattedLine = ["0:0:0", lineType, getCharacterName(line, lineType), cleanItemName(line, lineType), "1", getRollValue(line)]
        elif stringList[8] in line:
            lineType = "ObtainLoot"
            itemName = cleanItemName(line, lineType)
            formattedLine = ["0:0:0", lineType, getCharacterName(line, lineType), itemName, "1", "0"]
            if itemName in items:
                items.remove(itemName)

        elif stringList[9] in line:
            lineType = "ObtainLoot"
            itemName = cleanItemName(line, lineType)
            formattedLine = ["0:0:0", lineType, logger, itemName, getItemQuantity(line), "0"]
            if itemName in items:
                items.remove(itemName)
        yield formattedLine




def textParser(file: TextIO, logger: str) -> list:
    data = []
    with open(file, encoding= "utf-8",newline='') as source:
        lines = [line for line in source]
        filteredLines = logLineFilter(lines)
        for line in stringsToCSV(filteredLines, logger, data):
            # print(line)
            swapItemandQuantity = [line[0],line[1],line[2],line[3],line[5],line[4]] 
            data.append(swapItemandQuantity)
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

def encounterSplitter(data: Iterable, logger) -> list:
    output = []
    newEncounter = True
    for row in data:
        print(row)
        if (newEncounter and row[1] == "ObtainLoot" and row[2] == logger):
            newEncounter = False
            print("NEW ENCOUNTER")
            encounterData = []
            encounterData.append(row)
            addedLoot = list()
            castLoot = list()
            # Loot obtained without an AddLoot is personal loot and should be not be considered to be obtainedLoot
            obtainedRolledLoot = list()
            continue
        elif (newEncounter and row[1] == "AddLoot" and row[2] == ''):
            newEncounter = False
            encounterData = []
            encounterData.append(row)
            addedLoot = list()
            castLoot = list()
            addedLoot.append(row[3])
            obtainedRolledLoot = list()
            continue

        if (not newEncounter and row[1] == "AddLoot" and row[2] == ''):
            addedLoot.append(row[3])
            encounterData.append(row)
        elif (not newEncounter and row[1] == "CastLoot"):
            castLoot.append(row[3])
            encounterData.append(row)
        elif (not newEncounter and row[1] == "ObtainLoot" and len(addedLoot) > 0):
            # Catch possibility where logger leaves instance prematurely before loot is handed out
            if (row[2] == logger and (row[3] not in addedLoot and len(addedLoot) > 0)):
                newEncounter = False
                # print("NEW ENCOUNTER")
                encounterData = []
                encounterData.append(row)
                addedLoot = list()
                # Loot obtained without an AddLoot is personal loot and should be not be considered to be obtainedLoot
                obtainedRolledLoot = list()
                continue
            else:
                obtainedRolledLoot.append(row[3])
                # print(addedLoot, obtainedLoot)
                encounterData.append(row)
                if len(Counter(addedLoot) - Counter(obtainedRolledLoot)) <= 0:
                    print(addedLoot,obtainedRolledLoot)
                    newEncounter = True
                    output.append(Encounter(encounterData))
        
        # elif (not newEncounter and row[1] == "ObtainLoot" and ):
            

        elif (not newEncounter and (row[1] == "NeedLoot" or row[1] == "GreedLoot" or row[1] == "CastLoot")):
            # print("GREED OR NEED",row)
            encounterData.append(row)
        else:
            # print("CONTINUING")
            # print(row)
            continue
        
    return output

