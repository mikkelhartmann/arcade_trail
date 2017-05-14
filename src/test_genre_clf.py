import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

from sklearn.base import clone

from sklearn.pipeline import Pipeline
from sklearn import metrics

from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

from sklearn.externals import joblib

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

genre_names = ['Action', 'Indie', 'Strategy', 'Early Access', 'Free to Play', 'Massively Multiplayer', 'RPG',
               'Adventure', 'Casual', 'Simulation', 'Racing', 'Sports', 'Audio Production', 'Utilities', 
               'Video Production', 'Education', 'Design & Illustration', 'Web Publishing', 'Photo Editing',
               'Software Training', 'Animation & Modeling', 'Puzzle', 'Platformer', 'Survival', 'Shooter', 
               'Horror', 'Sandbox', 'Music', 'Fighting', 'Hidden Objects', 'Accounting']

model_collection = joblib.load('model_collection.pkl') 
example = ['Shoot your way through the jungle to survive']
pred_list = []
for idx, clf in enumerate(model_collection):
    pred = clf.predict_proba(example)
    pred_list.append(pred[:,1])
    #print(pred[:,1], genre_names[idx])

sort_idx = sorted(range(len(pred_list)), key=lambda k: pred_list[k], reverse=True)
my_list = [(pred_list[idx], genre_names[idx]) for idx in sort_idx]
print(my_list)