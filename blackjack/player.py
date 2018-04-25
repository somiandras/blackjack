import random

class PlayerException(Exception):
    pass


class Player:
    def __init__(self):
        pass

    def take_action(self):
        return random.choice(['stand', 'hit'])
