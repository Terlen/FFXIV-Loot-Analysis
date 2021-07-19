import random
from utils.encounter import Member, Item, Roll

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