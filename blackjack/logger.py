import os
import pickle
import sqlite3

def tuple_adapter(input):
    return str(input)

sqlite3.register_adapter(tuple, tuple_adapter)

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
                    CREATE TABLE results (phase TEXT, state TEXT, result INTEGER);
                ''')
        except sqlite3.OperationalError:
            con.execute('DELETE FROM results')

        try:
            with self.con as con:
                con.execute('''
                    CREATE TABLE actions (phase TEXT, state TEXT, action TEXT);
                ''')
        except sqlite3.OperationalError:
            con.execute('DELETE FROM actions')

        try:
            with self.con as con:
                con.execute('''
                  CREATE TABLE Q (state TEXT, action TEXT, value INT,
                  PRIMARY KEY (state, action))
                ''')
        except sqlite3.OperationalError:
            con.execute('DELETE FROM Q')

    def log_action(self, training, state, action):

        if training:
            phase = 'Training'
        else:
            phase = 'Testing'

        with self.con as con:
            con.execute('INSERT INTO actions VALUES (?,?,?)',
                        (phase, state, action))

    def max_Q(self, state):
        with self.con as con:            
            cursor = con.execute('''
                SELECT 
                    state, MAX(value) 
                FROM Q
                WHERE
                    state = ?
                GROUP BY state
            ''', (state, ))

            _, max_Q = cursor.fetchone()
        
        return max_Q

    def init_Q(self, state, actions):
        with self.con as con:
            cursor = con.execute('''
                SELECT
                    state, action, value
                FROM Q
                WHERE state = ?
            ''', (state,))

            if cursor.fetchone() is None:
                for action in actions:
                    con.execute('INSERT INTO Q VALUES (?, ?, 0)', (state, action))
            
    def check_stateQ(self, state):
        with self.con as con:
            cursor = con.execute('''
                SELECT state 
                FROM Q 
                WHERE
                    state = ?
            ''', (state,))
            
            return bool(cursor.fetchone())
    
    def get_Q_value(self, state, action):
        with self.con as con:
            cursor = con.execute('''
                SELECT 
                    state, action, value 
                FROM Q
                WHERE
                    state = ? AND
                    action = ?
            ''', (state, action))

            result = cursor.fetchone()
            if result is not None:
                _, _, value = result
                return value
            else:
                return None

    def argmax_Q(self, state):
        max_Q = self.max_Q(state)
        with self.con as con:
            cursor = con.execute('''
                SELECT state, action, value
                FROM Q
                WHERE
                    value = ? AND
                    state = ?
            ''', (max_Q, state))

            if cursor is not None:
                return [action for s, action, v in cursor]
            else:
                return None

    def set_Q(self, state, action, value):
        with self.con as con:
            con.execute('''
                UPDATE Q 
                SET value = ? 
                WHERE 
                    state = ? AND
                    action = ?
            ''', (value, state, action))

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
    
    def log_results(self, training, final_state, reward):

        if training:
            phase = 'Training'
        else:
            phase = 'Testing'
        
        with self.con as con:
            con.execute('INSERT INTO results VALUES (?,?,?)',
                        (phase, final_state, reward))
