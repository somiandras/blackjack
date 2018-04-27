import random
from blackjack.logger import Logger


class PlayerException(Exception):
    pass


class Player:
    Q = dict()
    t = 0
    transitions = []
    training = True

    def __init__(self, alpha=0.5, gamma=0.5, epsilon=0.9, tolerance=0.05):
        self.alpha = 0.5
        self.gamma = gamma
        self._epsilon = epsilon
        self.tolerance = 0.05

    def action(self, player_cards, house_cards):
        state = (tuple(sorted(player_cards)), tuple(house_cards))
        
        if state not in self.Q:
            self.Q[state] = {'hit': 0, 'stand': 0}

        roll = random.random()
        if roll < self.epsilon:
            action = random.choice(['stand', 'hit'])
        else:
            maxQ = max([value for key, value in self.Q[state].items()])
            potential_actions = [a for a, q in self.Q[state].items() if q == maxQ]
            action = random.choice(potential_actions)

        if self.training:
            self.transitions.append((state, action))

        return action

    def reward(self, reward):
        if self.training:
            self.learn(reward)

        if self.epsilon < self.tolerance:
            self.training = False

        self.transitions = []
        self.t += 1
    
    def learn(self, reward):
        for step, (state, action) in enumerate(reversed(self.transitions)):
            if step == 0:
                mod_factor = reward
            else:
                prev_state = self.transitions[step - 1][0]
                prev_max_Q = max([v for a, v in self.Q[prev_state].items()])
                mod_factor = self.gamma * prev_max_Q

            self.Q[state][action] = (1 - self.alpha) * self.Q[state][action] + \
                                self.alpha * mod_factor

    @property
    def epsilon(self):
        return self._epsilon ** self.t
