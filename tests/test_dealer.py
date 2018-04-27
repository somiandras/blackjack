import unittest
from blackjack.dealer import Dealer, DealerException
from blackjack.player import Player
from unittest.mock import Mock, MagicMock

class TestDealer(unittest.TestCase):

    def setUp(self):
        self.dealer = Dealer(player=MagicMock())

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

    def test_run_game(self):
        # TODO: Set up test for player blackjack
        dealer = Dealer(player=MagicMock())
        dealer.deal_starting_hands = Mock()
        dealer.player.action = Mock(side_effect=['hit', 'stand'])
        dealer.deck.deal = Mock(side_effect=[['Ac'], ['6c']])    
        
        dealer.player_cards = ['3s', '4d']
        dealer.player_value = 7
        dealer.house_cards = ['Ad']
        dealer.house_value = 11

        dealer.run_game()

        dealer.deal_starting_hands.assert_called_once()

        self.assertEqual(len(dealer.player_cards), 3)
        self.assertEqual(dealer.player.action.call_count, 2)

        dealer.player.reward.assert_called_once()

    def test_evaluate_game(self):
        cases = [
            (23, 10, -10),
            (21, 11, 10),
            (20, 17, 10),
            (18, 18, 0),
            (17, 20, -10),
            (16, 22, 10),
            (23, 23, -10)
        ]

        for player_v, house_v, exp_rew in cases:
            with self.subTest(player=player_v, house=house_v, exp_rew=exp_rew):
                self.dealer.player_value = player_v
                self.dealer.house_value = house_v
                reward = self.dealer.reward
                self.assertEqual(reward, exp_rew)
