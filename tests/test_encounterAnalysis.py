from utils.encounter import Encounter, Item, Member, Roll
import random

fixedseed = 5
fixedGen = random.Random()


firstNames = ['Karou', 'Akiva', 'Hien', 'Yda', 'Alphinaud']
lastNames = ['Cookiepouch', 'Final', 'Fantasy', 'Chocobo', 'Tonberry']

def random_member_gen():
    name = firstNames[fixedGen.randint(0,4)] + ' ' + lastNames[fixedGen.randint(0,4)]
    return Member(name)


def random_roll_gen():
    rolltype = random.randint(0,1)
    if rolltype:
        Roll("GreedLoot",)




class Test_get_item_most_rolls_Unit:



    test_items = Item("Test Item 1", 1)


    def test_get_item_most_rolls(self):
        pass