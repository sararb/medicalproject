import text_preprocessing
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import os
import pickle


def save_obj(obj, name):
    with open(name, 'wb') as handle:
          pickle.dump(obj, handle)


def learning_(rf, text_train, y, path_clf):
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
    save_obj(rf, os.path.join(directory, path_clf))

    # TODO : save the evaluation metrics

    return rf, X_train, features_names

