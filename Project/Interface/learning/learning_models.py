import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import os
import pickle


class learning():
    def save_obj(self, obj, name):
        with open(name, 'wb') as handle:
            pickle.dump(obj, handle)

    def learning_rf(self, text_train, y, path_clf):
        """

                :param clf:
                :param text_train:
                :param y:
                :param path_clf:
                :return:
                """

        # the the bag of word representation :
        vectorizer = TfidfVectorizer(max_df=0.8, min_df=3)
        X_train = vectorizer.fit_transform(text_train)
        features_names = np.asarray(vectorizer.get_feature_names())
        # TODO : add Hyperopt/gridsearch for Hyper-parameter selection
        #gridsearch
        param_grid = {'max_depth': [5, 10, 25, 35],
                      'min_samples_split': [5, 10, 15, 20, 25],
                      'n_estimators': [10, 20, 50, 100, 200],
                      'bootstrap': [True, False],
                      'criterion': ["gini", "entropy"]}
        rf = RandomForestClassifier()
        grid_search = GridSearchCV(rf, param_grid=param_grid, cv=5, n_jobs=-1)
        grid_search.fit(X_train, y)
        print(grid_search.best_score_)
        rf = RandomForestClassifier(grid_search.best_params_)

        # TODO : get the f1-score : from Hyperopt object

        # from sklearn.model_selection import cross_val_predict
        # predicted = cross_val_predict(rf_best, X_train, y, cv=5)
        # from sklearn.metrics import confusion_matrix
        # confusion_matrix(predicted, y)
        # compute the f1 score

        # apply our best model to all the dataframe
        rf.fit(X_train, y)

        directory = os.getcwd()
        # save the learned best  model
        self.save_obj(rf, os.path.join(directory, path_clf))

        # TODO : save the evaluation metrics

        return rf, X_train, features_names
