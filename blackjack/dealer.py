from blackjack.deck import Deck
from blackjack.logger import Logger


class Dealer:
    '''
    Class representing the dealer. The dealer manages a single round of
    the game from initial dealing through dealing additional cards to 
    monitoring hand values and logging the results.

    Args:  
    `player`: blackjack.Player instance to interact with.
    '''

    def __init__(self, player, **kwargs):
        self.player = player
        self.deck = Deck()
        self.logger = Logger()
        self.options = ['stand', 'hit']

    def deal_starting_hands(self):
        '''
        Reshuffle deck and deal 2 cards for player and one card for house.

        Returns: self
        '''
        self.deck.reshuffle()
        self.player_cards = self.deck.deal(n_cards=2)
        self.house_cards = self.deck.deal(n_cards=1)
        
        return self

    @property
    def player_value(self):
        '''
        Returns the current value of player cards.

        Returns: (int): the current value
        '''
        return self.evaluate_cards(self.player_cards)

    @property
    def house_value(self):
        '''
        Returns the current value of house cards.

        Returns: (int): the current value
        '''
        return self.evaluate_cards(self.house_cards)

    def evaluate_cards(self, hand):
        '''
        Calculates the value of a hand (list of cards) according to
        blackjack rules (2-T: face value, J-K: 10, A: either 1 or 11).

        Args:  
        `hand`: list(str): list of card strings (first character: card
        face, second character: suit, eg. 'As', '4c', 'Td')

        Returns: (int): the current value of the hand.
        '''
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
        '''
        Returns the current reward (winning) based on the card values (
        even mid-round). The winning is calculated with the initial bet 
        (10) inclued, therefore the result is in [-10, 0, 10].

        Returns: (int):    
        0 if player value == house value, and both are valid hands
        -10 if player lost
        10 if player won
        '''
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
    def game_state(self):
        '''
        Creates ((P1, P2, ...), H) tuple, where P1, P2, ... are the
        player's cards ranks, while H is the rank of the open card
        of the house. The tuple represents the current state of the game,
        which is needed by the learning agent.

        Note: the suit of the cards is stripped as it is not necessary
        for computing the hand values and bloats state space for the
        learner.

        Returns: (tuple): state of the game, eg. (('A', '4'), 'K')
        '''

        player_cards = [card[0] for card in sorted(self.player_cards)]
        house_card = [card[0] for card in self.house_cards][0]

        state = (tuple(player_cards), house_card)

        return state

    @property
    def player_action(self):
        '''
        Returns the player's chosen action, after calling player.action()
        with current state and the given options for player actions. Logs
        the given action (phase, player hand, house hand, action).

        Returns: (str): players chose action, eg. 'hit' or 'stand'
        '''
        action, style = self.player.action(self.game_state, self.options)
        
        training = self.player.training
        player_cards = self.player_cards
        house_cards = self.house_cards

        self.logger.log_action(
            training, player_cards, house_cards, action, style)

        return action

    def hit_hand(self, which_hand):
        '''
        Deals one additional card for the hand defined by `which_hand`.

        Params:  
        `which_hand`: (str): 'player' or 'house'

        Returns: None
        '''
        assert which_hand in ['player', 'house']
        new_card = self.deck.deal()
        if which_hand == 'player':
            self.player_cards.extend(new_card)
        else:
            self.house_cards.extend(new_card)

    def run_game(self):
        '''
        Runs one round of blackjack game with player:

        1. Deal starting hands
        2. Deal cards to player until 'stand' or bust
        3. Deal cards for the house if needed (player stays in game)
        4. Evaluate game and give reward to player
        5. Log results

        Returns: None
        '''
        self.deal_starting_hands()
       
        if self.player_value < 21:
            while self.player_action != 'stand':
                self.hit_hand('player')
                if self.player_value >= 21:
                    break

        if self.player_value <= 21:
            while self.house_value < 17:
                self.hit_hand('house')

        self.player.set_reward(self.reward)
        self.logger.log_results(
            self.player.training, self.player_cards, self.house_cards, self.reward)
