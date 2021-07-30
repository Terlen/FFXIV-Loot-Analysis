from utils.encounter import Encounter, Item, Roll, Member
from collections import Counter
from typing import Union

def get_item_most_rolls(encounter: Encounter) -> Union[Item,list]:
    itemRollCounts = [len(item.rolls) for item in encounter.items]
    rollCountCounter = Counter(itemRollCounts)
    mostRolls = max(itemRollCounts)
    if rollCountCounter[mostRolls] > 1:
        # identify the indicies of itemRollCounts where itemRollCount[index] == mostRolls
        # because the indicies of itemRollCounts correspond to encounter.items, we can use those indicies to return all the items with the most rolls
        indiciesOfItems = [index for index, count in enumerate(itemRollCounts) if count == mostRolls]
        return [encounter.items[index] for index in indiciesOfItems]
    else:
        maxRollsIndex = itemRollCounts.index(mostRolls)
        return encounter.items[maxRollsIndex]


def get_item_fewest_rolls(encounter: Encounter) -> Item:
    itemCounts = [len(item.rolls) for item in encounter.items]
    minRollsIndex = itemCounts.index(min(itemCounts))
    return encounter.items[minRollsIndex]
