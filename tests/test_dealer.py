import unittest
from blackjack.dealer import Dealer, DealerException
from blackjack.player import Player
from unittest.mock import Mock, MagicMock

class TestDealer(unittest.TestCase):

    def setUp(self):
        mock_player = MagicMock(spec=Player)
        self.dealer = Dealer(mock_player)

    def test_deal_starting_hands(self):
        self.dealer.deal_starting_hands()

        self.assertEqual(len(self.dealer.player_cards), 2)
        self.assertEqual(len(self.dealer.house_cards), 1)
        self.assertGreater(self.dealer.player_value, 0)
        self.assertGreater(self.dealer.house_value, 0)

    def test_evaluate_cards(self):
        hands = [
            ['3d', 'Tc'],
            ['Ad', 'Tc'],
            ['Ad', '2c'],
            ['Ad', 'Ac'],
            ['Ks', 'Qs'],
            ['Ks', 'Qs', 'Ad']
        ]

        values = [13, 21, 13, 12, 20, 21]

        for hand, value in zip(hands, values):
            with self.subTest(hand=hand, value=value):
                calculated_value = self.dealer.evaluate_cards(hand)
                self.assertEqual(calculated_value, value)
