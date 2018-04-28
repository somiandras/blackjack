from blackjack.dealer import Dealer
from blackjack.player import Player
from blackjack.logger import Logger


class Simulator:
    '''
    Class for running series of blackjack games with one player and some
    parameters for configuring the simulation. Under the hood uses
    `blackjack.Dealer` and `blackjack.Logger`.

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
        self.logger = Logger()
        
    def run(self):
        '''
        Runs the simulation in two phases: 1) training until the 
        `player.training` flag is set to `True` 2) testing after training
        flag is set to `False`.

        After training and testing is done this method logs what the 
        player has "learned" by logging `player.Q`.

        Returns: self
        '''
        rounds = 0
        while self.player.training:
            self.dealer.run_game()
            rounds += 1

        for _ in range(self.test_games):
            self.dealer.run_game()
            rounds += 1

        self.logger.log_Q(self.player.Q)

        return self
    
    def report(self, *args, **kwargs):
        '''
        Wrapper method for blackjack.logger.report(). All arguments are
        passed unchanged.

        Returns: self
        '''
        self.logger.report(*args, **kwargs)

        return self
