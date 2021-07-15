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
    loot = set()
    rolls = set()

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

    def add_loot(self, item, quantity, rowNum):
        self.loot.add(Item(item, quantity, rowNum))

    def set_loot(self, data):
        for rowNum, row in enumerate(data):
            if row[1] == "AddLoot":
                self.add_loot(row[3],row[5], rowNum)
        return self.loot


    def __init__(self, data):
        self.rows = data
        self.set_cleartime(self.rows[0])
        self.set_members(self.rows)
        self.set_loot(self.rows)




    