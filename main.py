from player import Player
from board import Board
from random_computer import RandomComputer
from smart_computer import SmartComputer


ENEMIES = ['another player', 'random computer', 'smart computer']

ENEMIES_DICT = {'another player': 'P',
                'random computer': 'RC',
                'smart computer': 'SC'}


def create_player(mark):
    """Creates player"""
    name = input(f'Please enter the name of the player {mark}: ')
    return Player(name)


def create_random_computer():
    """Creates random computer"""
    return RandomComputer()


def create_smart_computer(board):
    """Creates smart computer"""
    return SmartComputer(board.board(), board.collapse_dict(),
                         board.spooky_marks_dict())


def choose_enemy(ENEMIES_DICT, board):
    """Allows user to choose his enemy"""
    message = 'Please choose your opponent by entering the given letters:\n'
    opening = 'To play against'
    num = 1
    for enemy in ENEMIES:
        message += f'{num}. {opening} {enemy} choose: {ENEMIES_DICT[enemy]}\n'
        num += 1
    choosen_enemy = input(message).upper()
    if choosen_enemy in ENEMIES_DICT.values():
        if choosen_enemy == 'P':
            enemy = create_player('O')
        elif choosen_enemy == 'RC':
            enemy = create_random_computer()
        else:
            enemy = create_smart_computer(board)
        return enemy
    else:
        return choose_enemy(ENEMIES_DICT, board)


def main():
    board = Board()
    player = create_player('X')
    enemy = choose_enemy(ENEMIES_DICT, board)
    board.game(player, enemy)


if __name__ == '__main__':
    main()
