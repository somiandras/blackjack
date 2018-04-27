from blackjack.dealer import Dealer
from blackjack.player import Player


class SimulatorException(Exception):
    pass


class Simulator:

    def __init__(self, player, test_rounds=100):
        self.player = player
        self.test_rounds = test_rounds
        self.dealer = Dealer(self.player)
        
    def run(self):
        train_rounds = 0
        training = True
        while training:
            training = self.dealer.run_one_round(test=False)
            train_rounds += 1
            print('Training rounds: {}, balance: {}'.format(train_rounds, self.dealer.balance))

        test_rounds = 0
        while test_rounds < self.test_rounds:
            self.dealer.run_one_round(test=True)
            test_rounds += 1
            print('Test rounds: {}'.format(test_rounds))

        print('Finished, balance: {}'.format(self.dealer.balance))
