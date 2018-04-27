from blackjack.dealer import Dealer
from blackjack.player import Player


class SimulatorException(Exception):
    pass


class Simulator:

    def __init__(self, train_rounds=None, test_rounds=None, **kwargs):
        self.train_rounds = train_rounds
        self.test_rounds = test_rounds
        player_kwargs = kwargs
        dealer_kwargs = kwargs
        self.dealer = Dealer(Player(**player_kwargs), **dealer_kwargs)
        
    def run(self, **kwargs):
        for train_round in range(self.train_rounds):
            self.dealer.run_game(round=train_round, test=False)

        for test_round in range(self.test_rounds):
            self.dealer.run_game(round=test_round + self.train_rounds, test=True)
