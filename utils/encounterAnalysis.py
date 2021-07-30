from utils.encounter import Encounter, Item, Roll, Member
from collections import Counter
from typing import Union

def get_item_most_and_least_rolls(encounter: Encounter) -> tuple[Union[list[Item],Item],Union[list[Item],Item]]:
    itemRollCounts = [len(item.rolls) for item in encounter.items]
    rollCountCounter = Counter(itemRollCounts)
    mostRolls = max(itemRollCounts)
    leastRolls = min(itemRollCounts)
    if rollCountCounter[mostRolls] > 1:
        # identify the indicies of itemRollCounts where itemRollCount[index] == mostRolls
        # because the indicies of itemRollCounts correspond to encounter.items, we can use those indicies to return all the items with the most rolls
        indiciesOfItems = [index for index, count in enumerate(itemRollCounts) if count == mostRolls]
        mostRolledItems = [encounter.items[index] for index in indiciesOfItems]
    else:
        maxRollsIndex = itemRollCounts.index(mostRolls)
        mostRolledItems =  encounter.items[maxRollsIndex]
    if rollCountCounter[leastRolls] > 1:
        indiciesOfItems = [index for index, count in enumerate(itemRollCounts) if count == leastRolls]
        leastRolledItems = [encounter.items[index] for index in indiciesOfItems]
    else:
        leastRollsIndex = itemRollCounts.index(leastRolls)
        leastRolledItems =  encounter.items[leastRollsIndex]
    return (mostRolledItems, leastRolledItems)
