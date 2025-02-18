from smart_computer import SmartComputer
from board import Board
from copy import deepcopy


def test_location_to_move(monkeypatch):
    def always_choose_2(some_list):
        return [2, 4]
    tested_method = 'smart_computer.SmartComputer.location_to_move'
    monkeypatch.setattr(tested_method, always_choose_2)
    board = Board()
    smart_computer = SmartComputer(board.board(), board.collapse_dict(),
                                   board.spooky_marks_dict())
    assert smart_computer.location_to_move() == [2, 4]


def test_collapse():
    board = Board()
    board.set_collapse_dict([5, 3])
    board.set_collapse_dict([4, 5])
    board.set_collapse_dict([4, 6])
    board.set_collapse_dict([4, 3])
    board.set_fields_dict(5, 'X1')
    board.set_fields_dict(3, 'X1')
    board.set_fields_dict(4, 'O2')
    board.set_fields_dict(5, 'O2')
    board.set_fields_dict(4, 'X3')
    board.set_fields_dict(6, 'X3')
    board.set_fields_dict(4, 'O4')
    board.set_fields_dict(3, 'O4')
    board.set_small_board(5, 1, 'X1')
    board.set_small_board(3, 1, 'X1')
    board.set_small_board(4, 2, 'O2')
    board.set_small_board(5, 2, 'O2')
    board.set_small_board(4, 3, 'X3')
    board.set_small_board(6, 3, 'X3')
    board.set_small_board(4, 4, 'O4')
    board.set_small_board(3, 4, 'O4')
    board.set_spooky_marks_dictionary('X1', [5, 3])
    board.set_spooky_marks_dictionary('O2', [4, 5])
    board.set_spooky_marks_dictionary('X3', [4, 6])
    board.set_spooky_marks_dictionary('O4', [4, 3])
    location_keys = board.keys_where_quantity_min_2()
    entanglements = board.all_entanglements_for_location_keys(location_keys)
    suspected_fields = board.find_suspected_fields(location_keys,
                                                   entanglements)
    coll_fields = board.verify_suspected_fields(suspected_fields)
    chosen_mark = 'X1'
    assert board.board() == [
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['X1', '  ', '  ', 'O4', '  ', '  ', '  ', '  ', '  '],
        ['  ', 'O2', 'X3', 'O4', '  ', '  ', '  ', '  ', '  '],
        ['X1', 'O2', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', 'X3', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    ]

    current_board = deepcopy(board.board())
    smart_computer = SmartComputer(board.board(), board.collapse_dict(),
                                   board.spooky_marks_dict())
    assert smart_computer.collapse(coll_fields, chosen_mark,
                                   current_board) == [
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['O4'],
        ['O2'],
        ['X1'],
        ['X3'],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    ]


def test_winning_process_no_winner():
    board = Board()
    smart_computer = SmartComputer(board.board(), board.collapse_dict(),
                                   board.spooky_marks_dict())
    collapsed_board = [['O6'], ['O8'], ['X3'], ['O2'], ['X1'], ['O4'],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']]
    assert not smart_computer.winning_process(collapsed_board)


def test_winning_process_winner():
    board = Board()
    smart_computer = SmartComputer(board.board(), board.collapse_dict(),
                                   board.spooky_marks_dict())
    collapsed_board = [['O6'], ['O8'], ['O4'], ['O2'],
                       ['X1'], ['X3'], ['X5'], ['X7'],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']]
    assert smart_computer.winning_process(collapsed_board) == ('O', 1, 0)


def test_check_winner_O():
    result1 = ('O', 1, 0)
    result2 = None
    first_mark = 'O4'
    second_mark = 'X3'
    board = Board()
    smart_computer = SmartComputer(board.board(), board.collapse_dict(),
                                   board.spooky_marks_dict())
    assert smart_computer.check_winner(result1, result2,
                                       first_mark, second_mark) == 'O4'


def test_check_winner_X():
    result1 = None
    result2 = ('O', 1, 0)
    first_mark = 'X3'
    second_mark = 'O4'
    board = Board()
    smart_computer = SmartComputer(board.board(), board.collapse_dict(),
                                   board.spooky_marks_dict())
    assert smart_computer.check_winner(result1, result2,
                                       first_mark, second_mark) == 'O4'


def test_check_winner_none_X():
    result1 = None
    result2 = ('X', 1, 0)
    first_mark = 'O4'
    second_mark = 'X3'
    board = Board()
    smart_computer = SmartComputer(board.board(), board.collapse_dict(),
                                   board.spooky_marks_dict())
    assert smart_computer.check_winner(result1, result2,
                                       first_mark, second_mark) == 'O4'


def test_check_winner_both_O():
    result1 = ('O', 1.5, 0)
    result2 = ('O', 1, 0)
    first_mark = 'O6'
    second_mark = 'O4'
    board = Board()
    smart_computer = SmartComputer(board.board(), board.collapse_dict(),
                                   board.spooky_marks_dict())
    assert smart_computer.check_winner(result1, result2,
                                       first_mark, second_mark) == 'O6'


def test_check_winner_both_X():
    result1 = ('X', 1.5, 0)
    result2 = ('X', 1, 0)
    first_mark = 'X1'
    second_mark = 'X7'
    board = Board()
    smart_computer = SmartComputer(board.board(), board.collapse_dict(),
                                   board.spooky_marks_dict())
    assert smart_computer.check_winner(result1, result2,
                                       first_mark, second_mark) == 'X7'


def test_check_winner_two_diffrent_O():
    result1 = ('O', 1.5, 0)
    result2 = ('X', 1, 0)
    first_mark = 'O2'
    second_mark = 'X7'
    board = Board()
    smart_computer = SmartComputer(board.board(), board.collapse_dict(),
                                   board.spooky_marks_dict())
    assert smart_computer.check_winner(result1, result2,
                                       first_mark, second_mark) == 'O2'
