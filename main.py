import utils.dataReader as reader
import utils.aggregateAnalysis as aggregate
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse
import utils.visualizations as visualize
from inspect import cleandoc

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

    members = aggregate.getMemberList(encounters)
    uniqueMemberNames = aggregate.getMemberNames(members)

    rolledItems = aggregate.getRolledItemNames(encounters)

    rolledItemCounts = aggregate.countList(rolledItems)

    rolledNumbers = aggregate.getRolledValues(encounters)
    rolledNumberCount = aggregate.countList(rolledNumbers)

    rollStatistics = aggregate.rollStatistics(rolledNumbers)

    visualize.rollDistributionChart(rolledNumberCount, rollStatistics, outputFolder, rollGraphFile)
    
    greedrolls = aggregate.getRolls(encounters, "GreedLoot")
    
    memberGreedCount = aggregate.countList([roll.member.name for roll in greedrolls])

    greediestPlayers = aggregate.getCounterKeysWithValue(memberGreedCount, aggregate.getCounterMaxCount(memberGreedCount))

    needrolls = aggregate.getRolls(encounters, "NeedLoot")
    memberNeedCount = aggregate.countList([roll.member.name for roll in needrolls])
    neediestPlayers = aggregate.getCounterKeysWithValue(memberNeedCount, aggregate.getCounterMaxCount(memberNeedCount))

    needRatios = aggregate.winRatios(uniqueMemberNames, needrolls)
    greedRatios = aggregate.winRatios(uniqueMemberNames, greedrolls)

    bestNeeders = aggregate.getMembersBestRatio(needRatios)
    worstNeeders = aggregate.getMembersWorstRatio(needRatios)


    bestGreeders = aggregate.getMembersBestRatio(greedRatios)
    worstGreeders = aggregate.getMembersWorstRatio(greedRatios)

    # Convert unicode char indicating HQ to 'HQ'
    def translate_HQ(string, translation= u'HQ'):
        hqChar = u'\ue03c'
        translate_table = dict((ord(char), translation) for char in hqChar)
        return string.translate(translate_table)

    totalEventLoot, totalPrivateLoot = aggregate.getDroppedLoot(members, fileLogger)


    # Calculate what percentage of greed/need wins each member has won
    needWinPercents = aggregate.percentWins(uniqueMemberNames, needrolls)
    greedWinPercents = aggregate.percentWins(uniqueMemberNames, greedrolls)


    labels = sorted([key for key in needWinPercents.keys()], key= lambda key: needWinPercents[key])
    sizes = [value[2] for value in needWinPercents.values()]
    sizes.sort()
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes,labels=labels, autopct='%1.0f%%', startangle=90, wedgeprops={'color':(1.0,1.0,1.0,0.0), 'edgecolor':'k'}, pctdistance=0.8, counterclock=False)
    ax2.axis('equal')
    plt.savefig(outputFolder+pieChartFile, transparent=True)

    bestNeedWinPercentage = aggregate.getMembersBestRatio(needWinPercents)
    worstNeedWinPercentage = aggregate.getMembersWorstRatio(needWinPercents)


    outputHeader = """
        # FFXIV Loot Analyzer Report
        ## File: {}
        ## Logged By: {}
        """.format(dataFile, fileLogger)
    outputHeader = cleandoc(outputHeader)

    outputMembers = """\n# Participating Members""" + ''.join('\n- {}'.format(member) for member in uniqueMemberNames)

    outputPersonalLoot = """\n# Personal Loot""" + ''.join('\n- {} {}'.format(*item) for item in totalPrivateLoot.items())

    outputRolledLoot ="""\n# Rolled Loot""" + ''.join('\n- {} {}'.format(*item) for item in rolledItemCounts.most_common())

    outputEventLoot = """\n# Dropped Loot""" + ''.join('\n- {} {}'.format(*item) for item in totalEventLoot.items())

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