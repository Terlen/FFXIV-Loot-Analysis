from statistics import mean
import utils.dataReader as reader
import utils.encounter
import utils.encounterAnalysis as analysis
from collections import Counter
from statistics import mean, median, multimode

# TODO #9 Remove hardcoded input file and logger name and replace with argparse?
data = reader.textParser("hades.txt", "Kame Ha")
encounters = reader.encounterSplitter(data, "Kame Ha")
encounters = [encounter for encounter in encounters]

members = []
for encounter in encounters:
    for member in encounter.members:
        members.append(member.name)
members = set(members)

loot = []
for encounter in encounters:
    for item in encounter.items:
        loot.append(item.name)

print("LOOT!")
for key,value in Counter(loot).most_common():
    print(key,value)

rolls = []
for encounter in encounters:
    for roll in encounter.rolls:
        rolls.append(int(roll.value))
print("\nMEAN ROLL!")
print(mean(rolls))
print("\nMEDIAN ROLL!")
print(median(rolls))
print("\nMODE ROLL!")
rollCount = Counter(rolls)
maxCount = max(rollCount.values())
modeRolls = [roll[0] for roll in rollCount.items() if roll[1] == maxCount]
print(modeRolls, maxCount)

greedrolls = []
for encounter in encounters:
    for roll in encounter.rolls:
        if roll.type == "GreedLoot":
            greedrolls.append(roll)
greedCount = Counter([roll.member.name for roll in greedrolls])
maxCount = max(greedCount.values())
greediestPlayers  = [key for key, value in greedCount.items() if value == maxCount]
# print("\nGREEDIEST!")
# print(greediestPlayers, maxCount)

needrolls = []
for encounter in encounters:
    for roll in encounter.rolls:
        if roll.type == "NeedLoot":
            needrolls.append(roll)
needCount = Counter([roll.member.name for roll in needrolls])
maxCount = max(needCount.values())
neediestPlayers  = [key for key, value in needCount.items() if value == maxCount]

needWins = list(Counter([roll.member.name for roll in needrolls if roll.win]))

memberNeedWinRatios = {}
for member in members:
    memberAttempts = [roll for roll in needrolls if roll.member.name == member]
    memberWins = [roll for roll in needrolls if roll.member.name == member and roll.win]
    try:
        winRatio = len(memberWins) / len(memberAttempts)
        memberNeedWinRatios[member] = (len(memberWins),len(memberAttempts),winRatio)
    except ZeroDivisionError:
        continue
    

ratios = [item[2] for item in memberNeedWinRatios.values()]
maxRatio = max(ratios)

minWins = min([item[0] for item in memberNeedWinRatios.values()])

badNeeders = [(key,value[0],value[1]) for key, value in memberNeedWinRatios.items() if value[0] == minWins]

mostTries = max([value[2] for value in badNeeders])

worstNeeders = [value for value in badNeeders if value[2] == mostTries]
bestNeeders = [(key,value) for key, value in memberNeedWinRatios.items() if value[2] == maxRatio]



print("\nBEST NEEDER")
print(bestNeeders)

print("\nWORST NEEDER")
print(worstNeeders)



# print("\nNEEDIEST!")
# print(neediestPlayers, maxCount)