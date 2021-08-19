import csv
from typing import Iterable, TextIO
from utils.encounter import Encounter

specialUnicodeChar = u"\ue0bb"
stringList = ["added to the loot list","casts his lot","casts her lot","cast your lot","You roll Greed","You roll Need","rolls Greed","rolls Need", "obtains", "You obtain"]

# Convert unicode char indicating HQ to 'HQ'
def translate_HQ(string, translation= u'HQ'):
    hqChar = u'\ue03c'
    translate_table = dict((ord(char), translation) for char in hqChar)
    return string.translate(translate_table)

def logLineFilter(lines: list) -> list:
    filteredLog = []
    for line in lines:
        if any(substring in line for substring in stringList):
            filteredLog.append(line.rstrip())
    return filteredLog

def findCapitalLetters(string):
    return [index for index, character in enumerate(string) if character.isupper()]

def cleanItemName(line, lineFormat):
    # print(line)
    if lineFormat == "AddLoot":
        startIndexofItemName = line.find(specialUnicodeChar)
        endIndexofItemName =line.find(" has")
        substring = line[startIndexofItemName+1:endIndexofItemName]
        firstCapitalIndex = findCapitalLetters(substring)[0]
        outputString = substring[firstCapitalIndex:]
    elif lineFormat == "CastLoot" or lineFormat == "ObtainLoot":
        startIndexofItemName = line.find(specialUnicodeChar)
        if startIndexofItemName == -1:
            itemCapitalIndex = findCapitalLetters(line)
            # print(itemCapitalIndex)
            # Handle case where item has no captial letters (gil, crafting materials)
            if itemCapitalIndex == [7]:
                reversedLine = line[::-1]
                indexOfObtain = reversedLine.find("niatbo")
                reversedSlice = reversedLine[:indexOfObtain]
                if reversedSlice[-1] == ' ':
                    indexOfItem = indexOfObtain -1
                    substring = line[len(line)-indexOfItem:]
                    if len(substring.split(' ')) == 2:
                        outputString = substring.split(' ')[1][:-1]
                    else:
                        outputString = substring
                elif reversedSlice[-1] == 's':
                    indexOfItem = indexOfObtain -2
                    substring = line[len(line)-indexOfItem:]
                    if len(substring.split(' ')) == 2:
                        outputString = substring.split(' ')[1][:-1]
                    else:
                        outputString = substring
            else:
                itemCapitalIndex = itemCapitalIndex[1]
                endIndexofItemName = -1
                substring = line[itemCapitalIndex: endIndexofItemName]
                outputString = substring
        else:
            endIndexofItemName = -1
            substring = line[startIndexofItemName+1: endIndexofItemName]
            outputString = substring
    elif lineFormat == "GreedLoot" or lineFormat == "NeedLoot":
        startIndexofItemName = line.find(specialUnicodeChar)
        reversedString = line[::-1]
        endIndexofItemName = len(line) - 1 - reversedString.find(".")

        substring = line[startIndexofItemName+1: endIndexofItemName]
        outputString = substring
    
    # Filter out additional item description IE: "pair of Cool Pants" should become "Cool Pants"
    # Probably not a perfect solution, may require more testing
    try:
        if outputString.split()[1] == 'of' and outputString[0].islower():
            outputString = outputString[outputString.index(' of ')+4:]
    except IndexError:
        pass
    return translate_HQ(outputString)

def getItemQuantity(line):
    itemCharacterIndex = line.find(specialUnicodeChar)
    if itemCharacterIndex == -1:
        itemCapitalIndex = findCapitalLetters(line)
        # If the only capital letter present is the first non-timestamp character (*Y*ou), quantity is penultimate word
        # EX: [18:06]You obtain 9,000 gil.
        if itemCapitalIndex == [7]:
            words = line.split(' ')
            return words[-2]
        else:
            substring = line[:itemCapitalIndex[1]-1]
            words = substring.split(' ')
            return words[-1]
    else:
        substring = line[:itemCharacterIndex -1]
        words = substring.split(' ')
        # if words[-1] is a number, return it. If it's not a number, just return 1.
        try:
            b = int(words[-1])
            return words[-1]
        except ValueError:
            return '1'


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
            formattedLine = ["0:0:0", lineType, getCharacterName(line, lineType), itemName, getItemQuantity(line), "0"]
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
    newEncounter = False
    startIndex = 0
    while True:
        if startIndex >= len(data)-1:
            break
        else:
            # print(startIndex)
            pass
        encounterData = []
        addedLoot = list()
        obtainedRolledLoot = list()
        for row in data[startIndex:]:
            # print(startIndex,row)
            # if (newEncounter and row[1] == "ObtainLoot" and row[2] == logger):
            #     newEncounter = False
            #     print("NEW ENCOUNTER")
            #     encounterData = []
            #     encounterData.append(row)
            #     addedLoot = list()
            #     castLoot = list()
            #     # Loot obtained without an AddLoot is personal loot and should be not be considered to be obtainedLoot
            #     obtainedRolledLoot = list()
            #     continue
            

            if (newEncounter):
                newEncounter = False
                encounterData = []
                encounterData.append(row)
                addedLoot = list()
                castLoot = list()
                # addedLoot.append(row[3])
                obtainedRolledLoot = list()
                startIndex += 1
                continue

            if (not newEncounter and row[1] == "AddLoot" and row[2] == '' and len(obtainedRolledLoot) == 0):
                addedLoot.append(row[3])
                encounterData.append(row)
            # If loot has started to be obtained from a roll, new loot shouldn't be getting added. This indicates there may be an error in the data collection
            elif (not newEncounter and row[1] == "AddLoot" and row[2] == '' and len(obtainedRolledLoot) > 0):
                # print(obtainedRolledLoot)
                print("POSSIBLE CORRUPT DATA, DROPPING ENCOUNTER")
                newEncounter == True
                break
            # elif (not newEncounter and row[1] == "CastLoot"):
            #     castLoot.append(row[3])
            #     encounterData.append(row)
            elif (not newEncounter and row[1] == "ObtainLoot"):
                # If the obtained loot is loot that was rolled on, note that
                if row[3] in addedLoot:
                    obtainedRolledLoot.append(row[3])
                    encounterData.append(row)
                # If obtained loot was given directly to player, it won't help determine if an encounter is resolved
                else:
                    encounterData.append(row)
                if len(addedLoot) > 0 and all(item in obtainedRolledLoot for item in addedLoot):
                    # print(addedLoot,obtainedRolledLoot)
                    newEncounter = True
                    # print("NEW ENCOUNTER")
                    output.append(Encounter(encounterData))
                    startIndex += 1
                    break
            
            # elif (not newEncounter and row[1] == "ObtainLoot" and ):
                

            elif (not newEncounter and (row[1] == "NeedLoot" or row[1] == "GreedLoot" or row[1] == "CastLoot")):
                # print("GREED OR NEED",row)
                encounterData.append(row)
            else:
                # print("CONTINUING")
                # print(row)
                continue
            startIndex += 1
            
    return output

