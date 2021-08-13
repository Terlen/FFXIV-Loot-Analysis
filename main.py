from os import truncate
import utils.dataReader as reader
import utils.aggregateAnalysis as aggregate
import argparse
import utils.visualizations as visualize
from inspect import cleandoc
import utils.reportGenerator as reportGen

if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description="Perform analysis on FFXIV loot data.")
    argParser.add_argument('data', type=str, help='The path of the data file to be analyzed. Supports .txt and .csv files.')
    argParser.add_argument('logger', type=str, help='The name of the player who captured the data file.')
    argParser.add_argument('-outputPath', type=str, default='output', help="The desired directory for output files. Default 'output'.")
    args = argParser.parse_args()

    dataFile = args.data
    fileLogger = args.logger
    outputFolder = args.outputPath + '/'
    reportName = 'report.md'
    
    # Instantiate a report
    report = reportGen.Report(fileLogger,dataFile)
    reportListSection = reportGen.ListSection


    if '.csv' in dataFile:
        data = reader.dataRead(dataFile)
    elif '.txt' in dataFile:
        data = reader.textParser(dataFile, fileLogger)
    else:
        print("Unsupported data file, please provide a .txt or .csv")
        exit()


    encounters = reader.encounterSplitter(data, fileLogger)
    rollGraphFile = 'rolldistribution.png'
    needPieChartFile = 'needPie.png'
    greedPieChartFile = 'greedPie.png'

    # Testing boolean
    reportMemberList = True
    if reportMemberList == True:
        members = aggregate.getMemberList(encounters)
        uniqueMemberNames = aggregate.getMemberNames(members)
        reportMemberList = report.addSection(reportGen.Section(title="Participating Members"))
        reportMemberList.addSubSection(reportGen.ListSection(data=uniqueMemberNames))
    
    # Testing boolean
    reportRolledItems = True
    if reportRolledItems == True:
        rolledItems = aggregate.getRolledItemNames(encounters)
        rolledItemCounts = aggregate.countList(rolledItems)
        reportRolledLoot = report.addSection(reportGen.Section(title="Rolled Loot"))
        reportRolledLoot.addSubSection(reportGen.ListSection(data=rolledItemCounts.most_common()))

    # Testing boolean
    reportRollData = True
    if reportRollData == True:
        rolledNumbers = aggregate.getRolledValues(encounters)
        rolledNumberCount = aggregate.countList(rolledNumbers)
        rollStatistics = aggregate.rollStatistics(rolledNumbers)

        reportRollDistribution = report.addSection(reportGen.Section(title="Roll Distribution"))
        reportRollDistribution.addSubSection(reportGen.ValueSection(title="Mean Roll",data=rollStatistics.mean))
        reportRollDistribution.addSubSection(reportGen.ValueSection(title="Median Roll", data=rollStatistics.median))
        reportRollDistribution.addSubSection(reportGen.ListSection(title="Mode Rolls", data=rollStatistics.mode[0]))
        reportRollDistribution.addSubSection(reportGen.ValueSection("Mode Roll Frequency",data=rollStatistics.mode[1]))

        # Testing boolean
        reportGraphRollDistribution = True
        if reportGraphRollDistribution == True:
            visualize.rollDistributionChart(rolledNumberCount, rollStatistics, outputFolder, rollGraphFile)
    
            reportRollDistribution.addSubSection(reportGen.GraphicSection(title="Roll Distribution Chart", data=rollGraphFile, alttext="Roll Distribution Chart"))

    # Testing boolean
    reportGreed = True
    if reportGreed == True:
        greedrolls = aggregate.getRolls(encounters, "GreedLoot")
        memberGreedCount = aggregate.countList([roll.member.name for roll in greedrolls])
        greediestPlayers = aggregate.getCounterKeysWithValue(memberGreedCount, aggregate.getCounterMaxCount(memberGreedCount))
        greedRatios = aggregate.winRatios(uniqueMemberNames, greedrolls)
        bestGreeders = aggregate.getMembersBestRatio(greedRatios)
        worstGreeders = aggregate.getMembersWorstRatio(greedRatios)
        greedWinPercents = aggregate.percentWins(uniqueMemberNames, greedrolls)
        bestGreedWinPercentage = aggregate.getMembersBestRatio(greedWinPercents)
        worstGreedWinPercentage = aggregate.getMembersWorstRatio(greedWinPercents)


        reportGreedRolls = report.addSection(reportGen.Section(title="Greed Rolls"))
        reportGreedRolls.addSubSection(reportGen.Section("Best Greeders", nest = 1))
        reportGreedRolls.addSubSection(reportGen.ListSection("Best Win Rate (wins/attempts)",nest = 2, data=bestGreeders))
        reportGreedRolls.addSubSection(reportGen.ListSection("Best Win Percentage (wins/all member wins)",nest = 2, data=bestGreedWinPercentage ))
        reportGreedRolls.addSubSection(reportGen.Section("Worst Greeders", nest = 1))
        reportGreedRolls.addSubSection(reportGen.ListSection("Worst Win Rate (wins/attempts)",nest = 2, data=worstGreeders))
        reportGreedRolls.addSubSection(reportGen.ListSection("Worst Win Percentage (wins/all member wins)",nest = 2, data=worstGreedWinPercentage ))

        visualize.pieChartPercentWins(greedWinPercents, outputFolder, greedPieChartFile)

        reportGreedRolls.addSubSection(reportGen.GraphicSection("Greed Win Percent Chart", data= greedPieChartFile, alttext="Greed Roll Win Percentage Pie Chart"))

    # Testing boolean
    reportNeed = True
    if reportNeed == True:

        needrolls = aggregate.getRolls(encounters, "NeedLoot")
        memberNeedCount = aggregate.countList([roll.member.name for roll in needrolls])
        neediestPlayers = aggregate.getCounterKeysWithValue(memberNeedCount, aggregate.getCounterMaxCount(memberNeedCount))

        needRatios = aggregate.winRatios(uniqueMemberNames, needrolls)
        

        bestNeeders = aggregate.getMembersBestRatio(needRatios)
        worstNeeders = aggregate.getMembersWorstRatio(needRatios)
        needWinPercents = aggregate.percentWins(uniqueMemberNames, needrolls)

        bestNeedWinPercentage = aggregate.getMembersBestRatio(needWinPercents)
        worstNeedWinPercentage = aggregate.getMembersWorstRatio(needWinPercents)

        reportNeedRolls = report.addSection(reportGen.Section(title="Need Rolls"))
        reportNeedRolls.addSubSection(reportGen.Section("Best Needers", nest = 1))
        reportNeedRolls.addSubSection(reportGen.ListSection("Best Win Rate (wins/attempts)",nest = 2, data=bestNeeders))
        reportNeedRolls.addSubSection(reportGen.ListSection("Best Win Percentage (wins/all member wins)",nest = 2, data=bestNeedWinPercentage ))
        reportNeedRolls.addSubSection(reportGen.Section("Worst Needers", nest = 1))
        reportNeedRolls.addSubSection(reportGen.ListSection("Worst Win Rate (wins/attempts)",nest = 2, data=worstNeeders))
        reportNeedRolls.addSubSection(reportGen.ListSection("Worst Win Percentage (wins/all member wins)",nest = 2, data=worstNeedWinPercentage ))



        visualize.pieChartPercentWins(needWinPercents, outputFolder, needPieChartFile)

        reportNeedRolls.addSubSection(reportGen.GraphicSection("Need Win Percent Chart", data= needPieChartFile, alttext="Need Roll Win Percentage Pie Chart"))


    # Testing boolean
    reportDropped = True
    reportPrivate = True
    if reportDropped == True or reportPrivate == True:
        totalEventLoot, totalPrivateLoot = aggregate.getDroppedLoot(members, fileLogger)
        if reportDropped == True:
            reportDroppedLoot = report.addSection(reportGen.Section(title="Dropped Loot"))
            reportDroppedLoot.addSubSection(reportGen.ListSection(data=totalEventLoot))
        if reportPrivate == True:
            reportPrivateLoot = report.addSection(reportGen.Section(title="Private Loot"))
            reportPrivateLoot.addSubSection(reportGen.ListSection(data=totalPrivateLoot))
    


    
    


   

    


    # outputHeader = """
    #     # FFXIV Loot Analyzer Report
    #     ## File: {}
    #     ## Logged By: {}
    #     """.format(dataFile, fileLogger)
    # outputHeader = cleandoc(outputHeader)

    # outputMembers = """\n# Participating Members""" + ''.join('\n- {}'.format(member) for member in uniqueMemberNames)

    # outputPersonalLoot = """\n# Personal Loot""" + ''.join('\n- {} {}'.format(*item) for item in totalPrivateLoot.items())

    # outputRolledLoot ="""\n# Rolled Loot""" + ''.join('\n- {} {}'.format(*item) for item in rolledItemCounts.most_common())

    # outputEventLoot = """\n# Dropped Loot""" + ''.join('\n- {} {}'.format(*item) for item in totalEventLoot.items())

    # outputMean = """\n# Mean Roll""" + ''.join('\n{:.2f}').format(rollStatistics.mean)

    # outputMedian = """\n# Median Roll""" + ''.join('\n{:.2f}').format(rollStatistics.median)

    # outputMode = """\n# Mode Rolls""" + ''.join('\n- {}'.format(roll) for roll in rollStatistics.mode[0]) + """\n\nRolled {} times""".format(rollStatistics.mode[1])

    # outputRollGraph = """\n![Graph of roll distributions]({})""".format(rollGraphFile)

    # # If bestNeeders/bestGreeders is a str, it means there were no need/greed roll-offs.
    # # TODO #11

    # bestNeedersHeader = """\n # Best Needers"""

    # noRolls = "\nThere were no need roll-offs!"
    # if bestNeeders == None:
    #     outputBestNeeders, outputWorstNeeders =  (noRolls,noRolls)
    # else:
    #     BestNeedWinRate = """\n## Best win rate (wins/attempts)""" + ''.join('\n- {} Wins:{} Rolls:{} Win Rate:{:.2%}'.format(*needer) for needer in bestNeeders)
    #     BestNeedPercentage = """\n## Most Need wins (individual wins / total need wins)""" + ''.join('\n- {} Wins:{} Total Wins:{} Win Percentage:{:.2%}'.format(*needer) for needer in bestNeedWinPercentage)

    #     outputBestNeeders = bestNeedersHeader + BestNeedWinRate + BestNeedPercentage

    #     outputWorstNeeders = """\n# Worst Needers""" + ''.join('\n- {} Wins:{} Rolls:{} Win Rate:{:.2%}'.format(*needer) for needer in worstNeeders)

    # if bestGreeders == None:
    #     outputBestGreeders = """\n# Best Greeders""" + noRolls
    #     outputWorstGreeders = """\n# Worst Greeders""" + noRolls
    # else:
    #     outputBestGreeders = """\n# Best Greeders""" + ''.join('\n- {} {}'.format(*greeder) for greeder in bestGreeders)
    #     outputWorstGreeders = """\n# Worst Greeders""" + ''.join('\n- {} {}'.format(*greeder) for greeder in worstGreeders)

    # outputPieChart = """\n![Pie chart of each member's need win percentage]({})""".format(needPieChartFile)

    # with open(outputFolder+'report.md', 'w') as f:
    #     f.write(outputHeader + outputMembers +outputPersonalLoot + outputRolledLoot + outputEventLoot + outputMean + outputMedian + outputMode + outputRollGraph + outputBestNeeders + outputWorstNeeders + outputBestGreeders + outputWorstGreeders + outputPieChart)
    #     f.close()
    # reportTemplate = report.loadTemplate('templates/report.md')
    # reportText = report.reportBuilder(dataFile, fileLogger, uniqueMemberNames,reportTemplate)
    # report.reportSave(outputFolder, reportText)
    report.export(outputFolder,reportName)