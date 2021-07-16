from utils.encounter import Encounter, Item, Member, Roll
import random

fixedseed = 5
fixedGen = random.Random()


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
    print (name, quantity)
    return Item(name, quantity)

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



class Test_get_item_most_rolls_Unit:



    test_items = Item("Test Item 1", 1)


    def test_get_item_most_rolls(self):
        pass