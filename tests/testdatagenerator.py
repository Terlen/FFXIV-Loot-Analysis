import random
from utils.encounter import Member, Item, Roll

fixedseed = 5
fixedGen = random.Random()
fixedGen.seed(fixedseed)

firstNames = ['Karou', 'Akiva', 'Hien', 'Yda', 'Alphinaud']
lastNames = ['Cookiepouch', 'Final', 'Fantasy', 'Chocobo', 'Tonberry']

itemAdjective = ["Tataru's", "Kugane", "Meaty", "Rusty", "Resplendent"]
itemNoun = ["Stick", "Lance", "Pot", "Scissors", "Sword"]

def random_name_gen():
    name = firstNames[fixedGen.randint(0,4)] + ' ' + lastNames[fixedGen.randint(0,4)]
    return name

# Generate a random Item with random name and quantity between 1-3. Each item has no associated rolls on init
def random_item_gen():
    name = itemAdjective[fixedGen.randint(0,4)] + ' ' + itemNoun[fixedGen.randint(0,4)]
    quantity = fixedGen.randint(1,3)
    item = (name,quantity)
    return item

# Generate a random roll for given item. Specify if roll is Need/Greed and if it won
def random_roll_gen():
        rolltype = fixedGen.randint(0,2)
        if rolltype == 1:
            roll = ("GreedLoot", fixedGen.randint(1,99))
        elif rolltype == 2:
            roll = ("NeedLoot", fixedGen.randint(1,99))
        return roll



