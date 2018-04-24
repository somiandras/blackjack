import unittest
from unittest.mock import MagicMock
from blackjack.simulator import Simulator, SimulatorException, Player


class TestSimulator(unittest.TestCase):

    def setUp(self):
        mocked_player = MagicMock(spec=Player)
        self.simulator = Simulator(mocked_player)

    def test_run(self):
        pass
