from termcolor import colored


ROUNDS = 9
FIELDS_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9]
NUMBER_SPOOKY_MARKS = 2
BOARD_SIZE = 3
COLOR = {'X': 'red', 'O': 'green'}


class Board:
    """ Class Board. Contains attributes:
        board: board of a given size
        type: list
        collapse_dict:
            keys: numbers of fields
            values: fields with which the given field is entangled with
        type: dictionary
        spooky_marks_dict:
            keys: spooky marks
            values: fields in which the given spooky mark appears
        type: dictionary
        fields_dict:
            keys: numbers of fields
            values: spooky marks which appear in the given field
        type: dictionary
        winner found: informs if winner was found or not
        type: bool
    """
    def __init__(self):
        self._board = [['  ' for field in range(BOARD_SIZE ** 2)]
                       for small_board in range(BOARD_SIZE ** 2)]
        self._collapse_dict = {}
        self._spooky_marks_dict = {}
        self._fields_dict = {}
        self._winner_found = False

    def board(self):
        return self._board

    def collapse_dict(self):
        return self._collapse_dict

    def spooky_marks_dict(self):
        return self._spooky_marks_dict

    def fields_dict(self):
        return self._fields_dict

    def set_small_board(self, location, round, mark):
        """Places the spooky mark in a given field"""
        self._board[location - 1][round - 1] = mark

    def set_fields_dict(self, location, mark):
        """Sets fields_dict:
           Keys: field numbers
           Values: spooky marks in given field
        """
        list_of_spooky_marks = []
        if location not in self.fields_dict():
            list_of_spooky_marks.append(mark)
            self.fields_dict()[location] = list_of_spooky_marks
        else:
            list_of_spooky_marks = self.fields_dict()[location]
            list_of_spooky_marks.append(mark)
            self.fields_dict()[location] = list_of_spooky_marks

    def placing_spooky_marks(self, round, mark, locations):
        self.set_fields_dict(locations[0], mark)
        self.set_fields_dict(locations[1], mark)
        self.set_small_board(locations[0], round, mark)
        self.set_small_board(locations[1], round, mark)

    def extend_collapse_dict(self, location1, location2):
        """ Extends self._collapse_dictionary.
            Keys: field number
            Values: fields its connected with"""
        entangled_list = []
        if location1 not in self._collapse_dict.keys():
            entangled_list.append(location2)
            self._collapse_dict[location1] = entangled_list
        else:
            entangled_list = self._collapse_dict[location1]
            entangled_list.append(location2)
            self._collapse_dict[location1] = entangled_list

    def set_collapse_dict(self, locations):
        """ Extendes collpase_dict by two new keys -
        locations where the spooky marks have been placed"""
        self.extend_collapse_dict(locations[0], locations[1])
        self.extend_collapse_dict(locations[1], locations[0])

    def keys_where_quantity_min_2(self):
        """Returns the locations which are entangled
           with at least two other fields"""
        location_keys = []
        for location in self._collapse_dict:
            if len(self._collapse_dict[location]) >= 2:
                location_keys.append(location)
        return location_keys

    def all_entanglements_for_location_keys(self, location_keys):
        """Returns a list of all fields with which the fields
           in location_keys are entangled """
        entanglements = []
        for location in location_keys:
            entanglements.extend(self._collapse_dict[location])
        return entanglements

    def get_all_spooky_marks_in_given_fields(self, collapsing_fields):
        """Returns a list of all spooky marks which are in collpasing fields"""
        list_of_all_spooky_marks = []
        for field in collapsing_fields:
            list_of_all_spooky_marks.extend(self.fields_dict()[field])
        return list_of_all_spooky_marks

    @staticmethod
    def if_enough_marks_repeat(all_spooky_marks, collapsing_fields):
        """Checks if the number of repeted spooky marks
           equals the number of collapsing fields"""
        repeated_spooky_marks = [mark for mark in set(all_spooky_marks)
                                 if all_spooky_marks.count(mark) == 2]
        return len(repeated_spooky_marks) == len(collapsing_fields)

    @staticmethod
    def find_suspected_fields(location_keys, entanglements):
        """Returns a list of fields
           which appeard in entanglements 2 times or more"""
        return [location for location in location_keys
                if entanglements.count(location) >= 2]

    def verify_suspected_fields(self, suspected_fields):
        """Returns a list of fields from suspected_fields
           which are connected with 2 fields or more"""
        collapsing_fields = []
        for field in suspected_fields:
            count = 0
            connected_fields = self.collapse_dict()[field]
            for connected_field in connected_fields:
                if connected_field in suspected_fields:
                    count += 1
            if count >= 2:
                collapsing_fields.append(field)
        return collapsing_fields

    @staticmethod
    def collapsing_requirements_met(collapsing_fields, if_enough_repeated):
        """Checks if collapsing requirements are met"""
        return len(collapsing_fields) >= 2 and if_enough_repeated

    def find_collapsed_fields(self, location_keys, entanglements):
        """Finds fields to collapse"""
        suspected_fields = Board.find_suspected_fields(location_keys,
                                                       entanglements)
        collapsing_fields = self.verify_suspected_fields(suspected_fields)
        all_sppoky_marks = \
            self.get_all_spooky_marks_in_given_fields(collapsing_fields)
        if_enought_repeated = \
            Board.if_enough_marks_repeat(all_sppoky_marks, collapsing_fields)
        return collapsing_fields if Board.collapsing_requirements_met(
               collapsing_fields, if_enought_repeated) else []

    def set_spooky_marks_dictionary(self, mark, locations):
        self._spooky_marks_dict[mark] = locations

    def spooky_marks_in_collapse(self, collapsing_fields):
        """Returns the marks which take part in collapse"""
        all_marks = \
            self.get_all_spooky_marks_in_given_fields(collapsing_fields)
        return [mark for mark in set(all_marks) if all_marks.count(mark) == 2]

    def collapse_spooky_marks_field_dict(self, collapsing_fields,
                                         collapse_spooky_marks):
        """Creates a dictionary of fields and marks taking part in collapse"""
        collapse_spooky_marks_dict = {}
        for field in collapsing_fields:
            marks_in_field = self.fields_dict()[field]
            collapse_spooky_marks_dict[field] = \
                set(marks_in_field).intersection(collapse_spooky_marks)
        return collapse_spooky_marks_dict

    def collapse(self, collapsing_fields, chosen_mark):
        """Sets the board after collapse """
        location = collapsing_fields[0]
        for number_of_locations in range(len(self._spooky_marks_dict)):
            self.board()[location - 1] = [chosen_mark]
            if location in FIELDS_LIST:
                FIELDS_LIST.remove(location)
            self._spooky_marks_dict[chosen_mark] = []
            if location in self._collapse_dict:
                del self._collapse_dict[location]
            if location in collapsing_fields:
                collapsing_fields.remove(location)
            for mark in self._spooky_marks_dict:
                locations = self._spooky_marks_dict[mark]
                if location in locations:
                    locations.remove(location)
                self._spooky_marks_dict[mark] = locations
            for mark in self._spooky_marks_dict:
                if len(self._spooky_marks_dict[mark]) == 1:
                    chosen_mark = mark
                    location = self._spooky_marks_dict[chosen_mark][0]

    def handling_collapsing_fields(self, enemy, collapsing_fields):
        """Handles the collapse"""
        collapse_spooky_marks = \
            self.spooky_marks_in_collapse(collapsing_fields)
        collapse_spooky_marks_dict = \
            self.collapse_spooky_marks_field_dict(collapsing_fields,
                                                  collapse_spooky_marks)
        choosen_mark = \
            enemy.choose_collapse(collapsing_fields,
                                  collapse_spooky_marks_dict)
        self.collapse(collapsing_fields, choosen_mark)

    def collapsing_process(self, enemy, locations, mark):
        """Handles all steps of the collapsing process"""
        self.set_spooky_marks_dictionary(mark, locations)
        self.set_collapse_dict(locations)
        location_keys = self.keys_where_quantity_min_2()
        entanglements = self.all_entanglements_for_location_keys(location_keys)
        collapsing_fields = \
            self.find_collapsed_fields(location_keys, entanglements)
        if collapsing_fields:
            self.handling_collapsing_fields(enemy, collapsing_fields)
            self.print_board()

    @staticmethod
    def is_field_collapsed(field):
        """Checks if field has been collapsed"""
        return len(field) == 1

    @staticmethod
    def convert_big_board(board):
        """Convertes big board"""
        big_board = []
        for field in board:
            if Board.is_field_collapsed(field):
                big_board.append(field[0])
            else:
                big_board.append(" 0")
        return big_board

    @staticmethod
    def diagonals(big_board):
        """Returns the marks located on the diagonals of the board"""
        diagonals = []
        diagonals.append(big_board[::BOARD_SIZE + 1])
        diagonals.append(big_board[BOARD_SIZE - 1:
                                   BOARD_SIZE ** 2 - 1: BOARD_SIZE - 1])
        return diagonals

    @staticmethod
    def rows(big_board):
        """Returns the marks located in the rows of the board"""
        rows = []
        for row_index in range(BOARD_SIZE):
            starting_index = row_index * BOARD_SIZE
            rows.append(big_board[starting_index: starting_index + BOARD_SIZE])
        return rows

    @staticmethod
    def columns(big_board):
        """Returns the marks located in the columns of the board"""
        columns = []
        for column_index in range(BOARD_SIZE):
            columns.append(big_board[column_index::BOARD_SIZE])
        return columns

    @staticmethod
    def create_all_possibilietes(diagonals, rows, columns):
        """Returns a list of all possible winning sequences"""
        all_possibilities = []
        all_possibilities.extend(diagonals)
        all_possibilities.extend(rows)
        all_possibilities.extend(columns)
        return all_possibilities

    @staticmethod
    def check_winners(all_possibilieties):
        """Returns all winning sequences"""
        winners = []
        for poss in all_possibilieties:
            max_round = max(poss[0][1], poss[1][1], poss[2][1])
            if poss[0][0] == poss[1][0] == poss[2][0] and poss[0][0] != ' ':
                winners.append((poss[0][0], int(max_round)))
        return winners

    @staticmethod
    def choose_winner(winners):
        """Chooses winner between all winning sequences"""
        winner_points = 0
        loser_points = 0
        chosen_winner = ' '
        if len(winners) == 1:
            chosen_winner = winners[0][0]
            winner_points = 1
        elif len(winners) == 2:
            if winners[0][0] != winners[1][0]:
                winner_points = 1
                loser_points = 0.5
                if winners[0][1] < winners[1][1]:
                    chosen_winner = winners[0][0]
                else:
                    chosen_winner = winners[1][0]
            else:
                chosen_winner = winners[0][0]
                if winners[0][1] == winners[1][1]:
                    winner_points = 2
                else:
                    winner_points = 1.5
        return chosen_winner, winner_points, loser_points

    @staticmethod
    def print_winner(chosen_winner, winner_points, loser_points):
        """Prints the winner"""
        message1 = f'Player {chosen_winner} won the game '
        message2 = f'with a score {winner_points} : {loser_points}'
        message = message1 + message2
        print(message)

    @staticmethod
    def print_tie():
        print("It's a tie!")

    def winning_process(self):
        """Handles all steps of the winning process"""
        big_board = Board.convert_big_board(self._board)
        diagonals = Board.diagonals(big_board)
        rows = Board.rows(big_board)
        columns = Board.columns(big_board)
        all_poss = Board.create_all_possibilietes(diagonals, rows, columns)
        winners = Board.check_winners(all_poss)
        if winners:
            self._winner_found = True
            chosen_winner, w_points, l_points = Board.choose_winner(winners)
            self.print_winner(chosen_winner, w_points, l_points)

    def game(self, player, enemy):
        """Handles all the steps of the game"""
        self.print_board()
        for round in range(1, ROUNDS + 1):
            if not self._winner_found:
                if round % 2 == 1:
                    mark = 'X' + str(round)
                    locations = player.location_to_move()
                    self.placing_spooky_marks(round, mark, locations)
                    self.print_board()
                    self.collapsing_process(enemy, locations, mark)
                else:
                    mark = 'O' + str(round)
                    locations = enemy.location_to_move()
                    self.placing_spooky_marks(round, mark, locations)
                    self.print_board()
                    self.collapsing_process(player, locations, mark)
                self.winning_process()
        if not self._winner_found:
            self.print_tie()

    def print_board(self):
        """Prints the current state of the board"""
        for board_row in range(BOARD_SIZE):
            print('==================================================')
            small_boards = self.board()[board_row * 3: board_row * 3 + 3]
            for row in range(BOARD_SIZE):
                row_str = ''
                for small_board in small_boards:
                    if len(small_board) > 1:
                        small_board_row = small_board[row * 3: row * 3 + 3]
                        message1 = f'|| {small_board_row[0]} | '
                        message2 = f'{small_board_row[1]} | '
                        message3 = f'{small_board_row[2]} '
                        small_board_str = message1 + message2 + message3
                    else:
                        if row == 1:
                            small_board = [colored(small_board[0],
                                           COLOR[small_board[0][0]])]
                            small_board_str = \
                                f'||    | {small_board[0]} |    '
                        else:
                            small_board_str = '||    |    |    '
                    row_str += small_board_str
                print(row_str + '||')
        print('==================================================')
