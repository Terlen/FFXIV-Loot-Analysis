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
    return Member(name)

# Generate a random Item with random name and quantity between 1-3. Each item has no associated rolls on init
def random_item_gen():
    name = itemAdjective[fixedGen.randint(0,4)] + ' ' + itemNoun[fixedGen.randint(0,4)]
    quantity = fixedGen.randint(1,3)
    item = Item(name, quantity)
    return item

# Generate a random roll for given item. Specify if roll is Need/Greed and if it won
def random_roll_gen(rolltype : str, item : Item, member : Member = random_member_gen()):
        roll = Roll(rolltype,member,fixedGen.randint(1,99),item)
        item.rolls.append(roll)
        #print (roll.member.name, roll.type, roll.value)
        return roll


# def test_data_gen(maxRolls, numItems, numMembers):
#     data = []
    
#     items = []
#     for x in range(numItems):
#         items.append(random_item_gen())

#     return items