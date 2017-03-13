# to execute the script, one should type :
#  python text_preprocessing.py -filepath "./data.csv" -str_clean True -ntlk_clean True

import pandas as pd
import re
import numpy as np
from clean_nltk import nltk_words, chunk_mot
import argparse
from sklearn.preprocessing import LabelEncoder
import sys

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# ------------------------------------------ processing functions---------------------------------------------------- #
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def clean_str(string):
    """
    :param string
    Tokenization/string cleaning for all datasets except for SST.
    Code source from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[-,!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return chunk_mot(string.lower())


def nltk_stemming(words):
    """
    :param words:
    :return:
    """
    return nltk_words(words)


# Convert patient_id to integers
def convert(x):
    try:
        return int(x)
    except:
        return np.nan


def load_data_text(path_data, clean_string=True, nltk_clean=True, stemm=True):
    """
    :param path_data: the path to the dataframe that contains three columns: patient_id, review_text and the Class.
    :param clean_string : the param that allows to do the basic cleaning : remove punctuation, add space between words
                         and punctuations..
    :param stemm : if we want to  return a stemmed text
    :param nltk_clean : if we want to process the text by removing stopwords...
    :return:
    the dataframe with the sequence of processed sentences where each sentence is a list of words
    """
    df = pd.read_csv(path_data, sep=';')

    # convert labels
    le = LabelEncoder()
    labels = le.fit_transform(df['Class'])

    # process the patients' reviews :
    if clean_string:
        print('clean the reviews from noisy words and punctuations')
        # create the sequence of sentences where each sentence is a list of words
        verbatims = df['review_text'].apply(clean_str)

    else:
        verbatims = df['review_text'].apply(lambda s: s.strip().split())

    if nltk_clean:
        if stemm:
            print('stemming the reviews')
            verbatims = verbatims.apply(lambda x: nltk_words(x, stemm=True))
            return list(verbatims.apply(lambda x: ' '.join(x))), labels, df
        else:
            print('removing noisy words')
            verbatims = verbatims.apply(lambda x: nltk_words(x, stemm=False))
            return list(verbatims.apply(lambda x: ' '.join(x))), labels, df

    return list(verbatims.apply(lambda x: ' '.join(x))), labels, df


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# ------------------------------------------ Main function----------------------------------------------------------- #
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def main(args):
    parser = argparse.ArgumentParser(description="Text processing")
    parser.add_argument("-filepath", "--data_path", type=str, required=True)
    parser.add_argument("-ntlk_clean", "--nltk_clean", type=bool, default=True, required=True)
    parser.add_argument("-str_clean", "--str_clean", type=bool, default=True, required=True)
    args = parser.parse_args(args)
    return load_data_text(args.data_path, args.str_clean, args.nltk_clean)

if __name__ == "__main__":
    main(sys.argv[1:])




