import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from learning_rf import learning_


def load_obj(name):
    """
    :param name: the path of the rf classifier
    :return:
    """
    with open(name, 'rb') as f:
        return pickle.load(f)


def build_infos(df, patient_id, path_clf):
    """
    :param df:
    :param instance: the review_text that we want to interpret
    :param path_clf: the path to the classifier that we modeled from train data
    :return:
    the list of the "n_estimator" different path_decision of the instance
    the list of
    """
    rf, feature_names = learning_()
    n_tree = rf.n_estimators

    instance = df[df['patient_id'] == patient_id]
    # get the infos for each decision tree of the rf model :
    phrases = {}
    flag = {}
    missing_words = {}
    classes = {}
    print('Rules used to predict sample %s: ' % patient_id)
    for i in range(n_tree):
        phrases[i] = []
        flag[i] = []
        estimator = rf.estimators_[i]
        feature = estimator.tree_.feature
        threshold = estimator.tree_.threshold
        node_indicator = estimator.decision_path(instance)
        activated_node_index = node_indicator.nonzero()[1]
        classes[i] = estimator.predict(instance)[0]

        for node_id in activated_node_index:
            if instance[0, feature[node_id]] <= threshold[node_id]:
                phrases[i].append(feature_names[feature[node_id]])
                flag[i].append('left')
            else:
                phrases[i].append(feature_names[feature[node_id]])
                flag[i].append('right')
        missing_words[i] = set(feature_names[feature]).difference(feature_names[feature[activated_node_index]])

    return phrases, flag, classes, missing_words
