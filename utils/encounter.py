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


class Encounter:
    def set_cleartime(self, firstrow):
        self.cleartime = firstrow[0]
    
    def set_members(self, data):
        self.members = set()
        for row in data:
            if row[2] != '':
                self.members.add(row[2])
    
    # def 

    def __init__(self, data):
        self.rows = data
        self.set_cleartime(self.rows[0])




    