from utils.encounterAnalysis import get_item_most_and_least_rolls
from utils.encounter import Encounter, Item, Member, Roll
from testdatagenerator import random_data_gen
from utils.dataReader import encounterSplitter



class Test_get_item_most_and_least_rolls_Unit:
    
    test_data_no_tie = [
            ['8-8-08', 'AddLoot', '', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'AddLoot', '', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Stick', 0, 1],  
            ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1], 
            ['8-8-08', 'GreedLoot', 'Hien Cookiepouch', 'Resplendent Pot', 41, 1], 
            ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1], 
            ['8-8-08', 'NeedLoot', 'Hien Fantasy', 'Resplendent Stick', 25, 1], 
            ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Resplendent Stick', 9, 1], 
            ['8-8-08', 'NeedLoot', 'Hien Cookiepouch', 'Resplendent Stick', 43, 1], 
            ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Resplendent Stick', 45, 1]
            ]

    test_data_tie_most_and_least = [
        ['8-8-08', 'AddLoot', '', 'Resplendent Pot', 0, 1], 
        ['8-8-08', 'AddLoot', '', 'Resplendent Stick', 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Pot', 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Pot', 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Pot', 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Stick', 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Stick', 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Stick', 0, 1], 
        ['8-8-08', 'GreedLoot', 'Hien Fantasy', 'Resplendent Pot', 13, 1], 
        ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1], 
        ['8-8-08', 'GreedLoot', 'Hien Cookiepouch', 'Resplendent Pot', 41, 1], 
        ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1], 
        ['8-8-08', 'NeedLoot', 'Hien Fantasy', 'Resplendent Stick', 25, 1], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Resplendent Stick', 9, 1], 
        ['8-8-08', 'NeedLoot', 'Hien Cookiepouch', 'Resplendent Stick', 43, 1], 
        ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Resplendent Stick', 45, 1]
        ]

    test_data_tie_most = [
        ['8-8-08', 'AddLoot', '', 'Kugane Stick', 0, 1], 
        ['8-8-08', 'AddLoot', '', 'Kugane Pot', 0, 1], 
        ['8-8-08', 'AddLoot', '', "Tataru's Pot", 0, 2], 
        ['8-8-08', 'AddLoot', '', 'Meaty Pot', 0, 2], 
        ['8-8-08', 'CastLoot', 'Karou Tonberry', 'Kugane Stick', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Final', 'Kugane Stick', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Tonberry', 'Kugane Pot', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Final', 'Kugane Pot', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Tonberry', "Tataru's Pot", 0, 2], 
        ['8-8-08', 'CastLoot', 'Karou Final', "Tataru's Pot", 0, 2], 
        ['8-8-08', 'CastLoot', 'Karou Tonberry', 'Meaty Pot', 0, 2], 
        ['8-8-08', 'CastLoot', 'Karou Final', 'Meaty Pot', 0, 2], 
        ['8-8-08', 'GreedLoot', 'Karou Tonberry', 'Kugane Stick', 45, 1], 
        ['8-8-08', 'GreedLoot', 'Karou Final', 'Kugane Stick', 30, 1], 
        ['8-8-08', 'ObtainLoot', 'Karou Tonberry', 'Kugane Stick', 45, 1], 
        ['8-8-08', 'NeedLoot', 'Karou Tonberry', 'Kugane Pot', 46, 1], 
        ['8-8-08', 'NeedLoot', 'Karou Final', 'Kugane Pot', 41, 1], 
        ['8-8-08', 'ObtainLoot', 'Karou Tonberry', 'Kugane Pot', 46, 1], 
        ['8-8-08', 'NeedLoot', 'Karou Final', "Tataru's Pot", 94, 2], 
        ['8-8-08', 'ObtainLoot', 'Karou Final', "Tataru's Pot", 94, 2], 
        ]
    
    test_data_tie_least = [
        ['8-8-08', 'AddLoot', '', 'Kugane Stick', 0, 1], 
        ['8-8-08', 'AddLoot', '', 'Kugane Pot', 0, 1], 
        ['8-8-08', 'AddLoot', '', "Tataru's Pot", 0, 2], 
        ['8-8-08', 'AddLoot', '', 'Meaty Pot', 0, 2], 
        ['8-8-08', 'CastLoot', 'Karou Tonberry', 'Kugane Stick', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Final', 'Kugane Stick', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Tonberry', 'Kugane Pot', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Final', 'Kugane Pot', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Tonberry', "Tataru's Pot", 0, 2], 
        ['8-8-08', 'CastLoot', 'Karou Final', "Tataru's Pot", 0, 2], 
        ['8-8-08', 'CastLoot', 'Karou Tonberry', 'Meaty Pot', 0, 2], 
        ['8-8-08', 'CastLoot', 'Karou Final', 'Meaty Pot', 0, 2], 
        ['8-8-08', 'GreedLoot', 'Karou Tonberry', 'Kugane Stick', 45, 1], 
        ['8-8-08', 'GreedLoot', 'Karou Final', 'Kugane Stick', 30, 1], 
        ['8-8-08', 'ObtainLoot', 'Karou Tonberry', 'Kugane Stick', 45, 1], 
        ['8-8-08', 'NeedLoot', 'Karou Tonberry', 'Kugane Pot', 46, 1], 
        ['8-8-08', 'ObtainLoot', 'Karou Tonberry', 'Kugane Pot', 46, 1], 
        ]

    def test_get_item_most_and_least_rolls_no_tie(self):
        test_encounter = Encounter(self.test_data_no_tie)
        item_names = [item.name for item in test_encounter.items]
        assert (test_encounter.items[item_names.index("Resplendent Stick")],test_encounter.items[item_names.index("Resplendent Pot")]) == get_item_most_and_least_rolls(test_encounter)
    def test_get_item_most_and_least_rolls_tie_most_and_least(self):
        test_encounter = Encounter(self.test_data_tie_most_and_least)
        assert (test_encounter.items, test_encounter.items) == get_item_most_and_least_rolls(test_encounter)
    def test_get_item_most_and_least_rolls_tie_most(self):
        test_encounter = Encounter(self.test_data_tie_most)
        item_names = [item.name for item in test_encounter.items]
        assert ([test_encounter.items[item_names.index("Kugane Stick")],test_encounter.items[item_names.index("Kugane Pot")]], test_encounter.items[item_names.index("Meaty Pot")]) == get_item_most_and_least_rolls(test_encounter)
    def test_get_item_most_and_least_rolls_tie_least(self):
        test_encounter = Encounter(self.test_data_tie_least)
        item_names = [item.name for item in test_encounter.items]
        assert (test_encounter.items[item_names.index("Kugane Stick")], [test_encounter.items[item_names.index("Tataru's Pot")],test_encounter.items[item_names.index("Meaty Pot")]]) == get_item_most_and_least_rolls(test_encounter)