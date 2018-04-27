from blackjack import Simulator
from blackjack import Player


if __name__ == '__main__':
    player = Player(alpha=0.7, gamma=0.7, epsilon=0.999, tolerance=0.001)
    simulator = Simulator(player, test_games=100)
    simulator.run()
