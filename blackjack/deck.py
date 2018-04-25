import random

CARD_FACES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['c', 'd', 'h', 's']

class DeckException(Exception):
    pass


class Deck:
    '''Class defining a deck of playing cards.'''

    def __init__(self):
        self.reshuffle()

    def _generate(self):
        '''Generate new deck of cards and return list of cards.'''

        new_deck = []
        for suit in SUITS:
            for face in CARD_FACES:
                new_deck.append('{}{}'.format(face, suit))

        return new_deck

    def shuffle(self):
        '''Shuffle remaining cards inplace.'''

        random.shuffle(self.cards)
        return self

    def reshuffle(self):
        '''Get new deck and shuffle it inplace.'''
        
        self.cards = self._generate()
        self.shuffle()
        self.dealt = []
        return self

    def deal(self, n_cards=1):
        '''Get last n cards and return them in a list.'''

        assert n_cards > 0, 'n_cards has to be greater than 0'

        if n_cards > len(self.cards):
            raise DeckException('Deck is shorter ({}) than needed ({})'
                                .format(len(self.cards), n_cards))
        dealt_cards = self.cards[-n_cards:]
        dealt_cards.reverse()
        self.cards = self.cards[:-n_cards]
        self.dealt.extend(dealt_cards)

        return dealt_cards
