import random
from blackjack.logger import Logger


class Player:
    

    Q = dict()
    t = 0
    transitions = []
    training = True

    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.9, no_decay=False,
                tolerance=0.01, training_rounds=10000):
        self.alpha = alpha
        self.gamma = gamma
        self._epsilon = epsilon
        self.no_decay = no_decay
        self.tolerance = tolerance
        self.training_rounds = training_rounds

    def action(self, state, options):
        
        # Initialize state in Q collection with 0 for al
        #  possible options if agent is currently learning
        if state not in self.Q and self.training:
            self.Q[state] = dict()
            for option in options:
                self.Q[state][option] = 0

        roll = random.random()
        if roll < self.epsilon or state not in self.Q:
            # If agent is testing and state is unkown or the exploration
            # "roll" is less then epsilon, randomly choose from options
            potential_actions = options
        else:
            # Get max Q value from Q collection for the given state and
            # randomly choose action from actions with the max. Q
            maxQ = max([value for key, value in self.Q[state].items()])
            potential_actions = [a for a, q in self.Q[state].items() if q == maxQ]
        
        action = random.choice(potential_actions)
        
        if self.training:
            self.transitions.append((state, action))

        return action

    def reward(self, reward):
        if self.training:
            self.learn(reward)

        self.transitions = []
        self.t += 1

        if (not self.no_decay and self.epsilon < self.tolerance) or \
            (self.no_decay and self.t > self.training_rounds):
            self.training = False
    
    def learn(self, reward):
        # TODO: This is just a part of the Q iteration, we should update
        # all other states that could in theory lead to final state where
        # reward is given. The current implementation propagates reward
        # only to Q(s, a) of the action chain that directly lead to it.

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
        if self.no_decay:
            return self._epsilon * self.training
        else:
            return (self._epsilon ** self.t) * self.training
