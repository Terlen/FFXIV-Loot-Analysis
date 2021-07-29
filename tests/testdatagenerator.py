import random
from utils.encounter import Member, Item, Roll
from operator import itemgetter

#fixedseed = 5
seed = random.randint(0,100)
fixedGen = random.Random(seed)
#print("the seed was: ",seed)


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
    roll = fixedGen.randint(1,99)
    return roll

def random_data_gen(numMembers, numItems):
    print("the seed was :",seed)
    data = []
    numRolls = fixedGen.randint(0,numMembers*numItems)
    members = [random_name_gen() for x in range(numMembers)]
    items = [random_item_gen() for x in range(numItems)]
    for item in items:
        data.append(["8-8-08","AddLoot",'',item[0], 0, item[1]])
    rolls = []
    winRoll = 0
    winner = ''
    for item in items:
        for member in members:
            data.append(["8-8-08","CastLoot",member,item[0],0,item[1]])
    for item in items:
        if fixedGen.randint(0,1):
            rollType = "GreedLoot"
        else:
            rollType = "NeedLoot"
        for member in members:
            if len(rolls) < numRolls:
                while True:
                    roll = random_roll_gen()
                    if roll not in rolls:
                        break
                data.append(["8-8-08",rollType, member,item[0], roll, item[1]])
                if roll > winRoll:
                    winRoll = roll
                    winner = member
        data.append(["8-8-08","ObtainLoot", winner, item[0], winRoll, item[1]])
    return data
