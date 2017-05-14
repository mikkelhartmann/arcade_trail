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

import ReccomenderSystem as RC

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

titles = RC.reading_titles('data/game_titles.csv')
genres, num_games, num_attributes = RC.reading_votes('data/game_genres.csv')
id, taglines = RC.reading_taglines('data/game_tagline.csv')

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

train_size = int(round(len(y_mat)*0.8))
genre_to_train = 0
y_train = y_mat[:train_size, genre_to_train]
X_train = X_mat[:train_size]
X_test = X_mat[train_size:];
y_test = y_mat[train_size:, genre_to_train];

tfid_vectorizer = TfidfVectorizer(X_train,
                stop_words='english',analyzer='word')



tfid_vectorizer = TfidfVectorizer(X_train,
                    tokenizer=LemmaTokenizer(), 
                    stop_words='english',analyzer='word')
                    
tfidf_normalizer = TfidfTransformer(norm='l2',use_idf=True,smooth_idf=True)

X_vect = tfid_vectorizer.fit_transform([X_test[0]])

X_vect_norm = tfidf_normalizer.fit_transform(X_vect)

pipeline = Pipeline([
('vect', tfid_vectorizer),
('tfidf', tfidf_normalizer),
('clf', MultinomialNB())
])
clf = pipeline.fit(X_train, y_train)

model_collection = []
for genre in range(0,31):
    clf_clone = clone(pipeline)
    clf_clone.fit(X_mat, y_mat[:, genre])
    model_collection.append(clf_clone)

# Saving the models
from sklearn.externals import joblib
joblib.dump(model_collection, 'data/model_collection.pkl') 

