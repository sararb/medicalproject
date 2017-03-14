# Load data
import glob
import os.path as op
import numpy as np

from glob import glob
print("Loading imdb dataset")

filenames_neg = sorted(glob(op.join('data', 'imdb1', 'neg', '*.txt')))
filenames_pos = sorted(glob(op.join('data', 'imdb1', 'pos', '*.txt')))

texts_neg = [open(f).read() for f in filenames_neg]
texts_pos = [open(f).read() for f in filenames_pos]
texts = texts_neg + texts_pos
y = np.ones(len(texts), dtype=np.int)
y[:len(texts_neg)] = 0.

import pandas as pd
df = pd.DataFrame({'review_text': texts, 'Class': y})
df.to_csv('text_classification.csv', sep=';')

