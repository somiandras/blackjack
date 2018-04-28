from blackjack.dealer import Dealer
from blackjack.player import Player
from blackjack.logger import Logger


class SimulatorException(Exception):
    pass


class Simulator:

    def __init__(self, player, test_games=100):
        self.player = player
        self.test_games = test_games
        self.dealer = Dealer(self.player)
        self.logger = Logger()
        
    def run(self):
        rounds = 0
        while self.player.training:
            self.dealer.run_game()
            rounds += 1

        for _ in range(self.test_games):
            self.dealer.run_game()
            rounds += 1

        self.logger.log_Q(self.player.Q)
    
    def report(self, *args, **kwargs):
        self.logger.report(*args, **kwargs)
