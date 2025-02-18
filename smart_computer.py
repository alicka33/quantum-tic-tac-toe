from copy import deepcopy
from random import choice
from board import Board, FIELDS_LIST


class SmartComputer:
    """ Class SmartComputer. Contains attributes:
        board: current board of a given size
        type: list
        collapse_dict:
            keys: numbers of fields
            values: fields with which the given field is entangled with
        type: dictionary
        spooky_marks_dict:
            keys: spooky marks
            values: fields in which the given spooky mark appears
        type: dictionary
        winner found: informs if winner was found or not
        type: bool
    """
    def __init__(self, board, collapse_dict, spooky_marks_dict):
        self.board = board
        self._collapse_dict = collapse_dict
        self._spooky_marks_dict = spooky_marks_dict
        self._winner_found = False

    @staticmethod
    def location_to_move():
        """Randomly chooses two locations to place the spooky marks"""
        if len(FIELDS_LIST) == 1:
            return FIELDS_LIST[0], FIELDS_LIST[0]
        first_choice = choice(FIELDS_LIST)
        second_choice = first_choice
        while second_choice == first_choice:
            second_choice = choice(FIELDS_LIST)
        return [first_choice, second_choice]

    def collapse(self, collapsing_fields, chosen_mark, current_board):
        """Collapses spooky marks into real marks"""
        current_spooky_marks_dict = deepcopy(self._spooky_marks_dict)
        location = collapsing_fields[0]
        for num_of_locations in range(len(current_spooky_marks_dict)):
            current_board[location - 1] = [chosen_mark]
            for mark in current_spooky_marks_dict:
                locations = current_spooky_marks_dict[mark]
                if location in locations:
                    locations.remove(location)
                current_spooky_marks_dict[mark] = locations
            if chosen_mark in current_spooky_marks_dict.keys():
                del current_spooky_marks_dict[chosen_mark]
            for mark in current_spooky_marks_dict:
                if len(current_spooky_marks_dict[mark]) == 1:
                    chosen_mark = mark
                    location = \
                        current_spooky_marks_dict[chosen_mark][0]
        return current_board

    def winning_process(self, current_baord):
        """Returns the potential winner of the game"""
        big_board = Board.convert_big_board(current_baord)
        diagonals = Board.diagonals(big_board)
        rows = Board.rows(big_board)
        columns = Board.columns(big_board)
        all_poss = Board.create_all_possibilietes(diagonals, rows,
                                                  columns)
        winners = Board.check_winners(all_poss)
        if winners:
            self._winner_found = True
            chosen_winner, w_points, l_points = \
                Board.choose_winner(winners)
            return (chosen_winner, w_points, l_points)
        return None

    @staticmethod
    def choose_collapse_randomly(marks):
        """Chooses randomly one of the two marks"""
        return choice(marks)

    def check_winner(self, result1, result2, first_mark, second_mark):
        """Returns the more advantageous mark for the smart computer"""
        if not result1 and not result2:
            return SmartComputer.choose_collapse_randomly([first_mark,
                                                          second_mark])
        if not result1:
            return second_mark if result2[0] == 'O' else first_mark
        elif not result2:
            return first_mark if result1[0] == 'O' else second_mark

        if result1[0] == result2[0]:
            if result1[0] == 'O':
                return first_mark if result1[1] > result2[1] else second_mark
            else:
                return first_mark if result1[1] < result2[1] else second_mark
        else:
            return first_mark if result1[0] == 'O' else second_mark

    def choose_collapse(self, collapsing_fields, collapse_spooky_marks_dict):
        """Handles all steps of choosing the better collapsing option"""
        current_board = deepcopy(self.board)
        first_mark = list(collapse_spooky_marks_dict[collapsing_fields[0]])[0]
        second_mark = list(collapse_spooky_marks_dict[collapsing_fields[0]])[1]
        collapsed_board1 = self.collapse(collapsing_fields, first_mark,
                                         current_board)
        current_board = deepcopy(self.board)
        collapsed_board2 = self.collapse(collapsing_fields, second_mark,
                                         current_board)
        result1 = \
            self.winning_process(collapsed_board1)
        result2 = \
            self.winning_process(collapsed_board2)
        chosen_mark = self.check_winner(result1, result2, first_mark,
                                        second_mark)
        return chosen_mark
