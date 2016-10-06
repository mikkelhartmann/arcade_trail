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

# Constructing R
R = ReccomenderSystem.construct_R(votes,ownerships,num_users,num_games)
np.save('src/cli/R',R)
