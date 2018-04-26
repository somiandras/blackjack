import random

class PlayerException(Exception):
    pass


class Player:
    def __init__(self):
        pass

    def take_action(self, *args, **kwargs):
        return random.choice(['stand', 'hit'])
