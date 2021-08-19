from collections import Counter, namedtuple, defaultdict
from statistics import mean, median, multimode
from utils.api_request import get_item_market_price

stats = namedtuple('rollStats', ['mean', 'median', 'mode'])
lootTupleValued = namedtuple('lootVal', ['item','quantity','value','totalvalue'])
lootTupleNoVal = namedtuple('loot', ['item','quantity'])

def getMemberList(encounters: list) -> list:
    members = []
    for encounter in encounters:
        for member in encounter.members:
            members.append(member)
    return members


def getMemberNames(memberList: list) -> set:
    members = []
    for member in memberList:
        members.append(member.name)
    return set(members)

async def getRolledItems(encounters: list, get_loot_value: bool) -> list:
    loot = []
    for encounter in encounters:
        for item in encounter.items:
            loot.append(item.name)
    loot = countList(loot).most_common()
    if get_loot_value:
        prices = await get_item_market_price([item[0] for item in loot])
        
        loot = [lootTupleValued(item[0], item[1], prices[item[0]]['pricePerUnit'], int(prices[item[0]]['pricePerUnit']) * item[1]) for item in loot]
    else:
        loot = [lootTupleNoVal(item[0],item[1]) for item in loot]
    return loot

def getRolledValues(encounters: list) -> list:
    rolls = []
    for encounter in encounters:
        for roll in encounter.rolls:
            rolls.append(int(roll.value))
    return rolls

def getRolls(encounters: list,type: str) -> list:
    rolls = []
    for encounter in encounters:
        for roll in encounter.rolls:
            if roll.type == type:
               rolls.append(roll)
    return rolls

async def getDroppedLoot(members: list, logger: str, get_loot_value : bool, sort : str ='asc' ) -> tuple[list,list]:
    # Show loot that wasn't rolled for
    eventLoot = []
    privateLoot = []
    for member in members:
        if member.name != logger:
            eventLoot += member.loot
        else:
            # The log file will contain the logger's private loot (gil, tomestones) that each player receives individually.
            # This loot needs to be separated from the randomly dropped eventLoot
            for item in member.loot:
                if 'gil' not in item.name and 'tomestone' not in item.name:
                    eventLoot.append(item)
                else:
                    privateLoot.append(item)

    totalEventLoot = defaultdict(int)
    totalPrivateLoot = defaultdict(int)
    for item in eventLoot:
        totalEventLoot[item.name] += item.quantity
    for item in privateLoot:
        totalPrivateLoot[item.name] += item.quantity
    
    if sort == 'desc':
        sortReverse = True
    else:
        sortReverse = False
    sortedTotalEventLoot = {k:v for k,v in sorted(totalEventLoot.items(), key= lambda item: item[1], reverse=sortReverse)}
    sortedTotalPrivateLoot = {k:v for k,v in sorted(totalPrivateLoot.items(), key= lambda item: item[1], reverse=sortReverse)}
    if get_loot_value:
        prices = await get_item_market_price(list(sortedTotalEventLoot.keys()))
        sortedTotalEventLoot = [lootTupleValued(item[0],item[1],prices[item[0]]['pricePerUnit'], int(prices[item[0]]['pricePerUnit'])*item[1]) for item in sortedTotalEventLoot.items()]
        sortedTotalPrivateLoot = [lootTupleNoVal(item[0],item[1]) for item in sortedTotalPrivateLoot.items()]
        
        pass
    else:
        sortedTotalEventLoot = [lootTupleNoVal(item[0],item[1]) for item in sortedTotalEventLoot.items()]
        sortedTotalPrivateLoot = [lootTupleNoVal(item[0],item[1]) for item in sortedTotalPrivateLoot.items()]
    return (sortedTotalEventLoot, sortedTotalPrivateLoot)

def countList(list: list) -> Counter:
    return Counter(list)

def getCounterMaxCount(counter: Counter) -> int:
    return counter.most_common()[0][1] if counter else 0

def getCounterKeysWithValue(counter: Counter, count: int) -> list:
    return [key for key,value in counter.items() if value == count]

def rollStatistics(rolledNumbers: list) -> stats:
    rollCount = Counter(rolledNumbers)
    maxRollCount = getCounterMaxCount(rollCount)
    meanRolls = mean(rolledNumbers)
    medianRolls = median(rolledNumbers)
    rollMode = multimode(rolledNumbers)
    return stats(meanRolls,medianRolls,(rollMode, maxRollCount))


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
