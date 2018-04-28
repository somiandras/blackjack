from blackjack import Simulator
from blackjack import Player


if __name__ == '__main__':
    player = Player(epsilon=0.1, no_decay=True, training_rounds=500000, alpha=0.5)
    simulator = Simulator(player, test_games=100000)
    simulator.run()
    simulator.report(rolling=10000)
