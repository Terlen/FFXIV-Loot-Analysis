from utils.encounterAnalysis import get_item_most_rolls, get_item_fewest_rolls
from utils.encounter import Encounter, Item, Member, Roll
from testdatagenerator import random_item_gen, random_roll_gen



class Test_get_item_most_rolls_Unit:
    pass
    # items = [random_item_gen(),random_item_gen()]

    # items[0].rolls.append(random_roll_gen(1,1))
    # items[0].rolls.append(random_roll_gen(1,0))

    # items[1].rolls.append(random_roll_gen(0, 1))
    # items[1].rolls.append(random_roll_gen(0,0))
    # items[1].rolls.append(random_roll_gen(0,0))

    # encounter = Encounter([['18:00', 'AddLoot', '','Stick',0,1], ['18:00', 'GreedLoot', 'Test','Stick',20,1]])
    # encounter.items = items

    # def test_get_item_most_rolls(self):
    #     assert get_item_most_rolls(self.encounter) == self.items[1]

    # def test_get_item_fewest_rolls(self):
    #     assert get_item_fewest_rolls(self.encounter) == self.items[0]