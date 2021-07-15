class Roll:
    def __init__(self, rollType, member, rollValue, item):
        self.member = member
        self.value = rollValue
        self.type = rollType
        self.item = item

class Item:
    def __init__(self, name):
        self.name = name

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
    members = set()
    loot = set()
    rolls = set()

    def set_cleartime(self, firstrow):
        self.cleartime = firstrow[0]
    
    def add_member(self, name):
        self.members.add(Member(name))
        return self.members

    def set_members(self, data):
        for row in data:
            if row[2] != '':
                return self.add_member(row[2])
        
    
    #def 

    def __init__(self, data):
        self.rows = data
        self.set_cleartime(self.rows[0])
        self.set_members(self.rows)




    