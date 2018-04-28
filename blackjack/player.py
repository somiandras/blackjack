import random
from blackjack.logger import Logger


class Player:
    '''
    Naive implementation of a Q-learning agent, which given the states,
    possible actions and the resulting rewards tries to learn the optimal
    policy (state => action mappings) for the process.

    Q-learning on Wikipedia: https://en.wikipedia.org/wiki/Q-learning

    In general most of the methods are agnostic to the decision process 
    (ie. the agent is not aware that it is "playing" blackjack or else).

    Args:
    -----
    `alpha`: (float): learning rate in the iterative approximation.
    Should be in [0-1] (default=0.5)  

    `gamma`: (float): discount rate to "decay" the effect of a reward 
    towards states that are "further" away in the chain of actions.
    Should be in [0-1] (default=0.9)  
    
    `epsilon`: (float): starting epsilon value for the probability of
    exploration (random choice even when the agent has previous knowledge
    on the given state). Should be in [0-1] (default=0.9)  
    
    `constant_epsilon`: (bool) if set True, `epsilon` value will be
    used in all training rounds, otherwise it is "decayed" with the 
    `epsilon_decay` method. (default=False).  
    
    `tolerance`: (float): if `epsilon` is decayed with a function
    training will stop when `epsilon` falls below `tolerance`. It should 
    be a sufficiently low float (default=0.01).  
    
    `training_rounds`: (int) when `constant_epsilon` is set to `True`
    the training will end after this number of rounds (default=1000).
    
    Properties
    ----------
    `player.Q`: (dictionary): dict holding the learned Q values. Top level
    keys are the states, second level keys are the actions and
    approximated Q values are the values.

    `player.t`: (int): round counter (mainly for epsilon decay functions)
    
    `self.training`: (bool): flag indicating whether the agent is in
    learning (`True`) or testing phase (`False`)
    '''    

    Q = dict()
    t = 0
    transitions = []
    training = True

    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.9, constant_epsilon=False,
                tolerance=0.01, training_rounds=1000):
        self.alpha = alpha
        self.gamma = gamma
        self._epsilon = epsilon
        self.constant_epsilon = constant_epsilon
        self.tolerance = tolerance
        self.training_rounds = training_rounds

    def action(self, state, options):
        '''
        Returns the chosen action from the given options for the provided
        state.

        Adds states to `self.Q` dictionary when encountered during
        training phase and initializes the given options as actions with
        zero value. Based on player settings, it explores new actions
        with epsilon propbability when Q values are available for the
        given state.

        Args:  
        `state`: (obj.): hashable object describing the current state.  
        `options`: list(str):  list of possible actions that the agent can
        choose in the given state (assuming that for the same state always
        the same actions are possible).

        Returns: (str): the chosen action from the options list.
        '''

        if state not in self.Q and self.training:
            self.Q[state] = dict()
            for option in options:
                self.Q[state][option] = 0

        roll = random.random()
        if roll < self.epsilon or state not in self.Q:
            potential_actions = options
        else:
            maxQ = max([value for key, value in self.Q[state].items()])
            potential_actions = [a for a, q in self.Q[state].items() if q == maxQ]
        
        action = random.choice(potential_actions)
        
        if self.training:
            self.transitions.append((state, action))

        return action

    def set_reward(self, reward):
        '''
        Method is called when a decision round is ended and reward is
        given. If the player is in training phase, initiates learning
        with the given reward value, then increment `self.t` and empties
        cached transitions, and sets `self.training` flag if necessary.

        Note: currently the `Player` class works with decision "rounds" 
        which can contain multiple (state, action) pairs but has a single
        reward at the and of the decision round.

        Args.
        `reward`: (int, float): amount of the reward.

        Returns: None

        '''
        if self.training:
            self.learn(reward)

        self.t += 1
        self.transitions = []

        if (not self.constant_epsilon and self.epsilon < self.tolerance) or \
            (self.constant_epsilon and self.t > self.training_rounds):
            self.training = False
    
    def learn(self, reward):
        '''
        Takes the reward and applies the Q-approximation iteration
        backwards in the chain of (state, action) pairs.

        Note: currently the `Player` class works with decision "rounds" 
        which can contain multiple (state, action) pairs but has a single
        reward at the end of the decision round.

        Also, the value approximation is not complete as currently the 
        method only considers (state, action) pairs that directly lead
        to the final reward, and does not try to find other "neighbor"
        states that should also receive the some of the propagated
        reward (to support later decisions).

        Args:
        `reward` (int): the reward amount to use in learning.

        Returns: None
        '''
        rev_transitions = list(reversed(self.transitions))
        for step, (state, action) in enumerate(rev_transitions):
            if step == 0:
                mod_factor = reward
            else:
                prev_state = rev_transitions[step - 1][0]
                prev_max_Q = max([v for a, v in self.Q[prev_state].items()])
                mod_factor = self.gamma * prev_max_Q

            self.Q[state][action] = (1 - self.alpha) * self.Q[state][action] + \
                                self.alpha * mod_factor

    @property
    def epsilon(self):
        '''
        Returns the epsilon value to be used in the current decision. 
        
        Returns: (float): epsilon value.  
        if `self.constant_epsilon` is `False` it is the "decayed" value,  
        if `self.constant_epsilon` is `True`, this returns the initial
        `epsilon` value, 
        if `self.training` is `False` it is 0.
        '''
        if self.constant_epsilon:
            return self._epsilon * self.training
        else:
            return (self._epsilon ** self.t) * self.training
