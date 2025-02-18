from random_computer import RandomComputer


def test_location_to_move(monkeypatch):
    def always_choose_2(some_list):
        return [2, 4]
    tested_method = 'random_computer.RandomComputer.location_to_move'
    monkeypatch.setattr(tested_method, always_choose_2)
    random_computer = RandomComputer()
    assert random_computer.location_to_move() == [2, 4]


def test_choose_collapse(monkeypatch):
    def always_choose_X7(some_list):
        return 'X7'
    tested_method = 'random_computer.RandomComputer.choose_collapse'
    monkeypatch.setattr(tested_method, always_choose_X7)
    random_computer = RandomComputer()
    assert random_computer.choose_collapse() == 'X7'
