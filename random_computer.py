from random import choice
from board import FIELDS_LIST


class RandomComputer:
    @staticmethod
    def location_to_move():
        """Randomly chooses two locations to place spooky marks"""
        if len(FIELDS_LIST) == 1:
            return FIELDS_LIST[0], FIELDS_LIST[0]
        first_choice = choice(FIELDS_LIST)
        second_choice = first_choice
        while second_choice == first_choice:
            second_choice = choice(FIELDS_LIST)
        return [first_choice, second_choice]

    @staticmethod
    def choose_collapse(collapsing_fields, collapse_spooky_marks_dict):
        """"Randomly chooses which of the two given spooky marks
            should be collapsed in the given field"""
        list_of_marks = list(collapse_spooky_marks_dict[collapsing_fields[0]])
        return choice(list_of_marks)
