from statistics import mean
import utils.dataReader as reader
from collections import Counter
from statistics import mean, median
import utils.aggregateAnalysis as aggregate

# TODO #9 Remove hardcoded input file and logger name and replace with argparse?
file = "maps.txt"
logger = "Akiva Cookiepouch"
data = reader.textParser(file, logger)
encounters = reader.encounterSplitter(data, logger)
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

# print("LOOT!")
sortedLoot = [(key, value) for key,value in Counter(loot).most_common()]

rolls = []
for encounter in encounters:
    for roll in encounter.rolls:
        rolls.append(int(roll.value))
# print("\nMEAN ROLL!")
# print(f'{mean(rolls):.2f}')
# print("\nMEDIAN ROLL!")
# print(median(rolls))
# print("\nMODE ROLL!")
rollCount = Counter(rolls)
maxRollCount = max(rollCount.values())
modeRolls = [roll[0] for roll in rollCount.items() if roll[1] == maxRollCount]
# print(modeRolls, maxRollCount)

greedrolls = []
for encounter in encounters:
    for roll in encounter.rolls:
        if roll.type == "GreedLoot":
            greedrolls.append(roll)
greedCount = Counter([roll.member.name for roll in greedrolls])
try:
    maxCount = max(greedCount.values())
except ValueError:
    maxCount = 0
greediestPlayers  = [key for key, value in greedCount.items() if value == maxCount]

needrolls = []
for encounter in encounters:
    for roll in encounter.rolls:
        if roll.type == "NeedLoot":
            needrolls.append(roll)
# print([(roll.member.name, roll.value) for roll in needrolls])
needCount = Counter([roll.member.name for roll in needrolls])
# print(needCount)
try:
    maxCount = max(needCount.values())
except ValueError:
    maxCount = 0
    noNeed = "\nNobody rolled need!"
neediestPlayers  = [key for key, value in needCount.items() if value == maxCount]

needWins = list(Counter([roll.member.name for roll in needrolls if roll.win]))

needRatios = aggregate.winRatios(members, needrolls)
greedRatios = aggregate.winRatios(members, greedrolls)

ratios = [item[2] for item in needRatios.values()]
try:
    maxRatio = max(ratios)
    minWins = min([item[0] for item in needRatios.values()])
    badNeeders = [(key,value) for key, value in needRatios.items() if value[0] == minWins]
    mostTries = max([value[1][2] for value in badNeeders])
    worstNeeders = [value for value in badNeeders if value[1][2] == mostTries]
    bestNeeders = [(key,value) for key, value in needRatios.items() if value[2] == maxRatio]
    # print("\nBEST NEEDER")
    # print(bestNeeders)

    # print("\nWORST NEEDER")
    # print(worstNeeders)
except ValueError:
    bestNeeders = "\nNobody rolled Need"


ratios = [item[2] for item in greedRatios.values()]
try:
    maxRatio = max(ratios)
    minWins = min([item[0] for item in greedRatios.values()])
    badGreeders = [(key,value) for key, value in greedRatios.items() if value[0] == minWins]
    mostTries = max([value[1][2] for value in badGreeders])
    worstGreeders = [value for value in badGreeders if value[1][2] == mostTries]
    bestGreeders = [(key,value) for key, value in greedRatios.items() if value[2] == maxRatio]
    # print("\nBEST GREEDER")
    # print(bestGreeders)

    # print("\nWORST GREEDER")
    # print(worstGreeders)
except ValueError:
    bestGreeders = "\nNobody rolled Greed"




outputHeader = """# FFXIV Loot Analyzer Report
## File: {}
## Logged By: {}
""".format(file, logger)

outputLoot ="""# Loot""" + ''.join('\n- {} {}'.format(*item) for item in sortedLoot)

outputMean = """\n# Mean Roll""" + ''.join('\n{:.2f}').format(mean(rolls))

outputMedian = """\n# Median Roll""" + ''.join('\n{:.2f}').format(median(rolls))

outputMode = """\n# Mode Rolls""" + ''.join('\n- {}'.format(roll) for roll in modeRolls) + """\n\nRolled {} times""".format(maxRollCount)

if type(bestNeeders) == str:
    outputBestNeeders = """\n # Best Greeders""" + bestNeeders
    outputWorstNeeders = """\n # Worst Greeders""" + bestNeeders
else:
    outputBestNeeders = """\n# Best Needers""" + ''.join('\n- {} {}'.format(*needer) for needer in bestNeeders)
    outputWorstNeeders = """\n# Worst Needers""" + ''.join('\n- {} {}'.format(*needer) for needer in worstNeeders)

if type(bestGreeders) == str:
    outputBestGreeders = """\n# Best Greeders""" + bestGreeders
    outputWorstGreeders = """\n# Worst Greeders""" + bestGreeders
else:
    outputBestGreeders = """\n# Best Greeders""" + ''.join('\n- {} {}'.format(*greeder) for greeder in bestGreeders)
    outputWorstGreeders = """\n# Worst Greeders""" + ''.join('\n- {} {}'.format(*greeder) for greeder in worstGreeders)

with open('output.md', 'w') as f:
    f.write(outputHeader + outputLoot + outputMean + outputMedian + outputMode + outputBestNeeders + outputWorstNeeders + outputBestGreeders + outputWorstGreeders)
    f.close()