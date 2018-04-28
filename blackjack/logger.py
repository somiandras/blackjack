import os
import matplotlib
matplotlib.use('AGG')
import pandas as pd
import matplotlib.pyplot as plt

class Logger():
    def __init__(self):
        try:
            os.remove('logs/action_log.txt')
            os.remove('logs/results_log.txt')
        except FileNotFoundError:
            pass

        with open('logs/action_log.txt', 'w') as log:
            log.write('Phase\tHouse\tPlayer\tAction\n')

        with open('logs/results_log.txt', 'w') as results:
            results.write('Phase\tPlayer\tHouse\tReward\n')

    def log_action(self, training, player_cards, house_cards, action):
        hc = house_cards[0]
        pc = ' '.join(player_cards)

        if training:
            phase = 'Training'
        else:
            phase = 'Testing'

        action_record = '{:8}\t{:5}\t{:10}\t{:5}\n'.format(phase, hc, pc, action)
        
        with open('logs/action_log.txt', 'a') as log:
            log.write(action_record)

    def log_Q(self, Q):
        with open('logs/q_log.txt', 'w') as q_log:
            q_log.write('Player\tHouse\tHit    \tStand\n')
            for state, action in Q.items():
                player = ' '.join(state[0])
                house = state[1]
                hit = action['hit']
                stand = action['stand']

                q_log.write(
                    '{:8}\t{:6}\t{:4.2f}\t{:4.2f}\n'.format(player, house, hit, stand))
    
    def log_results(self, training, player, house, reward):
        player = ' '.join(player)
        house = ' '.join(house)
        if training:
            phase = 'Training'
        else:
            phase = 'Testing'
        
        with open('logs/results_log.txt', 'a') as results:
            results.write('{}\t{:20}\t{:20}\t{:4}\n'.format(phase, player, house, reward))

    def report(self, rolling=1000, suffix=''):
        if len(suffix):
            suffix = '_' + suffix
        
        df = pd.read_table('logs/results_log.txt')

        fig, ax = plt.subplots()
        for phase in ['Training', 'Testing']:
            data = df[df['Phase'] == phase]
            ax.plot(data['Reward'].rolling(rolling).sum())

        fig.savefig('logs/rolling_reward{}.png'.format(suffix))
