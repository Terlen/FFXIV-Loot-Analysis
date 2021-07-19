from utils.encounter import Encounter, Item, Roll, Member

def get_item_most_rolls(encounter: Encounter) -> Item:
    itemCounts = [len(item.rolls) for item in encounter.items]
    maxRollsIndex = itemCounts.index(max(itemCounts))
    return encounter.items[maxRollsIndex]
