import unittest
from unittest.mock import MagicMock
from blackjack.model import Model
import pandas as pd


class TestModel(unittest.TestCase):
    def test_get_features_from_state(self):
        self.model = Model(MagicMock())
        state = (('2', '3'), 'T')
        columns = ['2_pl',
                   '3_pl',
                   '4_pl',
                   '5_pl',
                   '6_pl',
                   '7_pl',
                   '8_pl',
                   '9_pl',
                   'A_pl',
                   'J_pl',
                   'K_pl',
                   'Q_pl',
                   'T_pl',
                   '2_ho',
                   '3_ho',
                   '4_ho',
                   '5_ho',
                   '6_ho',
                   '7_ho',
                   '8_ho',
                   '9_ho',
                   'A_ho',
                   'J_ho',
                   'K_ho',
                   'Q_ho',
                   'T_ho']

        values = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        d = [{col: value for col, value in zip(columns, values)}]
        expected = pd.DataFrame.from_dict(d)

        transformed = self.model._get_features_from_state(state)
        
        self.assertEqual(expected.equals(transformed), True)
