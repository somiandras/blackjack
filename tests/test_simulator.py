import unittest
from unittest.mock import MagicMock
from blackjack.simulator import Simulator, SimulatorException 
from blackjack.player import Player
from blackjack.dealer import Dealer


class TestSimulator(unittest.TestCase):

    def setUp(self):
        player = MagicMock(spec=Player)
        self.simulator = Simulator(player)
        self.simulator.dealer = MagicMock(spec=Dealer)
  