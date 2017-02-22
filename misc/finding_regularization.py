# This is the python implementation of the reccomender system i first developed
# in MatLab
import ReccomenderSystem
from numpy import *
import numpy as np
import operator
from os import listdir
import csv
import scipy
import scipy.optimize
import matplotlib.pyplot as plt

# Loading the votes
votes, num_games, num_users = ReccomenderSystem.reading_votes('CSV/game_votes_2.csv')
# Loading the ownerships
ownerships, num_games, num_users = ReccomenderSystem.reading_votes('CSV/game_ownerships_2.csv')
# Loading the titles of the games
titles = ReccomenderSystem.reading_titles('CSV/game_titles.csv')
# Loading the user names
user_names = ReccomenderSystem.reading_titles('CSV/user_names.csv')

# Constructing R
R = zeros((num_users,num_games))

# Filling with user vores
for ii in range(0,len(votes)):
    current_user = int(votes[ii,1])-1 #-1 because python starts at 0
    current_game = int(votes[ii,0])-1
    R[current_user,current_game] = 1

# Filling up with user ownerships
for ii in range(0,len(ownerships)):
    current_user = int(ownerships[ii,1])-1
    current_game = int(ownerships[ii,0])-1
    R[current_user,current_game] = 1

# Running the collaberative filtering
num_features = 1
X = np.random.randint(2,size=(num_games,num_features))
Theta = np.random.randint(2,size=(num_users,num_features))

X_long = np.reshape(X,(size(X),1))
Theta_long = np.reshape(Theta,size(Theta),1)
initial_parameters = np.append(X_long,Theta_long)

Y = R
accum_cost = zeros(30)
reg = zeros(30)
precision = zeros(30)
recall = zeros(30)
correctness_0 = zeros(30)
total_correctness = zeros(30)
F_score = zeros(30)

for i in range(1,30):
    regularization = i*2

    # doing the actual fitting
    params = scipy.optimize.fmin_cg(
        f = ReccomenderSystem.cost_function,
        x0 = initial_parameters,
        fprime = ReccomenderSystem.cost_grad,
        args=(Y, R, num_users, num_games,num_features, regularization),
        maxiter=200)

    cost = ReccomenderSystem.cost_function(
        initial_parameters, Y, R,
        num_users, num_games,num_features,
        regularization)

    accum_cost[i] = cost
    reg[i] = regularization

    # calculating metrix
    true_positive = 0;
    true_negative = 0;
    false_positive = 0;
    false_negative = 0;

    p = Theta * np.transpose(X)
    for ii in range(shape(p)[0]):
        for jj in range(shape(p)[1]):
            if	round(p[ii,jj])==1 and R[ii,jj]==1:
                true_positive = true_positive + 1
            if round(p[ii,jj])==0 and R[ii,jj]==0:
                true_negative = true_negative + 1
            if round(p[ii,jj])==1 and R[ii,jj]==0:
                false_positive = false_positive + 1
            if round(p[ii,jj])==0 and R[ii,jj]==1:
                false_negative = false_negative + 1

    print(true_positive)
    precision[i] = true_positive/(true_positive+false_positive)
    recall[i] = true_positive/(true_positive+false_negative)
    correctness_0[i] = true_negative/(true_negative+false_negative)
    total_correctness[i] = (true_positive+true_negative)/size(R)

    print(precision[i])
    print(recall[i])
    print(correctness_0[i])
    print(total_correctness[i])

    F_score[i] = (2*precision*recall)/(precision+recall)
print(accum_cost)

plt.plot(reg,accum_cost)
plt.show
