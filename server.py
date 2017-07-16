"""

"""
import os

from flask import Flask
from flask import request, render_template
import time
import numpy as np
import re
import h5py
import pickle

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

from nltk.corpus import stopwords

from keras.models import load_model

app = Flask(__name__)

def clean_string(string):
    """
    Tokenization/string cleaning for dataset
    Every dataset is lower cased except
    """
    string = re.sub(r"\\", "", string)    
    string = re.sub(r"\'", "", string)    
    string = re.sub(r"\"", "", string)
    # Replace numbers by x
    string = re.sub("\d", "x", string) 
    string.strip().lower()
    string = remove_stop_words(string)
    return string

def remove_stop_words(description):
    word_list = description.split()
    filtered_words = [word for word in word_list if word not in stopwords.words('english')]
    description = ' '.join(filtered_words)
    return description

def embedding_description(desc, top_n_words_dict):
    game_embedding = []
    for idx, word in enumerate(desc.split()):
        if word in top_n_words_dict:
            word_idx = top_n_words_dict[word]
            game_embedding.append(word_idx)
        else:
            game_embedding.append(0)
    return game_embedding

def pre_process_for_nn(string, top_n_words_dict):
    string = clean_string(string)
    embedded = embedding_description(string, top_n_words_dict)
    a = [0] * (70 - len(embedded))
    zero_padded_example = np.array(a + embedded).reshape(-1,70)
    return(zero_padded_example)

def make_example_from_index(idx):
    example = descriptions[relevant_description_idx[idx]]
    print(example)
    tag_indices = np.where(y_mat[relevant_description_idx[idx],:]>0)[0]
    for idx in tag_indices:
        print(tag_names[idx])
    return example

def make_prediction_with_nn(zero_padded_example, nn_model_collection, selected_tag_names):
    pred_list = []
    for idx, clf in enumerate(nn_model_collection):
        pred = clf.predict_proba(zero_padded_example, verbose=0)
        pred_list.append(pred)

    sort_idx = sorted(range(len(pred_list)), key=lambda k: pred_list[k], reverse=True)
    my_list = [(pred_list[idx], selected_tag_names[idx]) for idx in sort_idx]
    for item in my_list:
        proba = item[0][0][0]
        genre_name = item[1]
        if proba > 0.05:
            print(genre_name, proba)
    return my_list

@app.route('/')
def hello_world():
    
    return render_template('landingPage.html')

@app.route('/', methods=['POST'])
def my_form_post():
    selected_tag_names = [
        'Horror',
        'Sci-fi',
        'Futuristic',
        'Fantasy',
        'Medieval',
        'Dark Fantasy',
        'Magic',
        'Atmospheric',
        'Gore',
        'World War II',
        'Zombies',
        'Mystery',
        'Survival',
        'Aliens',
        'Space',
        'Supernatural',
        'Dark',
        'Gothic',
        'Western',
        'War',
        'Historical',
        'Military',
        'Naval',
        'Racing',
        'Post-apocalyptic',
        'Cyberpunk',
        'Surreal',
        'Pirates',
        'Sports',
        'Robots',
        'Survival Horror',
        'Crime',
        'Steampunk',
        'Mythology',
        'Dystopian',
        'World War I',
        'Psychedelic',
        'Cold War',
        'Psychological Horror',
        'Dragons'
        ]
    # Loading the neural networds
    t0 = time.time()
    nn_2_model_collection = []
    for i in range(len(selected_tag_names)):
        model = load_model('models/steam_nn_model_collection_' + str(i) + '.h5')
        nn_2_model_collection.append(model)
        if i%5==0:
            t1 = time.time()
            print((t1-t0)/60, ' min to load the models')
    
    # Loading the dictionary
    top_n_words_dict = np.load('data/top_n_words_dict.npy').item()
    
    # Pre-processing the input from the text field
    text = request.form['text']
    zero_padded_example = pre_process_for_nn(text, top_n_words_dict)
    
    # Making predictions with the neural networks
    print('Predicting with neural networks ...')
    t0 = time.time()
    my_list = make_prediction_with_nn(zero_padded_example, nn_2_model_collection, selected_tag_names)
    t1 = time.time()
    print('It took ', (t1-t0)/60, ' min to make these prediction')
    
    return render_template('recommendations.html', list=my_list)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=8080)