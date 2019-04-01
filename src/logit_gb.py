import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score

class LogitGB:
    """
    A 2-stage model:
    1. fit quickly using logistic regression using part of the data with many columns
    2. fit using gradient boosting on the predicted probabilites from logistic regression as well as the fewer remaining columns
        current columns: existing_stories, has_existing_stories

    This attempts to quickly capture information from many quickly (like tfidf of text), while combining that with other, non-text features
    """
    def __init__(self):
        """
        Don't need to pass anything in.
        """
        self.m1 = LogisticRegression()
        self.m2 = GradientBoostingClassifier(learning_rate = .13, loss = 'deviance', n_estimators = 500, min_samples_leaf = 4, max_depth = 3)
        self.vec = TfidfVectorizer()
        self.threshold = .5
        self.columns = ['existing_stories', 'has_existing_stories']

    def fit(self, text_mat, numerical_df, target, increase = True):
        """
        cleans up pred and target, and fits model to them.
        Also picks an optimal threshold based on training data

        input:
            text_df:array of text, lemmatized and with numbers stripped.
            numerical_data:dataframe of non-text features
                In this version, it uses existing_stories and has_existing_stories
            target:dataframe of fire rates before and after each permit
                has columns: 'fire_rate_before' and 'fire_rate_after'
            increase:bool whether we're predicting an increase in fire rate (or a decrease)
        """
        if increase:
            self.y = (target['fire_rate_after'] > target['fire_rate_before']).astype(int).values
        else:
            self.y = (target['fire_rate_after'] < target['fire_rate_before']).astype(int).values

        self.X = text_mat

        self.m1.fit(self.X, self.y)
        self.X_final = np.concatenate((numerical_df[self.columns].fillna(0).values, self.m1.predict_proba(self.X)[:,1].reshape(-1,1)),axis = 1)

        self.m2.fit(self.X_final, self.y)

        self._fit_threshold()

    def hasnumber(self, s):
        """
        check if there's a number in the string
        input:string to check
        output:bool
        """
        return bool(re.search(r'\d', s))

    def _fit_threshold(self):
        """
        set the prediction threshold to the value that gives the highest f1 score for training data.
        """
        self.threshold = 0
        current_best = 0
        for i in range(1000):
            old = self.threshold
            self.threshold = i/1000
            f = f1_score(self.y, self.predict(self.X_final))
            if f <= current_best:
                self.threshold = old
            else:
                current_best = f


    def predict_proba(self, pred, X_text):
        """
        input:
            X_num:df of non-text features.
            X_text:np array tfidf
        output:
        1d array
        """
        X_num = pred[self.columns].values
        X = np.concatenate((X_num, self.m1.predict_proba(X_text)[:,1]),axis = 1)
        return self.m2.predict_proba(X)[:,1]

    def predict(self, pred, X_text):
        """
        """
        return (self.predict_proba(X_test) > self.threshold).astype(int)
