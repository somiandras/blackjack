from blackjack.dealer import Dealer
from blackjack.player import Player
from blackjack.db import DB

class Simulator:
    '''
    Class for running series of blackjack games with one player and some
    parameters for configuring the simulation. Under the hood uses
    `blackjack.Dealer`.

    Args:  
    `player`: configured blackjack.Player instance which is added to the
    underlying blackjack.Dealer object.  
    `test_games`: number of rounds for testing the learning after 
    training phase is finished
    '''
    def __init__(self, player, test_games=100):
        self.player = player
        self.test_games = test_games
        self.dealer = Dealer(self.player)
        self.db = DB()
        
    def run(self):
        '''
        Runs the simulation in two phases: 
        1) training until the `player.training` flag is set to `True`   
        2) testing after training flag is set to `False`.

        Returns: self
        '''
        rounds = 1
        while self.player.training:
            self.dealer.run_game()
            print(' >> {} training round done'.format(
                rounds), end="\r", flush=True)
            rounds += 1

        print()

        for test in range(1, self.test_games + 1):
            self.dealer.run_game()
            print(' >> {} testing round done'.format(
                test), end="\r", flush=True)
        
        self.db.export_test_results()
        print()

        return self
