from statistics import mean
import utils.dataReader as reader
from collections import Counter
from statistics import mean, median
import utils.aggregateAnalysis as aggregate
import matplotlib.pyplot as plt
from matplotlib import ticker
from collections import defaultdict

# TODO #9 Remove hardcoded input file and logger name and replace with argparse?
file = "maps.txt"
logger = "Akiva Cookiepouch"
data = reader.textParser(file, logger)
encounters = reader.encounterSplitter(data, logger)
encounters = [encounter for encounter in encounters]
outputFolder = 'output/'
rollGraphFile = 'rolldistribution.png'


members = []
for encounter in encounters:
    for member in encounter.members:
        members.append(member.name)
uniqueMembers = set(members)

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
meanRolls = mean(rolls)
medianRolls = median(rolls)
modeRolls = [roll[0] for roll in rollCount.items() if roll[1] == maxRollCount]
# print(modeRolls, maxRollCount)

# Plot roll distribution
column_names = [str(x) for x in range(1,100)]
possibleRolls = list(range(1,100))
# values = []
# for x in possibleRolls:
#     if x in rollCount:
#         values.append(rollCount[x])
#     else:
#         values.append(0)
def tickFormatter(x, pos):
    return minorTickLabels[pos]
formatter = ticker.FuncFormatter(tickFormatter)
# Because minor labels start at x=-1, add an extra 0 to the start of the label list
minorTickLabels = [0]+possibleRolls[1::2]
minorTickLabels.append(100)
minorTickLabels.append(102)
values = [rollCount[x] if x in rollCount else 0 for x in possibleRolls]
plt.figure(figsize=(15,4),dpi=100)
plt.bar(column_names, values)
# Unclear why, but have to shift median and mean lines left 1 due to unexplainable offset
plt.axvline(meanRolls-1, color='red', label='Mean Roll')
plt.axvline(medianRolls-1, color='black', label='Median Roll')
plt.legend()
ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_formatter(formatter)
ax.tick_params(axis='x', which='minor', length=15)
ax.autoscale(enable=True, axis='x',tight=True)

plt.savefig(outputFolder+rollGraphFile, transparent=True)

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
    noNeed = "\nNo Need roll-offs!"
neediestPlayers  = [key for key, value in needCount.items() if value == maxCount]

needWins = list(Counter([roll.member.name for roll in needrolls if roll.win]))

needRatios = aggregate.winRatios(uniqueMembers, needrolls)
greedRatios = aggregate.winRatios(uniqueMembers, greedrolls)

ratios = [item[2] for item in needRatios.values()]
try:
    maxRatio = max(ratios)
    minWins = min([item[0] for item in needRatios.values()])
    badNeeders = [(key,value) for key, value in needRatios.items() if value[0] == minWins]
    mostTries = max([value[1][2] for value in badNeeders])
    worstNeeders = [value for value in badNeeders if value[1][2] == mostTries]
    bestNeeders = [(key,value[0],value[1],value[2]) for key, value in needRatios.items() if value[2] == maxRatio]
    # print("\nBEST NEEDER")
    # print(bestNeeders)

    # print("\nWORST NEEDER")
    # print(worstNeeders)
except ValueError:
    bestNeeders = "\nNo Need roll-offs"


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
    bestGreeders = "\nNo Greed roll-offs"

# Convert unicode char indicating HQ to 'HQ'
def translate_HQ(string, translation= u'HQ'):
    hqChar = u'\ue03c'
    translate_table = dict((ord(char), translation) for char in hqChar)
    return string.translate(translate_table)

# Show loot that wasn't rolled for
members = []
for encounter in encounters:
    for member in encounter.members:
        members.append(member)
eventLoot = []
privateLoot = []
for member in members:
    for item in member.loot:
        if 'gil' not in item.name and 'tomestone' not in item.name:
            eventLoot.append(item)
        else:
            privateLoot.append(item)

totalEventLoot = defaultdict(int)
for item in eventLoot:
    name = translate_HQ(item.name)
    totalEventLoot[name] += item.quantity
totalPrivateLoot = defaultdict(int)
for item in privateLoot:
    totalPrivateLoot[item.name] += item.quantity


sortedTotalEventLoot = {k:v for k,v in sorted(totalEventLoot.items(), key= lambda item: item[1], reverse=True)}
sortedTotalPrivateLoot = {k:v for k,v in sorted(totalPrivateLoot.items(), key= lambda item: item[1], reverse=True)}

# Calculate what percentage of greed/need wins each member has won
needWinPercents = aggregate.percentWins(uniqueMembers, needrolls)
greedWinPercents = aggregate.percentWins(uniqueMembers, greedrolls)





outputHeader = """# FFXIV Loot Analyzer Report
## File: {}
## Logged By: {}
""".format(file, logger)

outputMembers = """# Participating Members""" + ''.join('\n- {}'.format(member) for member in uniqueMembers)

outputPersonalLoot = """\n# Personal Loot""" + ''.join('\n- {} {}'.format(*item) for item in totalPrivateLoot.items())

outputRolledLoot ="""\n# Rolled Loot""" + ''.join('\n- {} {}'.format(*item) for item in sortedLoot)

outputEventLoot = """\n# Dropped Loot""" + ''.join('\n- {} {}'.format(*item) for item in sortedTotalEventLoot.items())

outputMean = """\n# Mean Roll""" + ''.join('\n{:.2f}').format(meanRolls)

outputMedian = """\n# Median Roll""" + ''.join('\n{:.2f}').format(medianRolls)

outputMode = """\n# Mode Rolls""" + ''.join('\n- {}'.format(roll) for roll in modeRolls) + """\n\nRolled {} times""".format(maxRollCount)

outputRollGraph = """\n![Graph of roll distributions]({})""".format(rollGraphFile)

# If bestNeeders/bestGreeders is a str, it means there were no need/greed roll-offs.
# TODO #11

if type(bestNeeders) == str:
    outputBestNeeders = """\n # Best Needers""" + bestNeeders
    outputWorstNeeders = """\n # Worst Needers""" + bestNeeders
else:
    outputBestNeeders = """\n# Best Needers\n## Best need roll win rate (wins/attempts)""" + ''.join('\n- {} Wins:{} Rolls:{} Win Rate:{}'.format(*needer) for needer in bestNeeders)
    outputBestNeedPercentage = """\n## Most Need wins (individual wins / total need wins)""" + ''.join('\n- {} Wins:{} Rolls:{} Win Rate:{}'.format(*needer) for needer in bestNeeders)

    outputWorstNeeders = """\n# Worst Needers""" + ''.join('\n- {} {}'.format(*needer) for needer in worstNeeders)

if type(bestGreeders) == str:
    outputBestGreeders = """\n# Best Greeders""" + bestGreeders
    outputWorstGreeders = """\n# Worst Greeders""" + bestGreeders
else:
    outputBestGreeders = """\n# Best Greeders""" + ''.join('\n- {} {}'.format(*greeder) for greeder in bestGreeders)
    outputWorstGreeders = """\n# Worst Greeders""" + ''.join('\n- {} {}'.format(*greeder) for greeder in worstGreeders)

with open(outputFolder+'report.md', 'w') as f:
    f.write(outputHeader + outputMembers +outputPersonalLoot + outputRolledLoot + outputEventLoot + outputMean + outputMedian + outputMode + outputRollGraph + outputBestNeeders + outputWorstNeeders + outputBestGreeders + outputWorstGreeders)
    f.close()