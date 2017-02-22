# This is the python implementation of the reccomender system i first developed
# in MatLab
# export LC_ALL=en_US.UTF-8
# export LANG=en_US.UTF-8

# ------------------------------------------------------------------------------
# TO DO
# * Implement the cross validation
# * Make it work with flaskr
# * Make Singular Value Decomposition work with more features
# ------------------------------------------------------------------------------

import ReccomenderSystem
from numpy import *
import numpy as np
from random import randrange
import operator
from os import listdir
import csv
import scipy
import scipy.optimize
import itertools
import matplotlib.pyplot as plt

# Loading the Data
votes, num_games_1, num_users_1 = ReccomenderSystem.reading_votes('CSV/game_votes.csv')
ownerships, num_games_2, num_users_2 = ReccomenderSystem.reading_votes('CSV/game_ownerships.csv')

# since the number of users from the votes and ownerships lists may differ
# i chose the largest one here
num_games = max([num_games_1, num_games_2])
num_users = max([num_users_1, num_users_2])
titles = ReccomenderSystem.reading_titles('CSV/game_titles.csv')
genres, num_games, num_attributes = ReccomenderSystem.reading_votes('CSV/game_genres.csv')
genre_titles = ReccomenderSystem.reading_titles('CSV/genre_titles.csv')
user_names = ReccomenderSystem.reading_titles('CSV/user_names.csv')

taglines = ReccomenderSystem.reading_taglines('../CSV/game_tagline.csv')

# Constructing R
R = ReccomenderSystem.construct_R(votes,ownerships,num_users,num_games)
np.save('R',R)

# ------------------------------------------------------------------------------
# Non-personalized reccomendations
# Getting the reccomendations from the simple sorting
# ------------------------------------------------------------------------------
user_id = 46
ReccomenderSystem.getMostPopularGames(votes,R,titles,user_names,user_id)
# ------------------------------------------------------------------------------
# Personalized reccomendations
# Content Based Reccomendations
# ------------------------------------------------------------------------------
user_id = 46
attrVec = ReccomenderSystem.construct_attrVec(genres,num_games,num_attributes)
ContentBasedPredictions = ReccomenderSystem.construct_ContentBasedPredictions(attrVec,R)
ReccomenderSystem.getContentBasedPrecition(ContentBasedPredictions,titles,user_names,user_id)

# ------------------------------------------------------------------------------
# Personalized reccomendations
# Running collaborative filtering
# ------------------------------------------------------------------------------
print('Using 1 feature')
num_features = 1
regularization = 10
X, Theta =  ReccomenderSystem.collaberative_filtering(num_games,num_users,num_features,R,regularization)

# Saving the trained model
np.save('X',X)
np.save('Theta',Theta)

user_id = 46
reccomendation_string = ReccomenderSystem.getting_reccomendations(R,Theta,X,titles,user_names,user_id)

print str(reccomendation_string)
