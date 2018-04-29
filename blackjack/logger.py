import os
import pickle
import sqlite3

class Logger():
    def __init__(self):
        try:
            os.mkdir('db')
        except FileExistsError:
            pass

        self.con = sqlite3.connect('db/blackjack.db')
        try:
            with self.con as con:
                con.execute('''
                    CREATE TABLE results (phase TEXT, player TEXT, house TEXT,
                    result INTEGER);
                ''')
        except sqlite3.OperationalError:
            con.execute('DELETE FROM results')

        try:
            with self.con as con:
                con.execute('''
                    CREATE TABLE actions (phase TEXT, player TEXT, house TEXT,
                    action TEXT);
                ''')
        except sqlite3.OperationalError:
            con.execute('DELETE FROM actions')

        try:
            with self.con as con:
                con.execute('''
                  CREATE TABLE Q (state TEXT PRIMARY KEY, hit REAL, stand REAL)
                ''')
        except sqlite3.OperationalError:
            con.execute('DELETE FROM Q')

    def log_action(self, training, player_cards, house_cards, action, *args):
        hc = house_cards[0]
        pc = ' '.join(player_cards)

        if training:
            phase = 'Training'
        else:
            phase = 'Testing'

        with self.con as con:
            con.execute('INSERT INTO actions VALUES (?,?,?,?)',
                        (phase, hc, pc, action))

    def log_Q(self, Q):
        with open('logs/q.pkl', 'b+w') as q_pkl:
            pickle.dump(Q, q_pkl)

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
        
        with self.con as con:
            con.execute('INSERT INTO results VALUES (?,?,?,?)',
                        (phase, player, house, reward))
