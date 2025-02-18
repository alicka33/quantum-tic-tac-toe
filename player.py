from board import FIELDS_LIST


class Player:
    """"Class Player. Contains attributes:
        name: the name of the player
        type: str
    """
    def __init__(self, name='player'):
        self._name = name

    def name(self):
        return self._name

    def set_name(self, new_name):
        """Sets the name of the player"""
        self._name = new_name

    @staticmethod
    def fields_list_to_str(list_of_fields):
        """Convertes a list of int into a list of str"""
        return [str(field) for field in list_of_fields]

    @staticmethod
    def valid_locations(locations, fields_list):
        """Checks if given locations are valid"""
        if not (len(locations) == 2
                and locations[0] in fields_list
                and locations[1] in fields_list):
            return False
        return locations[0] != locations[1] if len(fields_list) != 1 else True

    def location_to_move(self):
        """Allows the player to input the locations of the spooky marks"""
        locations = \
            input("Please input the numbers of the fields: ").replace(' ', '')
        fields_list = Player.fields_list_to_str(FIELDS_LIST)
        if Player.valid_locations(locations, fields_list):
            return [int(locations[0]), int(locations[1])]
        else:
            return self.location_to_move()

    def choose_collapse(self, collapsing_fields, collapse_spooky_marks_dict):
        """Allows the player to choose the spooky mark which should
           be collapsed in the given field"""
        list_of_marks = collapse_spooky_marks_dict[collapsing_fields[0]]
        message1 = "To collapse please choose one of the marks "
        message2 = f"{list_of_marks} in field {collapsing_fields[0]}: "
        message = message1 + message2
        choosen_one = input(message).upper().replace(' ', '')
        if choosen_one in list_of_marks:
            return choosen_one
        else:
            return self.choose_collapse(collapsing_fields,
                                        collapse_spooky_marks_dict)
