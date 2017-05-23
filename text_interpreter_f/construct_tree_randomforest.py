import pickle



def load_obj(name):
    """
    to load existing model already learned
    :param name: the path of the rf classifier
    :return:
    """
    with open(name, 'rb') as f:
        return pickle.load(f)


def build_infos(name_clf, instance, feature_names):
    """

    :param name_clf: the path of the rf classfier
    :param instance: if the id of the patient
    :param feature_names: the vocabulary of the corpus
    :return:
    """

    # load the model
    rf = load_obj(name_clf)

    # get the trees of the Random forest
    n_tree = rf.n_estimators

    # get the infos for each decision tree of the rf model :

    # a dict to save the path that lead to the prediction given by each tree
    # ##### the key is the id of the tree and the value is the list of the nodes activated
    phrases = {}

    # a dict where the key is the id of a tree and the value is a list of flags "right / left" related to each node
    flag = {}

    # key is the id of tee and the value is a list of the non activated nodes
    missing_words = {}

    # key is id of the tree and the value is an integer related to the predicted class
    classes = {}
    print('Rules used to predict sample %s: ' % instance)




    for i in range(n_tree):
        phrases[i] = []
        flag[i] = []
        # ght the tree i
        estimator = rf.estimators_[i]
        # get all the nodes of tree i
        feature = estimator.tree_.feature
        # get the values of the split decision
        threshold = estimator.tree_.threshold
        # get the index of the activated nodes
        node_indicator = estimator.decision_path(instance)
        activated_node_index = node_indicator.nonzero()[1]
        # get the predicted class by tree i
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
