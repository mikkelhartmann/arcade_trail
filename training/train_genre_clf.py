"""
This script trains a machine learning model that predicts the genre of a
game based on a short description (tagline) of the game.
"""


import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.base import clone
from sklearn.externals import joblib
import pre_processing as pre

taglines, y_mat = pre.pre_process()

tfid_vectorizer = TfidfVectorizer(taglines,
                    stop_words='english',
                    analyzer='word')
                    
tfidf_normalizer = TfidfTransformer(norm='l2',use_idf=True,smooth_idf=True)

pipeline = Pipeline([
('vect', tfid_vectorizer),
('tfidf', tfidf_normalizer),
('clf', LogisticRegression())
])

model_collection = []
for genre in range(0,12):
    clf_clone = clone(pipeline)
    clf_clone.fit(taglines, y_mat[:, genre])
    model_collection.append(clf_clone)

joblib.dump(model_collection, 'model_collection.pkl') 

