import unittest
from blackjack.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def test_take_action(self):
        action = self.player.take_action()
        self.assertIn(action, ['stand', 'hit'])
