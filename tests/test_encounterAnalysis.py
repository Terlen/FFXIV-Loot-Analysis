from utils.encounterAnalysis import get_most_and_least_rolls, get_winning_rolls, get_mean_roll_value, get_median_roll_value, get_mode_roll_value, get_most_and_least_lost_rolls
from utils.encounter import Encounter, Item, Member, Roll

def get_instance_from_list_by_name(list, *args):
    nameList = [item.name for item in list]
    instances = [list[nameList.index(name)] for name in args]
    return tuple(instances)

class Test_get_most_and_least_rolls_Unit:
    
    test_data_item_no_tie = [
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

    test_data_item_tie_most_and_least = [
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

    test_data_item_tie_most = [
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
    
    test_data_item_tie_least = [
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
        test_encounter = Encounter(self.test_data_item_no_tie)
        items = get_instance_from_list_by_name(test_encounter.items, "Resplendent Stick", "Resplendent Pot")
        assert (items[0],items[1]) == get_most_and_least_rolls(test_encounter.items)
    def test_get_item_most_and_least_rolls_tie_most_and_least(self):
        test_encounter = Encounter(self.test_data_item_tie_most_and_least)
        assert (test_encounter.items, test_encounter.items) == get_most_and_least_rolls(test_encounter.items)
    def test_get_item_most_and_least_rolls_tie_most(self):
        test_encounter = Encounter(self.test_data_item_tie_most)
        items = get_instance_from_list_by_name(test_encounter.items,"Kugane Stick","Kugane Pot","Meaty Pot")
        assert ([items[0],items[1]], items[2]) == get_most_and_least_rolls(test_encounter.items)
    def test_get_item_most_and_least_rolls_tie_least(self):
        test_encounter = Encounter(self.test_data_item_tie_least)
        items = get_instance_from_list_by_name(test_encounter.items,"Kugane Stick","Tataru's Pot","Meaty Pot")
        assert (items[0], [items[1],items[2]]) == get_most_and_least_rolls(test_encounter.items)


    test_data_member_no_tie = [
            ['8-8-08', 'AddLoot', '', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'AddLoot', '', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Stick', 0, 1],  
            ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1], 
            ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1], 
            ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Resplendent Stick', 9, 1], 
            ['8-8-08', 'NeedLoot', 'Hien Cookiepouch', 'Resplendent Stick', 43, 1], 
            ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Resplendent Stick', 45, 1]
            ]

    test_data_member_tie_most_and_least = [
            ['8-8-08', 'AddLoot', '', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'AddLoot', '', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Stick', 0, 1],  
            ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1], 
            ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1],
            ['8-8-08', 'NeedLoot', 'Hien Fantasy', 'Resplendent Stick', 1, 1], 
            ['8-8-08', 'NeedLoot', 'Hien Cookiepouch', 'Resplendent Stick', 43, 1], 
            ['8-8-08', 'ObtainLoot', 'Hien Cookiepouch', 'Resplendent Stick', 43, 1]
            ]
    
    test_data_member_tie_most = [
            ['8-8-08', 'AddLoot', '', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'AddLoot', '', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Stick', 0, 1],  
            ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1],
            ['8-8-08', 'GreedLoot', 'Hien Cookiepouch', 'Resplendent Pot', 40, 1], 
            ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1], 
            ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Resplendent Stick', 9, 1], 
            ['8-8-08', 'NeedLoot', 'Hien Cookiepouch', 'Resplendent Stick', 43, 1], 
            ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Resplendent Stick', 45, 1]
            ]
    
    test_data_member_tie_least = [
            ['8-8-08', 'AddLoot', '', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'AddLoot', '', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Pot', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Fantasy', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Stick', 0, 1], 
            ['8-8-08', 'CastLoot', 'Hien Cookiepouch', 'Resplendent Stick', 0, 1],  
            ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1], 
            ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Resplendent Pot', 45, 1], 
            ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Resplendent Stick', 9, 1], 
            ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Resplendent Stick', 45, 1]
            ]

    def test_get_member_most_and_least_rolls_no_tie(self):
        test_encounter = Encounter(self.test_data_member_no_tie)
        members = get_instance_from_list_by_name(test_encounter.members,"Akiva Chocobo","Hien Cookiepouch","Hien Fantasy")
        assert (members[0], members[2]) == get_most_and_least_rolls(test_encounter.members)

    def test_get_member_most_and_least_rolls_tie_most_and_least(self):
        test_encounter = Encounter(self.test_data_member_tie_most_and_least)
        members = get_instance_from_list_by_name(test_encounter.members, "Akiva Chocobo","Hien Cookiepouch","Hien Fantasy")
        assert (test_encounter.members,test_encounter.members) == get_most_and_least_rolls(test_encounter.members)
    
    def test_get_member_most_and_least_rolls_tie_most(self):
        test_encounter = Encounter(self.test_data_member_tie_most)
        members = get_instance_from_list_by_name(test_encounter.members, "Akiva Chocobo","Hien Cookiepouch","Hien Fantasy")
        output = get_most_and_least_rolls(test_encounter.members)
        assert members[0],members[1] in output[0]
        assert members[2] == output[1]

    def test_get_member_most_and_least_rolls_tie_least(self):
        test_encounter = Encounter(self.test_data_member_tie_least)
        members = get_instance_from_list_by_name(test_encounter.members, "Akiva Chocobo","Hien Cookiepouch","Hien Fantasy")
        output = get_most_and_least_rolls(test_encounter.members)
        assert members[0] == output[0]
        assert members[2],members[1] in output[1]

class Test_get_winning_rolls:
    test_data = [
        ['8-8-08', 'AddLoot', '', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'AddLoot', '', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Cookiepouch', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Final', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Cookiepouch', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Final', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'NeedLoot', 'Karou Cookiepouch', "Tataru's Sword", 12, 1], 
        ['8-8-08', 'NeedLoot', 'Hien Final', "Tataru's Sword", 28, 1], 
        ['8-8-08', 'NeedLoot', 'Akiva Final', "Tataru's Sword", 30, 1], 
        ['8-8-08', 'ObtainLoot', 'Akiva Final', "Tataru's Sword", 30, 1], 
        ['8-8-08', 'NeedLoot', 'Karou Cookiepouch', 'Resplendent Scissors', 72, 1], 
        ['8-8-08', 'NeedLoot', 'Hien Final', 'Resplendent Scissors', 26, 1], 
        ['8-8-08', 'NeedLoot', 'Akiva Final', 'Resplendent Scissors', 92, 1], 
        ['8-8-08', 'ObtainLoot', 'Akiva Final', 'Resplendent Scissors', 92, 1]
        ]

    test_data_no_winners = [
        ['8-8-08', 'AddLoot', '', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'AddLoot', '', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Cookiepouch', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Final', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Cookiepouch', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Final', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', 'Resplendent Scissors', 0, 1], 
        ]
    
    def test_get_winning_rolls(self):
        test_encounter = Encounter(self.test_data)
        expected_winners = [roll for roll in test_encounter.rolls if roll.win]
        assert expected_winners == get_winning_rolls(test_encounter)

    def test_get_winning_rolls_no_winners(self):
        test_encounter = Encounter(self.test_data_no_winners)
        expected_winners = []
        assert expected_winners == get_winning_rolls(test_encounter)

class Test_get_mean_roll_value:
    test_data = [
        ['8-8-08', 'AddLoot', '', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'AddLoot', '', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'CastLoot', 'Alphinaud Cookiepouch', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'CastLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Kugane Lance', 94, 3], 
        ['8-8-08', 'GreedLoot', 'Alphinaud Cookiepouch', 'Kugane Lance', 12, 3], 
        ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Kugane Lance', 94, 3], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Rusty Stick', 53, 3], 
        ['8-8-08', 'NeedLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 61, 3], 
        ['8-8-08', 'ObtainLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 61, 3]
        ]

    test_data_no_rolls = [
        ['8-8-08', 'AddLoot', '', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'AddLoot', '', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Cookiepouch', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Final', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Cookiepouch', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Final', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', 'Resplendent Scissors', 0, 1], 
        ]
    
    def test_get_mean_roll(self):
        test_encounter = Encounter(self.test_data)
        assert 55.0 == get_mean_roll_value(test_encounter)
    
    def test_get_mean_roll_no_rolls(self):
        test_encounter = Encounter(self.test_data_no_rolls)
        assert 0 == get_mean_roll_value(test_encounter)

class Test_get_median_roll_value:
    test_data = [
        ['8-8-08', 'AddLoot', '', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'AddLoot', '', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'CastLoot', 'Alphinaud Cookiepouch', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'CastLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Kugane Lance', 94, 3], 
        ['8-8-08', 'GreedLoot', 'Alphinaud Cookiepouch', 'Kugane Lance', 12, 3], 
        ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Kugane Lance', 94, 3], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Rusty Stick', 53, 3], 
        ['8-8-08', 'NeedLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 61, 3], 
        ['8-8-08', 'ObtainLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 61, 3]
        ]

    test_data_no_rolls = [
        ['8-8-08', 'AddLoot', '', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'AddLoot', '', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Cookiepouch', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Final', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', "Tataru's Sword", 0, 1], 
        ['8-8-08', 'CastLoot', 'Karou Cookiepouch', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Hien Final', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', 'Resplendent Scissors', 0, 1], 
        ]
    
    def test_get_median_roll(self):
        test_encounter = Encounter(self.test_data)
        assert 57.0 == get_median_roll_value(test_encounter)
    
    def test_get_median_roll_no_rolls(self):
        test_encounter = Encounter(self.test_data_no_rolls)
        assert 0 == get_median_roll_value(test_encounter)

class Test_get_mode_roll_value:
    test_data_no_mode = [
        ['8-8-08', 'AddLoot', '', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'AddLoot', '', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'CastLoot', 'Alphinaud Cookiepouch', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'CastLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Kugane Lance', 94, 3], 
        ['8-8-08', 'GreedLoot', 'Alphinaud Cookiepouch', 'Kugane Lance', 12, 3], 
        ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Kugane Lance', 94, 3], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Rusty Stick', 53, 3], 
        ['8-8-08', 'NeedLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 61, 3], 
        ['8-8-08', 'ObtainLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 61, 3]
        ]
    
    test_data_one_mode = [
        ['8-8-08', 'AddLoot', '', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'AddLoot', '', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'CastLoot', 'Alphinaud Cookiepouch', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'CastLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Kugane Lance', 94, 3], 
        ['8-8-08', 'GreedLoot', 'Alphinaud Cookiepouch', 'Kugane Lance', 12, 3], 
        ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Kugane Lance', 94, 3], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Rusty Stick', 94, 3], 
        ['8-8-08', 'NeedLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 61, 3], 
        ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Rusty Stick', 94, 3]
        ]
    
    test_data_multi_mode = [
        ['8-8-08', 'AddLoot', '', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'AddLoot', '', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'CastLoot', 'Alphinaud Cookiepouch', 'Kugane Lance', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'CastLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 0, 3], 
        ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Kugane Lance', 94, 3], 
        ['8-8-08', 'GreedLoot', 'Alphinaud Cookiepouch', 'Kugane Lance', 61, 3], 
        ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Kugane Lance', 94, 3], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Rusty Stick', 94, 3], 
        ['8-8-08', 'NeedLoot', 'Alphinaud Cookiepouch', 'Rusty Stick', 61, 3], 
        ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Rusty Stick', 94, 3]
        ]

    def test_get_mode_roll_value_no_mode(self):
        test_encounter = Encounter(self.test_data_no_mode)
        assert [] == get_mode_roll_value(test_encounter)
    
    def test_get_mode_roll_value_one_mode(self):
        test_encounter = Encounter(self.test_data_one_mode)
        assert [94] == get_mode_roll_value(test_encounter)
    
    def test_get_mode_roll_value_multi_mode(self):
        test_encounter = Encounter(self.test_data_multi_mode)
        assert 61,94 in get_mode_roll_value(test_encounter)

class Test_get_most_and_least_lost_rolls:
    test_data_need_and_greed_no_tie = [
        ['8-8-08', 'AddLoot', '', "Tataru's Stick", 0, 1], 
        ['8-8-08', 'AddLoot', '', 'Rusty Pot', 0, 3], 
        ['8-8-08', 'AddLoot', '', 'Meaty Pot', 0, 3], 
        ['8-8-08', 'AddLoot', '', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Yda Chocobo', "Tataru's Stick", 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', "Tataru's Stick", 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', "Tataru's Stick", 0, 1], 
        ['8-8-08', 'CastLoot', 'Yda Final', "Tataru's Stick", 0, 1], 
        ['8-8-08', 'CastLoot', 'Yda Chocobo', 'Rusty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Final', 'Rusty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Rusty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Yda Final', 'Rusty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Yda Chocobo', 'Meaty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Final', 'Meaty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Meaty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Yda Final', 'Meaty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Yda Chocobo', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Yda Final', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'NeedLoot', 'Yda Chocobo', "Tataru's Stick", 73, 1], 
        ['8-8-08', 'NeedLoot', 'Akiva Final', "Tataru's Stick", 71, 1], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', "Tataru's Stick", 44, 1], 
        ['8-8-08', 'NeedLoot', 'Yda Final', "Tataru's Stick", 99, 1], 
        ['8-8-08', 'ObtainLoot', 'Yda Final', "Tataru's Stick", 99, 1], 
        ['8-8-08', 'GreedLoot', 'Yda Chocobo', 'Rusty Pot', 72, 3], 
        ['8-8-08', 'GreedLoot', 'Akiva Final', 'Rusty Pot', 36, 3], 
        ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Rusty Pot', 16, 3], 
        ['8-8-08', 'GreedLoot', 'Yda Final', 'Rusty Pot', 73, 3], 
        ['8-8-08', 'ObtainLoot', 'Yda Final', 'Rusty Pot', 73, 3], 
        ['8-8-08', 'NeedLoot', 'Yda Chocobo', 'Meaty Pot', 53, 3], 
        ['8-8-08', 'NeedLoot', 'Akiva Final', 'Meaty Pot', 47, 3], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Meaty Pot', 50, 3], 
        ['8-8-08', 'NeedLoot', 'Yda Final', 'Meaty Pot', 38, 3], 
        ['8-8-08', 'ObtainLoot', 'Yda Chocobo', 'Meaty Pot', 53, 3], 
        ['8-8-08', 'NeedLoot', 'Yda Chocobo', 'Resplendent Scissors', 32, 1], 
        ['8-8-08', 'NeedLoot', 'Akiva Final', 'Resplendent Scissors', 92, 1], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Resplendent Scissors', 10, 1], 
        ['8-8-08', 'NeedLoot', 'Yda Final', 'Resplendent Scissors', 45, 1], 
        ['8-8-08', 'ObtainLoot', 'Akiva Final', 'Resplendent Scissors', 92, 1]
        ]
    
    test_data_need_no_tie = [
        ['8-8-08', 'AddLoot', '', "Tataru's Stick", 0, 1], 
        ['8-8-08', 'AddLoot', '', 'Rusty Pot', 0, 3], 
        ['8-8-08', 'AddLoot', '', 'Meaty Pot', 0, 3], 
        ['8-8-08', 'AddLoot', '', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', "Tataru's Stick", 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', "Tataru's Stick", 0, 1], 
        ['8-8-08', 'CastLoot', 'Yda Final', "Tataru's Stick", 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Final', 'Rusty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Rusty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Yda Final', 'Rusty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Final', 'Meaty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Meaty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Yda Final', 'Meaty Pot', 0, 3], 
        ['8-8-08', 'CastLoot', 'Akiva Final', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Akiva Chocobo', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'CastLoot', 'Yda Final', 'Resplendent Scissors', 0, 1], 
        ['8-8-08', 'NeedLoot', 'Akiva Final', "Tataru's Stick", 71, 1], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', "Tataru's Stick", 44, 1], 
        ['8-8-08', 'NeedLoot', 'Yda Final', "Tataru's Stick", 99, 1], 
        ['8-8-08', 'ObtainLoot', 'Yda Final', "Tataru's Stick", 99, 1], 
        ['8-8-08', 'GreedLoot', 'Akiva Final', 'Rusty Pot', 36, 3], 
        ['8-8-08', 'GreedLoot', 'Akiva Chocobo', 'Rusty Pot', 16, 3], 
        ['8-8-08', 'GreedLoot', 'Yda Final', 'Rusty Pot', 73, 3], 
        ['8-8-08', 'ObtainLoot', 'Yda Final', 'Rusty Pot', 73, 3], 
        ['8-8-08', 'NeedLoot', 'Akiva Final', 'Meaty Pot', 47, 3], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Meaty Pot', 50, 3], 
        ['8-8-08', 'NeedLoot', 'Yda Final', 'Meaty Pot', 38, 3], 
        ['8-8-08', 'ObtainLoot', 'Akiva Chocobo', 'Meaty Pot', 50, 3], 
        ['8-8-08', 'NeedLoot', 'Akiva Final', 'Resplendent Scissors', 45, 1], 
        ['8-8-08', 'NeedLoot', 'Akiva Chocobo', 'Resplendent Scissors', 10, 1], 
        ['8-8-08', 'NeedLoot', 'Yda Final', 'Resplendent Scissors', 92, 1], 
        ['8-8-08', 'ObtainLoot', 'Yda Final', 'Resplendent Scissors', 92, 1]
        ]

    def test_get_most_and_least_lost_rolls_need_and_greed_no_tie(self):
        test_encounter = Encounter(self.test_data_need_and_greed_no_tie)
        members = get_instance_from_list_by_name(test_encounter.members,'Yda Chocobo','Akiva Final','Akiva Chocobo','Yda Final')
        
        assert ([members[3]], [members[2]]) == get_most_and_least_lost_rolls(test_encounter)
    
    # def test_get_most_and_least_lost_rolls_need_no_tie(self):
    #     test_encounter = Encounter(self.test_data_need_no_tie)
    #     members = get_instance_from_list_by_name(test_encounter.members,'Akiva Final','Akiva Chocobo','Yda Final')
    #     assert ((members[0],3),(members[2],1)) == get_most_and_least_lost_rolls(test_encounter)

    
