import os

class Logger():
    def __init__(self):
        try:
            os.remove('logs/action_log.txt')
        except FileNotFoundError:
            pass

        with open('logs/action_log.txt', 'w') as log:
            log.write('Phase   \tHouse\tPlayer    \tAction\n')

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
