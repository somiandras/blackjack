from blackjack.deck import Deck


class DealerException(Exception):
    pass


class Dealer:

    def __init__(self, player):
        self.player = player
        self.deck = Deck()

    def deal_starting_hands(self):
        self.deck.reshuffle()

        self.player_cards = self.deck.deal(n_cards=2)
        self.player_value = self.evaluate_cards(self.player_cards)

        self.house_cards = self.deck.deal(n_cards=1)
        self.house_value = self.evaluate_cards(self.house_cards)
        
        return self

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
        
        for ace in aces:
            if value <= 10:
                value += 11
            else:
                value += 1

        return value        

    def run_game(self):
        self.deal_starting_hands()
        
        if self.player_value < 21:
            player_action = self.player.take_action(self.player_cards)
            while player_action != 'stand' and self.player_value < 21:
                self.player_cards.extend(self.deck.deal())
                self.player_value = self.evaluate_cards(self.player_cards)
                player_action = self.player.take_action(self.player_cards)

        if self.player_value <= 21:
            while self.house_value < 17:
                self.house_cards.extend(self.deck.deal())
                self.house_value = self.evaluate_cards(self.house_cards)


        if self.house_value <= 21 and self.player_value <= 21:
            if self.player_value < self.house_value:
                reward = -10
            elif self.player_value > self.house_value:
                reward = 10
            else:
                reward = 0
        elif self.house_value > 21:
            reward = 10
        elif self.player_value > 21:
            reward = -10

        print('Player: {}\nHouse: {}'.format(self.player_cards, self.house_cards))

        self.player.get_reward(reward)
        return reward
