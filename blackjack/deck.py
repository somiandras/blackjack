import random

CARD_RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
'''Possible card ranks for generating a deck'''

SUITS = ['c', 'd', 'h', 's']
'''Abreviations for the 4 card suits: clubs, diamonds, hearts and spades'''


class DeckException(Exception):
    '''Custom exception for `blackjack.Deck` class.'''
    pass


class Deck:
    '''
    Class defining a deck of playing cards with necessary methods to deal
    and (re)shuffle cards and track what cards had been dealt. Initializes 
    a shuffled state.
    '''

    def __init__(self):
        self.reshuffle()

    def _generate(self):
        '''
        Generate new deck of cards and return list of cards.

        Returns: list(str): list of cards in the form of 'As', '4c', etc.
        '''

        new_deck = []
        for suit in SUITS:
            for face in CARD_RANKS:
                new_deck.append('{}{}'.format(face, suit))

        return new_deck

    def shuffle(self):
        '''
        Shuffle remaining cards inplace in the deck.

        Returns: self
        '''

        random.shuffle(self.cards)
        return self

    def reshuffle(self):
        '''
        Get new deck and shuffle it inplace.

        Returns: self
        '''
        
        self.cards = self._generate()
        self.shuffle()
        self.dealt = []
        return self

    def deal(self, n_cards=1):
        '''
        Gets last n cards from current deck and returns them in a list.
        The `deck.dealt` list is extended with these cards.
        
        Returns: list(str): list of cards in the form of 'As', '4c', etc.
        '''

        assert n_cards > 0, 'n_cards has to be greater than 0'

        if n_cards > len(self.cards):
            raise DeckException('Deck is shorter ({}) than needed ({})'
                                .format(len(self.cards), n_cards))
        dealt_cards = self.cards[-n_cards:]
        dealt_cards.reverse()

        self.cards = self.cards[:-n_cards]
        self.dealt.extend(dealt_cards)

        return dealt_cards
