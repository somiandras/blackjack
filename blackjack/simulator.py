from blackjack.dealer import Dealer
from blackjack.player import Player


class SimulatorException(Exception):
    pass


class Simulator:

    def __init__(self, player, test_games=100):
        self.player = player
        self.test_games = test_games
        self.dealer = Dealer(self.player)
        
    def run(self):
        rounds = 0
        while self.player.training:
            self.dealer.run_game()
            rounds += 1

        for _ in range(self.test_games):
            self.dealer.run_game()
            rounds += 1
