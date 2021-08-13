import utils.dataReader as reader
import utils.aggregateAnalysis as aggregate
import argparse
import utils.visualizations as visualize
import utils.reportGenerator as reportGen

def main():
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
    

    # # TODO #11

  
    report.export(outputFolder,reportName)

if __name__ == "__main__":
    main()
    