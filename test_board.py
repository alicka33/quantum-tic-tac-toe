from board import Board


EMPTY_BOARD = [
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    ]


def test_create_empty_board():
    board = Board()
    assert board.board() == EMPTY_BOARD


def test_create_collapse_dict():
    board = Board()
    assert board.collapse_dict() == {}


def test_create_spooky_marks_dict():
    board = Board()
    assert board.spooky_marks_dict() == {}


def test_create_fields_dict():
    board = Board()
    assert board.fields_dict() == {}


def test_set_small_board():
    board = Board()
    board.set_small_board(1, 5, 'X5')
    assert board.board()[0][4] == 'X5'


def test_set_small_board_2():
    board = Board()
    board.set_small_board(9, 4, 'O4')
    assert board.board()[8][3] == 'O4'


def test_set_fields_dict():
    board = Board()
    board.set_fields_dict(4, 'X5')
    assert board.fields_dict()[4] == ['X5']


def test_set_fields_dict_already_exist():
    board = Board()
    board.set_fields_dict(4, 'X5')
    board.set_fields_dict(4, 'O6')
    assert board.fields_dict()[4] == ['X5', 'O6']


def test_placing_spooky_marks():
    board = Board()
    board.placing_spooky_marks(1, 'X1', [1, 2])
    board.placing_spooky_marks(2, 'O2', [9, 2])
    assert board.board() == [
        ['X1', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['X1', 'O2', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', 'O2', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    ]


def test_extend_collapse_dict():
    board = Board()
    board.extend_collapse_dict(4, 7)
    assert board.collapse_dict() == {4: [7]}


def test_extend_collapse_dict_2():
    board = Board()
    board.extend_collapse_dict(4, 7)
    board.extend_collapse_dict(4, 8)
    board.extend_collapse_dict(5, 7)
    assert board.collapse_dict() == {4: [7, 8], 5: [7]}


def test_set_collapse_dict():
    board = Board()
    board.set_collapse_dict([4, 7])
    assert board.collapse_dict() == {4: [7], 7: [4]}


def test_keys_where_quantity_min2():
    board = Board()
    board.set_collapse_dict([5, 3])
    board.set_collapse_dict([4, 5])
    assert board.keys_where_quantity_min_2() == [5]


def test_get_all_spooky_marks_in_given_fields():
    board = Board()
    board.set_fields_dict(5, 'X1')
    board.set_fields_dict(4, 'X1')
    board.set_fields_dict(9, 'X3')
    board.set_fields_dict(4, 'O4')
    board.set_fields_dict(4, 'X5')
    board.set_fields_dict(5, 'O4')
    assert board.get_all_spooky_marks_in_given_fields([4, 5]) == \
        ['X1', 'O4', 'X5', 'X1', 'O4']


def test_if_enought_marks_repeat_true():
    board = Board()
    board.set_fields_dict(5, 'X1')
    board.set_fields_dict(4, 'X1')
    board.set_fields_dict(9, 'X3')
    board.set_fields_dict(4, 'O4')
    board.set_fields_dict(4, 'X5')
    board.set_fields_dict(5, 'O4')
    collpasing_fields = [4, 5]
    all_spooky_marks = \
        board.get_all_spooky_marks_in_given_fields(collpasing_fields)
    assert board.if_enough_marks_repeat(all_spooky_marks, collpasing_fields)


def test_if_enought_marks_repeat_false():
    board = Board()
    board.set_fields_dict(5, 'X1')
    board.set_fields_dict(4, 'O2')
    board.set_fields_dict(9, 'X1')
    board.set_fields_dict(4, 'O4')
    board.set_fields_dict(4, 'X5')
    board.set_fields_dict(5, 'O4')
    coll_fields = [4, 5]
    all_spooky_marks = \
        board.get_all_spooky_marks_in_given_fields(coll_fields)
    assert not board.if_enough_marks_repeat(all_spooky_marks, coll_fields)


def test_find_suspected_fields_empty():
    board = Board()
    board.set_collapse_dict([5, 3])
    board.set_collapse_dict([4, 5])
    location_keys = board.keys_where_quantity_min_2()
    entanglements = board.all_entanglements_for_location_keys(location_keys)
    assert board.find_suspected_fields(location_keys, entanglements) == []


def test_find_suspected_fields():
    board = Board()
    board.set_collapse_dict([5, 3])
    board.set_collapse_dict([4, 5])
    board.set_collapse_dict([4, 3])
    location_keys = board.keys_where_quantity_min_2()
    entanglements = board.all_entanglements_for_location_keys(location_keys)
    assert board.find_suspected_fields(location_keys, entanglements) == \
        [5, 3, 4]


def test_find_suspected_fields_2():
    board = Board()
    board.set_collapse_dict([5, 4])
    board.set_collapse_dict([4, 5])
    location_keys = board.keys_where_quantity_min_2()
    entanglements = board.all_entanglements_for_location_keys(location_keys)
    assert board.find_suspected_fields(location_keys, entanglements) == [5, 4]


def test_verify_suspected_fields():
    board = Board()
    board.set_collapse_dict([5, 3])
    board.set_collapse_dict([4, 5])
    board.set_collapse_dict([4, 3])
    location_keys = board.keys_where_quantity_min_2()
    entanglements = board.all_entanglements_for_location_keys(location_keys)
    suspected_fields = board.find_suspected_fields(location_keys,
                                                   entanglements)
    assert board.verify_suspected_fields(suspected_fields) == [5, 3, 4]


def test_verify_suspected_fields_2():
    board = Board()
    board.set_collapse_dict([5, 3])
    board.set_collapse_dict([4, 5])
    board.set_collapse_dict([4, 6])
    board.set_collapse_dict([4, 3])
    location_keys = board.keys_where_quantity_min_2()
    entanglements = board.all_entanglements_for_location_keys(location_keys)
    suspected_fields = board.find_suspected_fields(location_keys,
                                                   entanglements)
    assert board.verify_suspected_fields(suspected_fields) == [5, 3, 4]


def test_collapsing_requirements_met():
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
    location_keys = board.keys_where_quantity_min_2()
    entanglements = board.all_entanglements_for_location_keys(location_keys)
    suspected_fields = board.find_suspected_fields(location_keys,
                                                   entanglements)
    coll_fields = board.verify_suspected_fields(suspected_fields)
    all_spooky_marks = \
        board.get_all_spooky_marks_in_given_fields(coll_fields)
    if_enough_repeat = board.if_enough_marks_repeat(all_spooky_marks,
                                                    coll_fields)
    assert board.collapsing_requirements_met(coll_fields, if_enough_repeat)


def test_find_collpased_fields():
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
    locations = board.keys_where_quantity_min_2()
    entanglements = board.all_entanglements_for_location_keys(locations)
    assert board.find_collapsed_fields(locations, entanglements) == [5, 3, 4]


def test_set_spooky_marks_dictionary():
    board = Board()
    board.set_spooky_marks_dictionary('X3', [5, 9])
    board.set_spooky_marks_dictionary('O4', [5, 3])
    assert board.spooky_marks_dict() == {'X3': [5, 9], 'O4': [5, 3]}


def test_spooky_marks_in_collapse():
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
    location_keys = board.keys_where_quantity_min_2()
    entanglements = board.all_entanglements_for_location_keys(location_keys)
    suspected_fields = board.find_suspected_fields(location_keys,
                                                   entanglements)
    coll_fields = board.verify_suspected_fields(suspected_fields)
    marks = board.spooky_marks_in_collapse(coll_fields)
    if_in = 'X1' in marks and 'O2' in marks and 'O4' in marks
    assert len(marks) == 3 and if_in


def test_collapse_spooky_marks_field_dict():
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
    location_keys = board.keys_where_quantity_min_2()
    entanglements = board.all_entanglements_for_location_keys(location_keys)
    suspected_fields = board.find_suspected_fields(location_keys,
                                                   entanglements)
    coll_fields = board.verify_suspected_fields(suspected_fields)
    marks = board.spooky_marks_in_collapse(coll_fields)
    dict = board.collapse_spooky_marks_field_dict(coll_fields, marks)
    assert 'O2' in dict[5] and 'X1' in dict[5] and len(dict[5]) == 2
    assert 'O4' in dict[3] and 'X1' in dict[3] and len(dict[3]) == 2
    assert 'O2' in dict[4] and 'O4' in dict[4] and len(dict[4]) == 2


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
    board.collapse(coll_fields, chosen_mark)
    assert board.board() == [
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


def test_is_field_collapsed():
    board = Board()
    board.board()[5] = ['X5']
    assert board.is_field_collapsed(board.board()[5])


def test_is_field_collapsed_false():
    board = Board()
    board.board()[5] = ['X5', 'X3', 'O4', '  ', '  ', '  ', '  ', '  ', '  ']
    assert not board.is_field_collapsed(board.board()[5])


def test_convert_big_board():
    board = Board()
    board.board()[0] = []
    board.board()[1] = ['X3', 'O4', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[2] = ['X5']
    board.board()[3] = ['X1', 'X3', 'O6', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[4] = ['O2']
    board.board()[5] = ['X6', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[6] = ['O4', 'X1', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[7] = []
    board.board()[8] = []
    assert board.convert_big_board(board.board()) == \
        [' 0', ' 0', 'X5', ' 0', 'O2', ' 0', ' 0', ' 0', ' 0']


def test_diagonals():
    board = Board()
    board.board()[0] = []
    board.board()[1] = ['X3', 'O4', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[2] = ['X5']
    board.board()[3] = ['X1', 'X3', 'O6', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[4] = ['O2']
    board.board()[5] = ['X6', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[6] = ['O4', 'X1', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[7] = []
    board.board()[8] = []
    big_board = board.convert_big_board(board.board())
    assert board.diagonals(big_board) == \
        [[' 0', 'O2', ' 0'], ['X5', 'O2', ' 0']]


def test_rows():
    board = Board()
    board.board()[0] = []
    board.board()[1] = ['X3', 'O4', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[2] = ['X5']
    board.board()[3] = ['X1', 'X3', 'O6', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[4] = ['O2']
    board.board()[5] = ['X6', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[6] = ['O4', 'X1', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[7] = []
    board.board()[8] = []
    big_board = board.convert_big_board(board.board())
    assert board.rows(big_board) == \
        [[' 0', ' 0', 'X5'], [' 0', 'O2', ' 0'], [' 0', ' 0', ' 0']]


def test_columns():
    board = Board()
    board.board()[0] = []
    board.board()[1] = ['X3', 'O4', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[2] = ['X5']
    board.board()[3] = ['X1', 'X3', 'O6', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[4] = ['O2']
    board.board()[5] = ['X6', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[6] = ['O4', 'X1', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
    board.board()[7] = []
    board.board()[8] = []
    big_board = board.convert_big_board(board.board())
    assert board.columns(big_board) == \
        [[' 0', ' 0', ' 0'], [' 0', 'O2', ' 0'], ['X5', ' 0', ' 0']]


def test_create_all_possibilities():
    board = Board()
    diagonals = [[' 0', 'O2', ' 0'], ['X5', 'O2', ' 0']]
    rows = [[' 0', ' 0', 'X5'], [' 0', 'O2', ' 0'], [' 0', ' 0', ' 0']]
    columns = [[' 0', ' 0', ' 0'], [' 0', 'O2', ' 0'], ['X5', ' 0', ' 0']]
    assert board.create_all_possibilietes(diagonals, rows, columns) == \
        [[' 0', 'O2', ' 0'], ['X5', 'O2', ' 0'],
         [' 0', ' 0', 'X5'], [' 0', 'O2', ' 0'], [' 0', ' 0', ' 0'],
         [' 0', ' 0', ' 0'], [' 0', 'O2', ' 0'], ['X5', ' 0', ' 0']]


def test_check_winners():
    board = Board()
    all_possibilities = [
        ['O6', 'O2', 'O4'], ['X5', 'O2', ' 0'],
        [' 0', ' 0', 'X5'], [' 0', 'O2', ' 0'], [' 0', ' 0', ' 0'],
        [' 0', ' 0', ' 0'], [' 0', 'O2', ' 0'], ['X5', 'X3', 'X1']]
    assert board.check_winners(all_possibilities) == [('O', 6), ('X', 5)]


def test_check_winners_no_winner():
    board = Board()
    all_possibilities = [
        [' 0', 'O2', ' 0'], ['X5', 'O2', ' 0'],
        [' 0', ' 0', 'X5'], [' 0', 'O2', ' 0'], [' 0', ' 0', ' 0'],
        [' 0', ' 0', ' 0'], [' 0', 'O2', ' 0'], ['X5', ' 0', ' 0']]
    assert board.check_winners(all_possibilities) == []


def test_choose_winner():
    board = Board()
    winners = [('O', 6), ('X', 5)]
    assert board.choose_winner(winners) == ('X', 1, 0.5)


def test_choose_winner_one_winner():
    board = Board()
    winners = [('O', 6)]
    assert board.choose_winner(winners) == ('O', 1, 0)


def test_choose_winner_3():
    board = Board()
    winners = [('X', 7), ('X', 5)]
    assert board.choose_winner(winners) == ('X', 1.5, 0)


def test_choose_winner_4():
    board = Board()
    winners = [('X', 9), ('X', 9)]
    assert board.choose_winner(winners) == ('X', 2, 0)
