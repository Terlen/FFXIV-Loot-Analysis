import utils.dataReader as reader
import utils.aggregateAnalysis as aggregate
import argparse
import utils.visualizations as visualize
import utils.reportGenerator as reportGen
from markdown2 import markdown_path
import asyncio

async def main():
    argParser = argparse.ArgumentParser(description="Perform analysis on FFXIV loot data.")
    argParser.add_argument('file', type=str, help='The path of the data file to be analyzed. Supports .txt and .csv files.')
    argParser.add_argument('logger', type=str, help='The name of the player who captured the data file.')
    argParser.add_argument('-outputDir', type=str, default='output', help="The desired directory for output files. Default 'output'.")
    argParser.add_argument('-reportfile', type=str, default='report', help="The name of the generated report file." )
    argParser.add_argument('--html', action='store_true', help='Generate a .html file from report.')
    graphGroup = argParser.add_mutually_exclusive_group()
    graphGroup.add_argument('--nograph', action='store_true', help="Disable data visualizations.")
    graphGroup.add_argument('--noreport', action="store_true", help="Disable report generation, exclusively perform data visualizations.")
    argParser.add_argument('--nomembers', action='store_true', help='Disable reporting of members.')
    argParser.add_argument('--norolledloot', action="store_true", help='Disable reporting of Rolled Loot.')
    argParser.add_argument('--norolls', action='store_true', help='Disable reporting of roll data.')
    argParser.add_argument('--nogreed', action="store_true", help='Disable reporting of Greed data.')
    argParser.add_argument('--noneed', action='store_true', help='Disable reporting of Need data.')
    argParser.add_argument('--nodroppedloot', action ='store_true', help='Disable reporting of dropped loot.')
    argParser.add_argument('--noprivateloot', action='store_true', help='Disable reporting of private loot.')
    argParser.add_argument('--nomarketboard', action='store_true', help ='Disable estimation of item marketboard prices.')

    args = argParser.parse_args()

    dataFile = args.file
    fileLogger = args.logger
    outputFolder = args.outputDir + '/'
    

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

    if args.nomembers != True:
        members = aggregate.getMemberList(encounters)
        uniqueMemberNames = aggregate.getMemberNames(members)
        
    
    if args.norolledloot != True:
        rolledItems = await aggregate.getRolledItems(encounters, not args.nomarketboard)
        
        

    if args.norolls != True:
        rolledNumbers = aggregate.getRolledValues(encounters)
        rolledNumberCount = aggregate.countList(rolledNumbers)
        rollStatistics = aggregate.rollStatistics(rolledNumbers)

        if args.nograph == False:
            visualize.rollDistributionChart(rolledNumberCount, rollStatistics, outputFolder, rollGraphFile)
    

    if args.nogreed != True:
        greedrolls = aggregate.getRolls(encounters, "GreedLoot")
        memberGreedCount = aggregate.countList([roll.member.name for roll in greedrolls])
        greediestPlayers = aggregate.getCounterKeysWithValue(memberGreedCount, aggregate.getCounterMaxCount(memberGreedCount))
        greedRatios = aggregate.winRatios(uniqueMemberNames, greedrolls)
        bestGreeders = aggregate.getMembersBestRatio(greedRatios)
        worstGreeders = aggregate.getMembersWorstRatio(greedRatios)
        greedWinPercents = aggregate.percentWins(uniqueMemberNames, greedrolls)
        bestGreedWinPercentage = aggregate.getMembersBestRatio(greedWinPercents)
        worstGreedWinPercentage = aggregate.getMembersWorstRatio(greedWinPercents)

        if args.nograph == False:
            visualize.pieChartPercentWins(greedWinPercents, outputFolder, greedPieChartFile)
            

    if args.noneed != True:

        needrolls = aggregate.getRolls(encounters, "NeedLoot")
        memberNeedCount = aggregate.countList([roll.member.name for roll in needrolls])
        neediestPlayers = aggregate.getCounterKeysWithValue(memberNeedCount, aggregate.getCounterMaxCount(memberNeedCount))

        needRatios = aggregate.winRatios(uniqueMemberNames, needrolls)
        

        bestNeeders = aggregate.getMembersBestRatio(needRatios)
        worstNeeders = aggregate.getMembersWorstRatio(needRatios)
        needWinPercents = aggregate.percentWins(uniqueMemberNames, needrolls)

        bestNeedWinPercentage = aggregate.getMembersBestRatio(needWinPercents)
        worstNeedWinPercentage = aggregate.getMembersWorstRatio(needWinPercents)

        if args.nograph == False:
            visualize.pieChartPercentWins(needWinPercents, outputFolder, needPieChartFile)


    if args.nodroppedloot != True or args.noprivateloot != True:
        totalEventLoot, totalPrivateLoot = await aggregate.getDroppedLoot(members, fileLogger, not args.nomarketboard)
        
    # # TODO #11
    if args.noreport != True:
        # Instantiate a report
        report = reportGen.Report(fileLogger,dataFile)

        if args.nomembers != True:
            reportMemberList = report.addSection(reportGen.Section(title="Participating Members"))
            reportMemberList.addSubSection(reportGen.ListSection(data=uniqueMemberNames))

        if args.norolledloot != True:
            reportRolledLoot = report.addSection(reportGen.Section(title="Rolled Loot"))
            reportRolledLoot.addSubSection(reportGen.TableSection(data=rolledItems))

        if args.norolls != True:
            reportRollDistribution = report.addSection(reportGen.Section(title="Roll Distribution"))
            reportRollDistribution.addSubSection(reportGen.ValueSection(title="Mean Roll",data=rollStatistics.mean))
            reportRollDistribution.addSubSection(reportGen.ValueSection(title="Median Roll", data=rollStatistics.median))
            reportRollDistribution.addSubSection(reportGen.ListSection(title="Mode Rolls", data=rollStatistics.mode[0]))
            reportRollDistribution.addSubSection(reportGen.ValueSection("Mode Roll Frequency",data=rollStatistics.mode[1]))
            if args.nograph != True:
                reportRollDistribution.addSubSection(reportGen.GraphicSection(title="Roll Distribution Chart", data=rollGraphFile, alttext="Roll Distribution Chart"))
        
        if args.nogreed != True:
            reportGreedRolls = report.addSection(reportGen.Section(title="Greed Rolls"))
            reportGreedRolls.addSubSection(reportGen.Section("Best Greeders", nest = 1))
            reportGreedRolls.addSubSection(reportGen.ListSection("Best Win Rate (wins/attempts)",nest = 2, data=bestGreeders))
            reportGreedRolls.addSubSection(reportGen.ListSection("Best Win Percentage (wins/all member wins)",nest = 2, data=bestGreedWinPercentage ))
            reportGreedRolls.addSubSection(reportGen.Section("Worst Greeders", nest = 1))
            reportGreedRolls.addSubSection(reportGen.ListSection("Worst Win Rate (wins/attempts)",nest = 2, data=worstGreeders))
            reportGreedRolls.addSubSection(reportGen.ListSection("Worst Win Percentage (wins/all member wins)",nest = 2, data=worstGreedWinPercentage ))
            if args.nograph != True:
                reportGreedRolls.addSubSection(reportGen.GraphicSection("Greed Win Percent Chart", data= greedPieChartFile, alttext="Greed Roll Win Percentage Pie Chart"))

        if args.noneed != True:
            reportNeedRolls = report.addSection(reportGen.Section(title="Need Rolls"))
            reportNeedRolls.addSubSection(reportGen.Section("Best Needers", nest = 1))
            reportNeedRolls.addSubSection(reportGen.ListSection("Best Win Rate (wins/attempts)",nest = 2, data=bestNeeders))
            reportNeedRolls.addSubSection(reportGen.ListSection("Best Win Percentage (wins/all member wins)",nest = 2, data=bestNeedWinPercentage ))
            reportNeedRolls.addSubSection(reportGen.Section("Worst Needers", nest = 1))
            reportNeedRolls.addSubSection(reportGen.ListSection("Worst Win Rate (wins/attempts)",nest = 2, data=worstNeeders))
            reportNeedRolls.addSubSection(reportGen.ListSection("Worst Win Percentage (wins/all member wins)",nest = 2, data=worstNeedWinPercentage ))
            if args.nograph != True:
                reportNeedRolls.addSubSection(reportGen.GraphicSection("Need Win Percent Chart", data= needPieChartFile, alttext="Need Roll Win Percentage Pie Chart"))
  
        if args.nodroppedloot != True:
            reportDroppedLoot = report.addSection(reportGen.Section(title="Dropped Loot"))
            reportDroppedLoot.addSubSection(reportGen.TableSection(data=totalEventLoot))
        if args.noprivateloot != True:
            reportPrivateLoot = report.addSection(reportGen.Section(title="Private Loot"))
            reportPrivateLoot.addSubSection(reportGen.TableSection(data=totalPrivateLoot))
    
    reportName = args.reportfile+'.md'
    report.export(outputFolder,reportName)

    if args.html == True:
        htmlReport = args.reportfile+'.html'
        html = markdown_path(outputFolder+reportName, extras=['tables'])
        with open(outputFolder+htmlReport, 'w') as reportHtml:
            reportHtml.write(html)
            reportHtml.close()

if __name__ == "__main__":
    asyncio.run(main())
    
    