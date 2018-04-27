from blackjack import Simulator
from blackjack import Player


if __name__ == '__main__':
    player = Player()
    simulator = Simulator(player, test_games=10)
    simulator.run()
