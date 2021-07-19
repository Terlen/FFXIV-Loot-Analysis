from utils.encounterAnalysis import get_item_most_rolls, get_item_fewest_rolls
from utils.encounter import Encounter, Item, Member, Roll
import random

fixedseed = 5
fixedGen = random.Random()
fixedGen.seed(fixedseed)


firstNames = ['Karou', 'Akiva', 'Hien', 'Yda', 'Alphinaud']
lastNames = ['Cookiepouch', 'Final', 'Fantasy', 'Chocobo', 'Tonberry']

itemAdjective = ["Tataru's", "Kugane", "Meaty", "Rusty", "Resplendent"]
itemNoun = ["Stick", "Lance", "Pot", "Scissors", "Sword"]

def random_member_gen():
    name = firstNames[fixedGen.randint(0,4)] + ' ' + lastNames[fixedGen.randint(0,4)]
    print(name)
    return Member(name)

def random_item_gen():
    name = itemAdjective[fixedGen.randint(0,4)] + ' ' + itemNoun[fixedGen.randint(0,4)]
    quantity = fixedGen.randint(1,3)
    item = Item(name, quantity)
    return item

def random_roll_gen(rolltype, win):
    if rolltype:
        roll = Roll("GreedLoot",random_member_gen(),fixedGen.randint(1,99),random_item_gen())
        roll.win = win
        print (roll.member.name, roll.type, roll.value, roll.win)
        return roll
    elif not rolltype:
        roll = Roll("NeedLoot",random_member_gen(),fixedGen.randint(1,99),random_item_gen())
        roll.win = win
        print (roll.member.name, roll.type, roll.value, roll.win)
        return roll

# def test_data_gen(maxRolls, numItems, numMembers):
#     data = []
    
#     items = []
#     for x in range(numItems):
#         items.append(random_item_gen())

#     return items


class Test_get_item_most_rolls_Unit:

    items = [random_item_gen(),random_item_gen()]

    items[0].rolls.append(random_roll_gen(1,1))
    items[0].rolls.append(random_roll_gen(1,0))

    items[1].rolls.append(random_roll_gen(0, 1))
    items[1].rolls.append(random_roll_gen(0,0))
    items[1].rolls.append(random_roll_gen(0,0))

    encounter = Encounter([['18:00', 'AddLoot', '','Stick',0,1], ['18:00', 'GreedLoot', 'Test','Stick',20,1]])
    encounter.items = items

    def test_get_item_most_rolls(self):
        assert get_item_most_rolls(self.encounter) == self.items[1]

    def test_get_item_fewest_rolls(self):
        assert get_item_fewest_rolls(self.encounter) == self.items[0]