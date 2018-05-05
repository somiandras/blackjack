from collections import Counter
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from blackjack.db import DB

COLUMNS = ['2_pl',
           '3_pl',
           '4_pl',
           '5_pl',
           '6_pl',
           '7_pl',
           '8_pl',
           '9_pl',
           'A_pl',
           'J_pl',
           'K_pl',
           'Q_pl',
           'T_pl',
           '2_ho',
           '3_ho',
           '4_ho',
           '5_ho',
           '6_ho',
           '7_ho',
           '8_ho',
           '9_ho',
           'A_ho',
           'J_ho',
           'K_ho',
           'Q_ho',
           'T_ho']


class ModelException(Exception):
    pass


class Model:
    '''
    Class for training and using a model based on learned Q values.
    '''
    trained = False

    def __init__(self):
        self.db = DB()

    def _load_data(self):
        '''
        Loads Q data from database and transforms it into features and
        labels for training the model (the model is trained on all
        available Q data).
        '''
        q = self.db.get_full_Q()

        states = q.groupby(['state', 'action']).sum().unstack()

        players = [Counter(p) for ((p, h), (hit, stand))
                   in states.iterrows() if hit != stand]
        houses = [Counter(h) for ((p, h), (hit, stand))
                in states.iterrows() if hit != stand]
        labels = [int(hit > stand) for ((p, h), (hit, stand))
                in states.iterrows() if hit != stand]

        data = pd.concat([pd.DataFrame.from_dict(players).fillna(0),
                        pd.DataFrame.from_dict(houses).fillna(0),
                        pd.Series(labels, name='label')],
                        axis=1)

        data.columns = COLUMNS + ['labels']

        self.features = data.iloc[:, :-1].values
        self.labels = data['labels'].values

    def train(self):
        '''
        Trains predictive model with the loaded features and labels.
        Saves the fitted model in class property for later access.
        '''
        self._load_data()
        pipeline = Pipeline([
            ('pca', PCA(n_components=10)),
            ('clf', RandomForestClassifier(n_estimators=30,
                                           min_samples_split=60,
                                           min_samples_leaf=30,
                                           max_depth=10))])

        pipeline.fit(self.features, self.labels)

        self.model = pipeline
        self.trained = True

    def _get_features_from_state(self, state):
        '''
        Transforms a single state instance to the feature set required
        for the trained model.

        Args:
        ----
        `state`: (tuple): tuple holding player cards and house cards

        Returns:
        -------
        `pd.DataFrame` with the feature values for the sample.
        '''
        player, house = state
        counters = [Counter(player), Counter(house)]

        player = pd.DataFrame.from_dict(counters[:1]).fillna(0)
        house = pd.DataFrame.from_dict(counters[1:]).fillna(0)

        player.columns = [col + '_pl' for col in player]
        house.columns = [col + '_ho' for col in house]

        sample = pd.concat([player, house], axis=1)
        empty = pd.DataFrame(columns=COLUMNS)
        
        return pd.concat([empty, sample]).fillna(0)

    def predict_action(self, state):
        '''
        Predicts optimal action for the given state.

        Args:
        ----
        `state`: (tuple): tuple holding player cards and house cards

        Returns:
        -------
        Predicted label (0 - "stand", 1 - "hit")
        '''
        if not self.trained:
            raise ModelException('Train model before predicting action')

        transformed = self._get_features_from_state(state)
        predicted = self.model.predict(transformed.values)
        
        return predicted[0]
