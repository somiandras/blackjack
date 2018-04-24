import random

CARD_FACES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUIT_CHAR_CODES = {
    'heart': u'\u2661',
    'club': u'\u2667',
    'spade': u'\u2664',
    'diamond': u'\u2662'
}


class CardException(Exception):
    pass


class DeckException(Exception):
    pass


class Card:
    '''Class defining individual playing cards in a deck.'''

    def __init__(self, suit, face):
        assert suit in SUIT_CHAR_CODES.keys(), \
            'Unkown suit: {}'.format(suit)
        self.suit = suit

        assert face in CARD_FACES or str(face) in CARD_FACES, \
             'Invalid card face: {}'.format(face)
        self.face = face

    def __repr__(self):
        return self.symbol

    @property
    def symbol(self):
        return '{}{}'.format(SUIT_CHAR_CODES[self.suit], self.face)


class Deck:
    '''Class defining a deck of playing cards.'''

    def __init__(self):
        self.reshuffle()

    def _generate(self):
        '''Generate new deck of cards and return list of cards.'''

        new_deck = []
        for suit in SUIT_CHAR_CODES.keys():
            for face in CARD_FACES:
                new_deck.append(Card(suit, face=face))

        return new_deck

    def shuffle(self):
        '''Shuffle remaining cards inplace.'''

        random.shuffle(self.cards)

    def reshuffle(self):
        '''Get new deck and shuffle it inplace.'''
        
        self.cards = self._generate()
        self.shuffle()
        self.dealt = []

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
