from itertools import combinations
import random
from blackjack.db import DB
from blackjack.model import Model

class Player:
    '''
    Naive implementation of a Q-learning agent, which given the states,
    possible actions and the resulting rewards tries to learn the optimal
    policy (state => action mappings) for the process.

    Q-learning on Wikipedia: https://en.wikipedia.org/wiki/Q-learning

    Most of the methods are agnostic to the decision process (ie. the
    agent is not aware that it is "playing" blackjack or else), but
    `Player.learn` and `Player._update_neighbor_states` methods do contain
    domain specific knowledge (ie. what action can lead from one neighbor
    state to the current state). When subclassing these methods and
    `Player.ACTIONS` should be overwritten.

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
    the training will end after this number of rounds. If set to 0, the
    agent will immediately proceed to testing without clearing the tables
    (default=1000).
    
    Properties
    ----------
    `ACTIONS`: list(str): constant list of possible actions the player
    can take.

    `player.t`: (int): round counter (mainly for epsilon decay functions)
    
    `self.training`: (bool): flag indicating whether the agent is in
    learning (`True`) or testing phase (`False`)
    '''
    
    ACTIONS = ['hit', 'stand']
    t = 1
    last_transition = None

    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.9, constant_epsilon=False,
                tolerance=0.01, training_rounds=1000):
        self.alpha = alpha
        self.gamma = gamma
        self._epsilon = epsilon
        self.constant_epsilon = constant_epsilon
        self.tolerance = tolerance
        self.training_rounds = training_rounds
        self.training = bool(self.training_rounds)

        self.db = DB()
        if self.training:
            self.db.clear_tables()
        else:
            self.db.clear_tables(tables=['results', 'actions'])

        self.model = Model()

    def action(self, state, options):
        '''
        Returns the chosen action from the given options for the provided
        state.

        Adds states to Q table when encountered during training phase 
        and initializes the given options as actions with zero value. 
        Based on player settings, it explores new actions with epsilon 
        propbability when Q values are available for the given state.

        Args
        ----
        `state`: (obj.): hashable object describing the current state. 

        `options`: list(str):  list of possible actions that the agent can
        choose in the given state (assuming that for the same state always
        the same actions are possible).

        Returns
        -------
        (str): the chosen action from the options list.
        '''
        if self.training:
            phase = 'Training'

            self.db.init_Q(state, self.ACTIONS)
            roll = random.random() < self.epsilon
            if roll:
                potential_actions = options
            else:
                potential_actions = self.db.argmax_Q(state, options)
 
            if len(potential_actions) > 1:
                decision = 'Exploration'
            else:
                decision = 'Exploitation'
        else:
            phase = 'Testing'
            state_in_Q = self.db.check_stateQ(state)

            if state_in_Q:
                potential_actions = self.db.argmax_Q(state, options)
                if len(potential_actions) > 1:
                    decision = 'Exploration'
                else:
                    decision = 'Exploitation'
            else:
                try:
                    pred = self.model.predict_action(state)
                except AssertionError:
                    self.model.train()
                    pred = self.model.predict_action(state)

                if pred == 0:
                    potential_actions = ['stand']
                else:
                    potential_actions = ['hit']

                decision = 'Modelled'

        action = random.choice(potential_actions)
        
        if self.training:
            self.last_transition = (state, action)

        self.db.log_action(phase, state, action, decision, self.t)

        return action

    def set_reward(self, reward, final_state):
        '''
        Should be called from outside when a reward is given for a
        decision. If the player is in training phase, initiates learning
        with the given reward value, then increment `self.t` and sets 
        `self.training` flag if necessary.

        Args
        ----
        `reward`: (int, float): amount of the reward.

        Returns: None
        ------
        '''
        if self.training:
            self.learn(reward)

        self.db.log_results(self.training, final_state, reward, self.t)

        if (not self.constant_epsilon and self.epsilon < self.tolerance) or \
                (self.constant_epsilon and self.t >= self.training_rounds):
            self.training = False
 
        self.t += 1

    def learn(self, reward):
        '''
        Takes the reward and applies the Q-approximation iteration
        backwards in the chain of possible (state, action) pairs.

        Args
        ----
        `reward` (int): the reward amount to use in learning.

        Returns: None
        -------
        '''
        if self.last_transition:
            state, action = self.last_transition
            self._update_Q_value(state, action, reward, 0)
            self._update_neighbor_states(state, 'hit')
        
        self.last_transition = None

    def _update_Q_value(self, state, action, reward, next_Q):
        '''
        Update Q value of the given action on a given state using the 
        preconfigured parameters.

        Args
        ----
        `state`: (obj): the state that needs to be updated

        `action`: (str): the action whose Q value should be updated

        `reward`: the immediate reward for getting into the state

        'next_Q`: the max Q value of the state where `action` could lead
        from `state`

        Returns: None
        -------
        '''
        old_value = self.db.get_Q_value(state, action)
        new_value = (1 - self.alpha) * old_value + \
            self.alpha * (reward + self.gamma * next_Q)
        
        self.db.set_Q(state, action, new_value)
    
    def _update_neighbor_states(self, state, action):
        '''
        Neighbor state is a state from which the player can end up in
        the current state by taking the given action. The method finds
        these "backwards" and recursively updates Q values for any 
        possible states that can be a "predecessor" to the current state
        in a chain of actions.

        This includes finding n-1 length combinations of player cards and
        combine these hands with the known house card. Update Q values 
        for all these states, and recursively apply the method to these
        states too.

        Example:  
        > Player has (2 3 K A), house holds K, therefore the "direct"
        neighbors are ((2 3 K), K), ((2 3 A), K), ((2 K A), K) and 
        ((3 K A), K). All of these has more neighbors (2-card combinations
        from 2 3 K A wih K as house cards).

        Args
        ---- 
        `state`: the current state from which we traverse the network of
        "neighbors"  

        `action`: the action that can lead from a neighbor to the current
        state

        Returns: None
        ------
        '''
        player_cards, house_card = state
        max_Q = self.db.max_Q(state)

        if len(player_cards) > 2:
            combos = combinations(player_cards, len(player_cards) - 1)
            neighbor_states = [((combo, house_card), action) for combo in combos]
        
            for neighbor_state, action in neighbor_states:
                self.db.init_Q(neighbor_state, self.ACTIONS)
                self._update_Q_value(neighbor_state, action, 0, max_Q)
                self._update_neighbor_states(neighbor_state, 'hit')
    
    @property
    def epsilon(self):
        '''
        Returns the epsilon value to be used in the current decision. 
        
        Returns: 
        -------
        (float): epsilon value:  
        if `self.constant_epsilon` is `False` it is the "decayed" value,  
        if `self.constant_epsilon` is `True`, this returns the initial
        `epsilon` value, 
        if `self.training` is `False` it is 0.
        '''
        if self.constant_epsilon:
            return self._epsilon * self.training
        else:
            return self._decay_func() * self.training

    def _decay_func(self):
        '''
        Replacable decay function for decreasing `epsilon` during the
        course of training.

        Returns
        -------
        self.epsilon ** self.t
        '''
        return self._epsilon ** self.t
