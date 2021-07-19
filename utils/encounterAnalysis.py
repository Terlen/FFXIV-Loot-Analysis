from utils.encounter import Encounter, Item, Roll, Member

def get_item_most_rolls(encounter: Encounter) -> Item:
    itemCounts = [len(item.rolls) for item in encounter.items]
    maxRollsIndex = itemCounts.index(max(itemCounts))
    return encounter.items[maxRollsIndex]

def get_item_fewest_rolls(encounter: Encounter) -> Item:
    itemCounts = [len(item.rolls) for item in encounter.items]
    minRollsIndex = itemCounts.index(min(itemCounts))
    return encounter.items[minRollsIndex]
