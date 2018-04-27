from blackjack import Simulator

if __name__ == '__main__':
    simulator = Simulator(train_rounds=20, test_rounds=10)
    simulator.run()
