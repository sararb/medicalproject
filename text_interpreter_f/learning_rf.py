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
    features_names = vectorizer.get_feature_names()
    feature_names = np.asarray(features_names)
    rf.fit(X_train, y)
    directory = os.getcwd()
    save_obj(rf, os.path.join(directory, path_clf))

    return rf, X_train, feature_names, vectorizer

