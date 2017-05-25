"""

"""


import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.base import clone
from sklearn import metrics
from sklearn.externals import joblib

from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

import pre_processing as pre

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

titles = pre.reading_titles('data/game_titles.csv')
genres, num_games, num_attributes = pre.reading_votes('data/game_genres.csv')
id, taglines = pre.reading_taglines('data/game_tagline.csv')

y_mat = np.zeros((len(id),32))
X_mat = []
X_titles = []
kk = 0;
for ii in range(0,len(id)):
    tagline_index = np.where(genres[:,0]==int(id[ii]))
    if len(tagline_index[0])>0:
        X_mat.append(taglines[ii])
        for jj in range(0,len(tagline_index[0])):
            genre = int(genres[tagline_index[0][jj],1])
            y_mat[kk,genre-1] = 1
    else:
        X_mat.append(taglines[ii])
    kk = kk+1

tfid_vectorizer = TfidfVectorizer(X_mat,
                    tokenizer=LemmaTokenizer(), 
                    stop_words='english',analyzer='word')
                    
tfidf_normalizer = TfidfTransformer(norm='l2',use_idf=True,smooth_idf=True)

pipeline = Pipeline([
('vect', tfid_vectorizer),
('tfidf', tfidf_normalizer),
('clf', MultinomialNB())
])

model_collection = []
for genre in range(0,31):
    clf_clone = clone(pipeline)
    clf_clone.fit(X_mat, y_mat[:, genre])
    model_collection.append(clf_clone)

joblib.dump(model_collection, 'data/model_collection.pkl') 

