import os
import pickle
import sqlite3
import pandas as pd
import re


def tuple_adapter(input):
    return str(input)


def convert_state(state):
    match = re.match(r'\(\((.*)\),\s(.{3})\)', state.decode('utf-8'))
    player = match.group(1).replace('\'', '').replace(' ', '').split(',')
    house = match.group(2).replace('\'', '')

    return (tuple(player), house)


sqlite3.register_adapter(tuple, tuple_adapter)
sqlite3.register_converter('state', convert_state)


class DB():
    def __init__(self):
        try:
            os.mkdir('db')
        except FileExistsError:
            pass

        try:
            with self.connection as con:
                con.execute('''
                    CREATE TABLE results (phase TEXT, state TEXT, result INTEGER,
                    round_no INTEGER PRIMARY KEY);
                ''')
        except sqlite3.OperationalError:
            pass

        try:
            with self.connection as con:
                con.execute('''
                    CREATE TABLE actions (phase TEXT, state TEXT, action TEXT, 
                    decision TEXT, round_no TEXT);
                ''')
        except sqlite3.OperationalError:
            pass

        try:
            with self.connection as con:
                con.execute('''
                  CREATE TABLE Q (state TEXT, action TEXT, value INT,
                  PRIMARY KEY (state, action))
                ''')
        except sqlite3.OperationalError:
            pass

    @property
    def connection(self):
        return sqlite3.connect(
            'db/blackjack.db', timeout=10, detect_types=sqlite3.PARSE_COLNAMES)

    def clear_tables(self):
        with self.connection as con:
            try:
                con.execute('DELETE FROM results')
                con.execute('DELETE FROM actions')
                con.execute('DELETE FROM Q')
            except sqlite3.OperationalError as e:
                print(e)

    def log_action(self, training, state, action, decision, round_no):

        if training:
            phase = 'Training'
        else:
            phase = 'Testing'

        with self.connection as con:
            con.execute('INSERT INTO actions VALUES (?,?,?,?,?)',
                        (phase, state, action, decision, round_no))

    def max_Q(self, state, keys=None):
        if keys is None:
            query = '''
                SELECT
                    state, MAX(value)
                FROM Q
                WHERE
                    state = ?
                GROUP BY state
            '''
            args = (state, )
        else:
            seq = ','.join(['?'] * len(keys))
            query = '''
                SELECT
                    state, MAX(value)
                FROM Q
                WHERE
                    state = ? AND
                    action IN ({})
                GROUP BY state
            '''.format(seq)
            args = (state, *keys)

        with self.connection as con:            
            cursor = con.execute(query, args)

            _, max_Q = cursor.fetchone()
        
        return max_Q

    def init_Q(self, state, actions):
        with self.connection as con:
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
        with self.connection as con:
            cursor = con.execute('''
                SELECT state 
                FROM Q 
                WHERE
                    state = ?
            ''', (state,))
            
            return bool(cursor.fetchone())
    
    def get_Q_value(self, state, action):
        with self.connection as con:
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

    def argmax_Q(self, state, keys=None):
        max_Q = self.max_Q(state, keys)

        if keys is None:
            query = '''
                SELECT state, action, value
                FROM Q
                WHERE
                    value = ? AND
                    state = ?
            '''
            args = (max_Q, state)
        else:
            seq = ','.join(['?'] * len(keys))
            query = '''
                SELECT state, action, value
                FROM Q
                WHERE
                    value = ? AND
                    state = ? AND
                    action IN ({})
            '''.format(seq)
            args = (max_Q, state, *keys)

        with self.connection as con:
            cursor = con.execute(query, args)

            all_records = cursor.fetchall()
            if all_records is not None:
                return [action for s, action, v in all_records]
            else:
                return None

    def set_Q(self, state, action, value):
        with self.connection as con:
            con.execute('''
                UPDATE Q 
                SET value = ? 
                WHERE 
                    state = ? AND
                    action = ?
            ''', (value, state, action))

    def get_full_Q(self):
        with self.connection as con:
            q = pd.read_sql(
                'SELECT state as "state [state]", action, value FROM Q', con)

        return q

    def log_results(self, training, final_state, reward, round_no):

        if training:
            phase = 'Training'
        else:
            phase = 'Testing'
        
        with self.connection as con:
            con.execute('INSERT INTO results VALUES (?,?,?,?)',
                        (phase, final_state, reward, round_no))
