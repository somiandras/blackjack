import random


class PlayerException(Exception):
    pass


class Player:
    Q = dict()
    t = 0
    transitions = []

    def __init__(self, alpha=0.5, gamma=0.5, epsilon=0.999, tolerance=0.05):
        self.alpha = 0.5
        self.gamma = gamma
        self._epsilon = epsilon
        self.tolerance = 0.05

    def take_action(self, player_cards, house_cards, test=False):
        state = (tuple(sorted(player_cards)), tuple(house_cards))
        if state not in self.Q:
            self.Q[state] = {'hit': 0, 'stand': 0}

        roll = random.random()
        if roll < self.epsilon:
            action = random.choice(['stand', 'hit'])
        else:
            maxQ = max([value for key, value in self.Q[state].items()])
            potential_actions = [action for action, q in self.Q[state].items() if q == maxQ]
            action = random.choice(potential_actions)

        if not test:
            self.transitions.append((state, action))

        return action

    def close_round(self, reward, test):
        if not test:
            self.process_transitions(reward)
        self.transitions = []
        self.t += 1

        if self.epsilon < self.tolerance:
            # Training has to be finished
            return False
        else:
            # Continue training
            return True
    
    def process_transitions(self, reward):
        self.transitions.reverse()
        for step, (state, action) in enumerate(self.transitions):
            
            if step == 0:
                mod_factor = reward
            else:
                prev_state = self.transitions[step - 1][0]
                prev_max_Q = max(
                    [value for action, value in self.Q[prev_state].items()])
                mod_factor = self.gamma * prev_max_Q

            self.Q[state][action] = (1 - self.alpha) * self.Q[state][action] + \
                                self.alpha * mod_factor

    @property
    def epsilon(self):
        return self._epsilon ** self.t
