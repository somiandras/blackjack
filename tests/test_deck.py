import unittest
from blackjack.deck import Deck, DeckException


class DeckTest(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_deck_reshuffle(self):
        self.assertIsNotNone(self.deck.cards)
        self.assertListEqual(self.deck.dealt, [])

    def test_generate_deck(self):
        new_deck = self.deck._generate()
        
        self.assertIsInstance(new_deck, list)
        self.assertEqual(len(set(new_deck)), 52)
        self.assertEqual(len(new_deck[0]), 2)

    def test_shuffle(self):
        old_deck = list(self.deck.cards)
        self.deck.shuffle()
        new_deck = list(self.deck.cards)

        self.assertEqual(len(old_deck), len(new_deck))
        self.assertNotEqual(old_deck, new_deck)
        self.assertEqual(sum([1 for card in self.deck.cards if card in old_deck]), len(old_deck))

    def test_deal(self):
        for n in [0, 1, 2, 52]:
            with self.subTest(n=n):
                old_deck = list(self.deck.cards)
                
                if n <=0:
                    with self.assertRaises(AssertionError):
                        self.deck.deal(n_cards=n)
                elif n > len(old_deck):
                    with self.assertRaises(DeckException):
                        self.deck.deal(n_cards=n)
                else:
                    dealt = self.deck.deal(n_cards=n)
                    dealt.reverse()

                    self.assertEqual(len(self.deck.cards), len(old_deck) - n)
                    self.assertEqual(len(dealt), n)
                    self.assertListEqual(old_deck[-n:], dealt)
                    self.assertNotIn(dealt[0], self.deck.cards)


if __name__ == '__main__':
    unittest.main()
