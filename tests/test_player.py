import unittest
from blackjack.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    @unittest.mock.patch('blackjack.player.Player.Q')
    def test_action(self, mock_Q):
        player_cards = ['As', 'Qh']
        house_cards = ['Kd']
        action = self.player.action(player_cards, house_cards)
        self.assertIn(action, ['stand', 'hit'])
