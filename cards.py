CARD_FACES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'K', 'Q', 'A']
SUIT_CHAR_CODES = {
    'heart': u'\u2665',
    'club': u'\u2663',
    'spade': u'\u2660',
    'diamond': u'\u2666'
}


class CardException(Exception):
    pass


class DeckException(Exception):
    pass


class Card:
    '''Class defining individual playing cards in a deck.'''

    def __init__(self, suit, rank=None, face=None):
        assert suit in ['heart', 'club', 'spade', 'diamond'], 'Unkown suit'
        self.suit = suit

        if rank:
            assert rank in range(13), 'Invalid card rank'
            self.rank = rank
            self.face = CARD_FACES[rank]
        elif face:
            assert face in CARD_FACES, 'Invalid card face'
            self.face = face
            self.rank = CARD_FACES.index(face)
        else:
            raise CardException('Either card face or rank has to be defined')

    @property
    def symbol(self):
        return '{}{}'.format(SUIT_CHAR_CODES[self.suit], self.face)


class Deck:
    '''Class defining a deck of playing cards.'''

    def __init__(self):
        pass

    def _generate(self):
        '''Generate new deck of cards'''
        pass

    def shuffle(self):
        '''Shuffle remaining cards'''
        pass

    def reshuffle(self):
        '''Add back all the dealt cards and shuffle'''
        pass

    def deal(self, n_cards=1):
        '''Deal top n cards'''
        pass
