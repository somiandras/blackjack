from blackjack import Simulator
from blackjack import Player


if __name__ == '__main__':
    for step in range(10):
        alpha = step / 10
        player = Player(epsilon=0, no_decay=True, training_rounds=100000, alpha=alpha)
        simulator = Simulator(player, test_games=10000)
        simulator.run()
        simulator.report(rolling=1000, suffix='alpha_{:.1f}'.format(alpha))
