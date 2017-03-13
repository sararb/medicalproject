# Define the functions nltk that process the text
import nltk
import re
from nltk.corpus import stopwords
import string
from nltk.stem.snowball import SnowballStemmer


def chunk_mot(sentences):
    """
    :param sentences:
    split text to a set of words : bag-of-words"""
    return nltk.word_tokenize(sentences)


def no_punctuation(words):
    """
    :param words:
    return the set of words without puntctuation marks
     """
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    mots_no_punctuation = []
    for token in words:
        # new_token = regex.sub(u'', token.decode('utf-8'))
        new_token = regex.sub(u'', token)
        if not new_token == u'':
            mots_no_punctuation.append(new_token.lower())  # lower pour normaliser le texte
    return mots_no_punctuation


def delete_stop_words(words):
    """
    :param words
    return the set of words without insignifiant words like : le , de, ces, the...
    """
    stops = set(stopwords.words('french') + stopwords.words('english'))
    return [mot for mot in words if mot not in stops]


def word_stemmer(words):
    """

    :param words:
    :return:
    """
    snowball = SnowballStemmer('french')
    return [snowball.stem(mot) for mot in words]


def nltk_words(words, stemm=True):
    """
    :param words:
    :param stemm:
    :return:
    """
    if stemm:
        return word_stemmer(delete_stop_words(no_punctuation(words)))
    return delete_stop_words(no_punctuation(words))


def nltk_text(text, stemm=True):
    text_f = delete_stop_words(no_punctuation(chunk_mot(text)))
    if stemm:
        text_f = word_stemmer(text_f)
    # reconstruct the text
    textn = ' '.join(text_f)
    return textn
