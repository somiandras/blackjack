import unittest
from unittest.mock import MagicMock
from blackjack.simulator import Simulator, SimulatorException, Player
from blackjack.dealer import Dealer


class TestSimulator(unittest.TestCase):

    def setUp(self):
        self.simulator = Simulator()
        self.simulator.dealer = MagicMock(spec=Dealer)
    
    def test_run(self):
        self.simulator.train_rounds = 20
        self.simulator.test_rounds = 10

        self.simulator.run()

        call_count = self.simulator.dealer.run_game.call_count
        self.assertEqual(call_count, 30)
