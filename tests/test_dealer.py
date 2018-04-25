import unittest
from blackjack.dealer import Dealer, DealerException
from blackjack.player import Player
from blackjack.cards import Card
from unittest.mock import MagicMock

class TestDealer(unittest.TestCase):

    def setUp(self):
        mock_player = MagicMock(spec=Player)
        self.dealer = Dealer(mock_player)

    def test_deal(self):
        self.dealer.deal()

        self.assertEqual(len(self.dealer.player_cards), 2)
        self.assertEqual(len(self.dealer.house_cards), 1)

    def test_reset(self):
        self.dealer.reset()

        self.assertEqual(len(self.dealer.player_cards), 0)
        self.assertEqual(self.dealer.player_value, 0)
        self.assertEqual(self.dealer.house_value, 0)

    def test_evaluate_hand(self):
        hands = [
            [Card('diamond', '3'), Card('club', '10')],
            [Card('diamond', 'A'), Card('club', '10')],
            [Card('diamond', 'A'), Card('club', '2')],
            [Card('diamond', 'A'), Card('club', 'A')],
            [Card('spade', 'K'), Card('spade', 'Q')],
            [Card('spade', 'K'), Card('spade', 'Q'), Card('club', 'A')]
        ]

        values = [13, 21, 13, 12, 20, 21]

        for hand, value in zip(hands, values):
            with self.subTest(hand=hand, value=value):
                calculated_value = self.dealer.evaluate_hand(hand)
                self.assertEqual(calculated_value, value)
