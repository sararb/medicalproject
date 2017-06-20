# Define the functions nltk that process the text
import nltk
#nltk.download()
from nltk import word_tokenize
import re
from nltk.corpus import stopwords
import string
from nltk.stem.snowball import SnowballStemmer


class cleaning_review():
    def chunk_mot(self, sentences):
        """
        :param sentences:
        split text to a set of words : bag-of-words"""
        return nltk.word_tokenize(sentences)

    def no_punctuation(self, words):
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

    def delete_stop_words(self, words):
        """
        :param words
        return the set of words without insignifiant words like : le , de, ces, the...
        """
        stops = set(stopwords.words('french') + stopwords.words('english'))
        return [mot for mot in words if mot not in stops]

    def word_stemmer(self, words):
        """

        :param words:
        :return:
        """
        snowball = SnowballStemmer('french')
        return [snowball.stem(mot) for mot in words]

    def nltk_words(self, words, stemm=True):
        """
        :param words:
        :param stemm:
        :return:
        """
        if stemm:
            return self.word_stemmer(self.delete_stop_words(self.no_punctuation(words)))
        return self.delete_stop_words(self.no_punctuation(words))

    def nltk_text(self, text, stemm=True):
        text_f = self.delete_stop_words(self.no_punctuation(self.chunk_mot(text)))
        if stemm:
            text_f = self.word_stemmer(text_f)
        # reconstruct the text
        textn = ' '.join(text_f)
        return textn
