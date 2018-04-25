import random

CARD_FACES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUIT_CHAR_CODES = [
    ('club', u'\u2667'),
    ('diamond', u'\u2662'),
    ('heart', u'\u2661'),
    ('spade', u'\u2664'),
]


class CardException(Exception):
    pass


class DeckException(Exception):
    pass


class Card:
    '''Class defining individual playing cards in a deck.'''

    def __init__(self, suit, face):
        assert suit in [name for name, char in SUIT_CHAR_CODES], \
            'Unkown suit: {}'.format(suit)
        self.suit = suit

        assert face in CARD_FACES or str(face) in CARD_FACES, \
             'Invalid card face: {}'.format(face)
        self.face = str(face)

    def __repr__(self):
        return self.symbol

    def __hash__(self):
        return hash(self.symbol)

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __lt__(self, other):
        suits = [name for name, char in SUIT_CHAR_CODES]
        self_suit_rank = suits.index(self.suit)
        other_suit_rank = suits.index(other.suit)
        self_face_rank = CARD_FACES.index(self.face)
        other_face_rank = CARD_FACES.index(other.face)
        
        if self_suit_rank != other_suit_rank:
            return self_suit_rank < other_suit_rank
        else:
            return self_face_rank < other_face_rank

    @property
    def symbol(self):
        char = [char for name, char in SUIT_CHAR_CODES if name == self.suit][0]
        return '{}{}'.format(char, self.face)


class Deck:
    '''Class defining a deck of playing cards.'''

    def __init__(self):
        self.reshuffle()

    def _generate(self):
        '''Generate new deck of cards and return list of cards.'''

        new_deck = []
        for suit in [name for name, char in SUIT_CHAR_CODES]:
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
