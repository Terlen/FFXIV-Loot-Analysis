import utils.dataReader as reader
from collections import Counter
import utils.aggregateAnalysis as aggregate
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse
import utils.visualizations as visualize

if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description="Perform analysis on FFXIV loot data.")
    argParser.add_argument('data', type=str, help='The path of the data file to be analyzed. Supports .txt and .csv files.')
    argParser.add_argument('logger', type=str, help='The name of the player who captured the data file.')
    argParser.add_argument('-outputPath', type=str, default='output', help="The desired directory for output files. Default 'output'.")
    args = argParser.parse_args()

    dataFile = args.data
    fileLogger = args.logger
    outputFolder = args.outputPath + '/'


    if '.csv' in dataFile:
        data = reader.dataRead(dataFile)
    elif '.txt' in dataFile:
        data = reader.textParser(dataFile, fileLogger)
    else:
        print("Unsupported data file, please provide a .txt or .csv")
        exit()


    encounters = reader.encounterSplitter(data, fileLogger)
    rollGraphFile = 'rolldistribution.png'
    pieChartFile = 'pie.png'

    uniqueMembers = aggregate.getMemberNames(encounters)

    rolledItems = aggregate.getRolledItemNames(encounters)

    rolledItemCounts = aggregate.countList(rolledItems)

    rolledNumbers = aggregate.getRolledValues(encounters)
    rolledNumberCount = aggregate.countList(rolledNumbers)

    rollStatistics = aggregate.rollStatistics(rolledNumbers)

    try:
        visualize.rollDistributionChart(rolledNumberCount, rollStatistics, outputFolder, rollGraphFile)
    except OSError:
        print("Unable to save roll distribution chart. Is the file open?")
        
    

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

    bestNeeders = aggregate.getMembersBestRatio(needRatios)
    worstNeeders = aggregate.getMembersWorstRatio(needRatios)


    bestGreeders = aggregate.getMembersBestRatio(greedRatios)
    worstGreeders = aggregate.getMembersWorstRatio(greedRatios)

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


    labels = sorted([key for key in needWinPercents.keys()], key= lambda key: needWinPercents[key])
    sizes = [value[2] for value in needWinPercents.values()]
    sizes.sort()
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes,labels=labels, autopct='%1.0f%%', startangle=90, wedgeprops={'color':(1.0,1.0,1.0,0.0), 'edgecolor':'k'}, pctdistance=0.8, counterclock=False)
    ax2.axis('equal')
    plt.savefig(outputFolder+pieChartFile, transparent=True)

    bestNeedWinPercentage = aggregate.getMembersBestRatio(needWinPercents)
    worstNeedWinPercentage = aggregate.getMembersWorstRatio(needWinPercents)


    outputHeader = """# FFXIV Loot Analyzer Report
    ## File: {}
    ## Logged By: {}
    """.format(dataFile, fileLogger)

    outputMembers = """# Participating Members""" + ''.join('\n- {}'.format(member) for member in uniqueMembers)

    outputPersonalLoot = """\n# Personal Loot""" + ''.join('\n- {} {}'.format(*item) for item in totalPrivateLoot.items())

    outputRolledLoot ="""\n# Rolled Loot""" + ''.join('\n- {} {}'.format(*item) for item in rolledItemCounts.most_common())

    outputEventLoot = """\n# Dropped Loot""" + ''.join('\n- {} {}'.format(*item) for item in sortedTotalEventLoot.items())

    outputMean = """\n# Mean Roll""" + ''.join('\n{:.2f}').format(rollStatistics.mean)

    outputMedian = """\n# Median Roll""" + ''.join('\n{:.2f}').format(rollStatistics.median)

    outputMode = """\n# Mode Rolls""" + ''.join('\n- {}'.format(roll) for roll in rollStatistics.mode[0]) + """\n\nRolled {} times""".format(rollStatistics.mode[1])

    outputRollGraph = """\n![Graph of roll distributions]({})""".format(rollGraphFile)

    # If bestNeeders/bestGreeders is a str, it means there were no need/greed roll-offs.
    # TODO #11

    bestNeedersHeader = """\n # Best Needers"""

    noRolls = "\nThere were no need roll-offs!"
    if bestNeeders == None:
        outputBestNeeders, outputWorstNeeders =  (noRolls,noRolls)
    else:
        BestNeedWinRate = """\n## Best win rate (wins/attempts)""" + ''.join('\n- {} Wins:{} Rolls:{} Win Rate:{:.2%}'.format(*needer) for needer in bestNeeders)
        BestNeedPercentage = """\n## Most Need wins (individual wins / total need wins)""" + ''.join('\n- {} Wins:{} Total Wins:{} Win Percentage:{:.2%}'.format(*needer) for needer in bestNeedWinPercentage)

        outputBestNeeders = bestNeedersHeader + BestNeedWinRate + BestNeedPercentage

        outputWorstNeeders = """\n# Worst Needers""" + ''.join('\n- {} Wins:{} Rolls:{} Win Rate:{:.2%}'.format(*needer) for needer in worstNeeders)

    if bestGreeders == None:
        outputBestGreeders = """\n# Best Greeders""" + noRolls
        outputWorstGreeders = """\n# Worst Greeders""" + noRolls
    else:
        outputBestGreeders = """\n# Best Greeders""" + ''.join('\n- {} {}'.format(*greeder) for greeder in bestGreeders)
        outputWorstGreeders = """\n# Worst Greeders""" + ''.join('\n- {} {}'.format(*greeder) for greeder in worstGreeders)

    outputPieChart = """\n![Pie chart of each member's need win percentage]({})""".format(pieChartFile)

    with open(outputFolder+'report.md', 'w') as f:
        f.write(outputHeader + outputMembers +outputPersonalLoot + outputRolledLoot + outputEventLoot + outputMean + outputMedian + outputMode + outputRollGraph + outputBestNeeders + outputWorstNeeders + outputBestGreeders + outputWorstGreeders + outputPieChart)
        f.close()