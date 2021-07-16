class Roll:
    def __init__(self, rollType, member, rollValue, item):
        self.member = member
        self.value = rollValue
        self.type = rollType
        self.item = item

class Item:
    def __init__(self, name, quantity, rowNumber):
        self.name = name
        self.quantity = quantity
        self.id = rowNumber
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.id == other.id

class Member:
    def __init__(self, name):
        self.name = name
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.name == other.name

class Encounter:

    rows = []
    cleartime = ''
    members = {}
    items = []
    rolls = []

    def add_row(self, row):
        self.rows.append(row)
        return self.rows

    def set_cleartime(self, firstrow):
        self.cleartime = firstrow[0]
    
    def add_member(self, name):
        self.members[name]= (Member(name))
        return self.members

    def set_members(self, data):
        for row in data:
            if row[2] != '':
                self.add_member(row[2])
        return self.members

    def add_item(self, item, quantity, rowNum):
        self.items.append(Item(item, quantity, rowNum))

    def set_item(self, data):
        for rowNum, row in enumerate(data):
            if row[1] == "AddLoot":
                self.add_item(row[3],row[5], rowNum)
        return self.items
    
    def add_roll(self, rollType, member, value, item):
        self.rolls.append(Roll(rollType,member,value,item))

    def set_rolls(self, data):
        for row in data:
            rollType = row[1]
            if rollType == "GreedLoot":
                self.add_roll(rollType, )
            elif rollType == "NeedLoot":
                pass

    def __init__(self, data=None):
        self.rows = data
        self.set_cleartime(self.rows[0])
        self.set_members(self.rows)
        self.set_item(self.rows)




    