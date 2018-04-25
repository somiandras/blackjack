from blackjack.cards import Deck


class DealerException(Exception):
    pass


class Dealer:

    def __init__(self, player):
        self.player = player
        self.deck = Deck()
        self.reset()

    def reset(self):
        self.deck.reshuffle()
        self.player_cards = []
        self.house_cards = []
        self.player_value = 0
        self.house_value = 0

    def deal(self):
        self.player_cards = self.deck.deal(n_cards=2)
        self.house_cards = self.deck.deal(n_cards=1)

    def evaluate_hand(self, hand):
        aces = [card for card in hand if card.face == 'A']
        non_aces = [card for card in hand if card.face != 'A']

        value = 0
        for card in non_aces:
            try:
                card_value = int(card.face)
            except ValueError:
                card_value = 10

            value += card_value
        
        for ace in aces:
            if value <= 10:
                value += 11
            else:
                value += 1

        return value
