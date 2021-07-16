from utils.encounter import Encounter, Item, Member, Roll
import random

fixedseed = 5
fixedGen = random.Random()


firstNames = ['Karou', 'Akiva', 'Hien', 'Yda', 'Alphinaud']
lastNames = ['Cookiepouch', 'Final', 'Fantasy', 'Chocobo', 'Tonberry']

def random_member_gen():
    name = firstNames[fixedGen.randint(0,4)] + ' ' + lastNames[fixedGen.randint(0,4)]
    print(name)
    return Member(name)


def random_roll_gen():
    rolltype = fixedGen.randint(0,1)
    if rolltype:
        return Roll("GreedLoot",random_member_gen(),fixedGen.randint(1,99),item)
    elif not rolltype:
        return Roll("NeedLoot",random_member_gen(),fixedGen.randint(1,99),item)



class Test_get_item_most_rolls_Unit:



    test_items = Item("Test Item 1", 1)


    def test_get_item_most_rolls(self):
        pass