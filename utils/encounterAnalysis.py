from utils.encounter import Encounter, Item, Roll, Member
from collections import Counter
from typing import Union
from statistics import mean, median, multimode

def get_most_and_least_rolls(encounterList: list) -> tuple[Union[list[Item],Item],Union[list[Item],Item]]:
    """Function to return the Member(s)/Item(s) with the most and fewest rolls"""
    RollCounts = [len(instance.rolls) for instance in encounterList]
    rollCountCounter = Counter(RollCounts)
    mostRolls = max(RollCounts)
    leastRolls = min(RollCounts)
    if rollCountCounter[mostRolls] > 1:
        # identify the indicies of RollCounts where RollCount[index] == mostRolls
        # because the indicies of RollCounts correspond to the encounterList, we can use those indicies to return all the instances with the most rolls
        indiciesOfInstances = [index for index, count in enumerate(RollCounts) if count == mostRolls]
        mostRolledInstances = [encounterList[index] for index in indiciesOfInstances]
    else:
        maxRollsIndex = RollCounts.index(mostRolls)
        mostRolledInstances =  encounterList[maxRollsIndex]
    if rollCountCounter[leastRolls] > 1:
        indiciesOfInstances = [index for index, count in enumerate(RollCounts) if count == leastRolls]
        leastRolledInstances = [encounterList[index] for index in indiciesOfInstances]
    else:
        leastRollsIndex = RollCounts.index(leastRolls)
        leastRolledInstances =  encounterList[leastRollsIndex]
    return (mostRolledInstances, leastRolledInstances)

def get_winning_rolls(encounter: Encounter):
        winners = [roll for roll in encounter.rolls if roll.win]
        return winners

def get_mean_roll_value(encounter: Encounter) -> Union[float,int]:
    values = [roll.value for roll in encounter.rolls]
    if len(values) > 0:
        return mean(values)
    else:
        return 0

def get_median_roll_value(encounter: Encounter) -> Union[float, int]:
    values = [roll.value for roll in encounter.rolls]
    if len(values) > 0:
        return median(values)
    else:
        return 0
    
def get_mode_roll_value(encounter: Encounter) -> list[int]:
    values = [roll.value for roll in encounter.rolls]
    mode = multimode(values)
    if len(mode) == len(values):
        return []
    else:
        return mode