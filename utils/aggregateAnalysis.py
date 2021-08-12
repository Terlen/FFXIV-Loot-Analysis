def winRatios(members, rolls):
    memberWinRatios = {}
    for member in members:
        attempts = [roll for roll in rolls if roll.member.name == member]
        wins = [roll for roll in attempts if roll.win]
        try:
            winRatio = len(wins) / len(attempts)
            memberWinRatios[member] = (len(wins),len(attempts),winRatio)
        except ZeroDivisionError:
            continue
    return memberWinRatios

def percentWins(members, rolls):
    winPercentages = {}
    totalWins = [roll for roll in rolls if roll.win]
    for member in members:
        memberWins = len([roll for roll in totalWins if roll.member.name == member])
        try:
            winPercent = memberWins / len(totalWins)
            winPercentages[member] = (memberWins, len(totalWins), winPercent)
        except ZeroDivisionError:
            continue
    return winPercentages

def getMembersBestRatio(ratios):
    items = ratios.items()
    stats = ratios.values()
    ratioValues = [item[2] for item in ratios.values()]
    try:
        maxRatio = max(ratioValues)
        best = [(key,value[0],value[1],value[2]) for key, value in items if value[2] == maxRatio]
        return best
    except ValueError:
        return None

def getMembersWorstRatio(ratios):
    items = ratios.items()
    stats = ratios.values()
    ratioValues = [item[2] for item in ratios.values()]
    try:
        minRatio = min(ratioValues)
        worst = [(key,value[0],value[1],value[2]) for key, value in items if value[2] == minRatio]
        return worst
    except ValueError:
        return None