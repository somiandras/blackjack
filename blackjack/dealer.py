from blackjack.deck import Deck
from blackjack.logger import Logger

class DealerException(Exception):
    pass


class Dealer:

    def __init__(self, player, **kwargs):
        self.player = player
        self.deck = Deck()
        self.logger = Logger()

    def deal_starting_hands(self):
        self.deck.reshuffle()
        self.player_cards = self.deck.deal(n_cards=2)
        self.house_cards = self.deck.deal(n_cards=1)
        
        return self

    @property
    def player_value(self):
        return self.evaluate_cards(self.player_cards)

    @property
    def house_value(self):
        return self.evaluate_cards(self.house_cards)

    def evaluate_cards(self, hand):
        aces = [card for card in hand if card[0] == 'A']
        non_aces = [card for card in hand if card[0] != 'A']

        value = 0
        for card in non_aces:
            try:
                card_value = int(card[0])
            except ValueError:
                card_value = 10

            value += card_value
        
        for _ in aces:
            if value <= 10:
                value += 11
            else:
                value += 1

        return value        

    @property
    def reward(self):
        if self.house_value <= 21 and self.player_value <= 21:
            if self.player_value < self.house_value:
                reward = -10
            elif self.player_value > self.house_value:
                reward = 10
            else:
                reward = 0
        elif self.player_value > 21:
            reward = -10
        elif self.house_value > 21:
            reward = 10

        return reward

    @property
    def player_action(self):
        training = self.player.training
        player_cards = self.player_cards
        house_cards = self.house_cards

        action = self.player.action(player_cards, house_cards)
        self.logger.log_action(training, player_cards, house_cards, action)

        return action

    def hit_hand(self, which_hand):
        new_card = self.deck.deal()
        if which_hand == 'player':
            self.player_cards.extend(new_card)
        elif which_hand == 'house':
            self.house_cards.extend(new_card)

    def run_game(self):
        self.deal_starting_hands()
       
        if self.player_value < 21:
            while self.player_action != 'stand':
                self.hit_hand('player')
                if self.player_value >= 21:
                    break

        if self.player_value <= 21:
            while self.house_value < 17:
                self.hit_hand('house')

        self.player.reward(self.reward)
        self.logger.log_results(
            self.player.training, self.player_cards, self.house_cards, self.reward)
