from operator import attrgetter

class Roll:
    def __init__(self, rollType, member, rollValue, item):
        self.member = member
        self.value = rollValue
        self.type = rollType
        self.item = item
        self.win = False
    def __eq__(self, other):
        attributes = attrgetter("member", "value", "type", "item")
        return self is other or attributes(self) == attributes(other)
    def iswin(self, bool):
        self.win = bool
        return self

class Item:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        self.rolls = []
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.name == other.name

class Member:
    def __init__(self, name):
        self.name = name
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.name == other.name


class Encounter:

    # def add_row(self, row):
    #     self.rows.append(row)
    #     return self.rows

    def set_cleartime(self, firstrow):
        self.cleartime = firstrow[0]
    
    def add_member(self, name):
        self.members.append(Member(name))
        return self.members

    def set_members(self, data):
        for row in data:
            names = [member.name for member in self.members]
            if row[2] != '' and row[2] not in names:
                self.add_member(row[2])
        return self.members

    def add_item(self, name, quantity):
        item = Item(name,quantity)
        if item not in self.items:
            self.items.append(item)

    def set_item(self, data):
        for row in data:
            if row[1] == "AddLoot":
                self.add_item(row[3],row[5])
        return self.items
    
    def get_item(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None
    
    def add_roll(self, rollType, member, value, item):
        roll = Roll(rollType,member,value,item)
        self.rolls.append(roll)
        item.rolls.append(roll)

    def set_rolls(self, data):
        for row in data:
            action = row[1]
            if action == "GreedLoot" or action == "NeedLoot":
                self.add_roll(action, self.get_member(row[2]), row[4],self.get_item(row[3]))

    def get_member(self, name):
        for member in self.members:
            if member.name == name:
                return member
        return None

    def set_winning_rolls(self):
        for item in self.items:
            rollValues = [roll.value for roll in item.rolls]
            highestRollValue = max(rollValues)
            highestRoll =  item.rolls[rollValues.index(highestRollValue)]
            highestRoll.iswin(True)

    def get_winning_rolls(self):
        winners = [roll for roll in self.rolls if roll.win]
        return winners

    def __init__(self, data=None):
        self.cleartime = ''
        self.members = []
        self.items = []
        self.rolls = []
        self.rows = data
        self.set_cleartime(self.rows[0])
        self.set_members(self.rows)
        self.set_item(self.rows)
        self.set_rolls(self.rows)
        #self.set_lootwins(self.items)
        self.set_winning_rolls()




    