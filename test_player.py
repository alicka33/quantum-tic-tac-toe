from player import Player


def test_create_player():
    player = Player('Ala')
    assert player.name() == 'Ala'


def test_set_name():
    player = Player('Ala')
    player.set_name('Kuba')
    assert player.name() == 'Kuba'


def test_fields_list_to_str():
    fields_list = [1, 2, 3]
    assert Player.fields_list_to_str(fields_list) == ['1', '2', '3']


def test_valid_locations():
    player = Player()
    fields_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    assert player.valid_locations('12', fields_list)


def test_valid_locations_error():
    player = Player()
    fields_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    assert not player.valid_locations('12ivboaiev', fields_list)


def test_valid_locations_repeated():
    player = Player()
    fields_list = ['2']
    assert player.valid_locations('22', fields_list)
