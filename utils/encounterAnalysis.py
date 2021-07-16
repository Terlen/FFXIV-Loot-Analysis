from utils.encounter import Encounter, Item, Roll, Member

def get_item_most_rolls(encounter: Encounter) -> Item:
    itemCounts = {item.name : len(item.rows) for item in encounter.items}
    pass
