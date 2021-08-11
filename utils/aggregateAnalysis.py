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
    winPercentages = ()
    totalWins = [roll for roll in rolls if roll.win]
    for member in members:
        memberWins = len([roll for roll in totalWins if roll.member.name == member])
        try:
            winPercent = memberWins / len(totalWins)
            winPercentages[member] = (memberWins, totalWins, winPercent)
        except ZeroDivisionError:
            continue
    return winPercentages
