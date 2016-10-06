# This is the python implementation of the reccomender system i first developed
# in MatLab
from numpy import *
import numpy as np
import operator
from os import listdir
import csv
import itertools
import apriori

# Defining the function that loads the votes and ownerships
def reading_votes(path_to_data):
	f = open(path_to_data)
	numberOfLines = len(f.readlines())
	votes = zeros((numberOfLines,2))
	f = open(path_to_data)
	index = 0
	for line in f.readlines():
		line = line.strip()
		listFromLine = line.split(',')
		votes[index,:] = listFromLine[0:2]
		index += 1
	num_games = int(max(votes[:,0]))
	num_users = int(max(votes[:,1]))
	return votes, num_games, num_users

# Defining the function that loads game titles
def reading_titles(path_to_data):
	f = open(path_to_data)
	numberOfLines = len(f.readlines())
	titles = []
	f = open(path_to_data)
	for line in f.readlines():
		line = line.replace('"','').strip().replace('\n','')
		listFromLine = line.split(',')
		if shape(listFromLine)[0] > 2:
			listFromLine_new = [[],[]]
			listFromLine_new[0] = listFromLine[0]
			flattened = list(itertools.chain.from_iterable(listFromLine[1:shape(listFromLine)[0]]))
			concatenated = ' '.join(flattened)
			listFromLine_new[1] = concatenated
			titles.append(listFromLine_new)
		else:
			titles.append(listFromLine)

	return [[d,t.decode("unicode-escape")] for [d,t] in titles]

# Constructing the R-matrix
def construct_R(votes,ownerships,num_users,num_games):
	R = zeros((num_users,num_games))
	for ii in range(0,len(votes)):
	    current_user = int(votes[ii,1])-1 #-1 because python starts at 0
	    current_game = int(votes[ii,0])-1
	    R[current_user,current_game] = 1
	# Filling up with user ownerships
	for ii in range(0,len(ownerships)):
	    current_user = int(ownerships[ii,1])-1
	    current_game = int(ownerships[ii,0])-1
	    R[current_user,current_game] = 1
	return R

# def consruct_assosiation_list(path_to_data):
# 	f = open(path_to_data)
# 	numberOfLines = len(f.readlines())
# 	votes = zeros((numberOfLines,2))
# 	f = open(path_to_data)
# 	index = 0
# 	for line in f.readlines():
# 		line = line.strip()
# 		listFromLine = line.split(',')
# 		votes[index,:] = listFromLine[0:2]
# 		index += 1
# 	num_games = int(max(votes[:,0]))
# 	num_users = int(max(votes[:,1]))
# 	return votes, num_games, num_users

# ------------------------------------------------------------------------------
# Functions relevant to coontent based reccomendations
# ------------------------------------------------------------------------------
# constructing the attribute vector for each game
def construct_attrVec(genres,num_games,num_attributes):
	attrVec = zeros((num_games,num_attributes))
	for ii in range(0,len(genres)):
		current_game = int(genres[ii,0])-1
		current_attribute = int(genres[ii,1])-1
		attrVec[current_game,current_attribute] = 1
	return attrVec

# Running the content based
def construct_ContentBasedPredictions(attrVec,R):
	# Normalize attrVec
	normAttrVec = zeros(shape(attrVec))
	for ii in range(0,len(attrVec)):
		attrCount = sum(attrVec[ii,:])
		if attrCount == 0:
			normAttrVec[ii,:] = attrVec[ii,:]
		else:
			normAttrVec[ii,:] = attrVec[ii,:]/attrCount
	# Calculating user preferences
	normUserPreference = np.dot(R, normAttrVec)
	# Calculating the prediction
	prediction = np.dot(normUserPreference, np.transpose(normAttrVec))
	return prediction

def getContentBasedPrecition(prediction,titles,user_names,user_id):
	user_index = user_id-1 # Fixing the indexing
	#to_remove = np.where(R[user_index,:]==1)
	#reccomendations[to_remove] = 0
	reccomendations = prediction[user_index,:]

	# sorting the list of reccomendations
	sortIndex = sorted(range(len(reccomendations)), key=lambda k: reccomendations[k],reverse=True)

	# finding the user name
	user_names = np.matrix(user_names)
	name_index = np.where(user_names[:,0]==str(user_id))
	name_index = int(name_index[0])
	name = user_names[name_index,1]

	titles = np.matrix(titles)

	reccomendation_list = []
	for i in range(0,10,1):
		title_index = np.where(titles[:,0]==str(sortIndex[i]+1))
		reccomendation_list.append(str(titles[title_index[0][0],1]))
	return reccomendation_list

# Defining the cost function
def cost_function(params, Y, R, num_users, num_games,num_features, regularization):
	X = np.reshape(params[0:num_games*num_features], (num_games, num_features))
	Theta = np.reshape(params[num_games*num_features:], (num_users, num_features))

	#prediction = X * np.transpose(Theta)
	prediction = np.dot(Theta,np.transpose(X))
	difference = ( prediction - Y )
	square_difference = np.multiply(difference,difference)
	square_difference_votes = np.multiply(square_difference,R)

	theta_squared = np.multiply(Theta,Theta)
	theta_regularized = (regularization/2)*sum(theta_squared)

	X_squared = np.multiply(X,X)
	X_regularized = (regularization/2)*sum(X_squared)

	cost = 0.5* sum(square_difference_votes) + theta_regularized + X_regularized
	return cost

# Defininf the gradient of the cost function
def cost_grad(params, Y, R, num_users, num_games,num_features, regularization):
	X = np.reshape(params[0:num_games*num_features], (num_games, num_features))
	Theta = np.reshape(params[num_games*num_features:], (num_users, num_features))

	# calculating X_grad
	prediction = np.dot(Theta,np.transpose(X))
	difference = prediction - Y
	voted = np.multiply(difference,R)
	X_grad = np.dot(np.transpose(voted),Theta) + regularization*X

	# calculating Theta_grad
	Theta_grad = np.dot(voted,X) + regularization*Theta

	# rolling paramaters out
	grad = np.append(X_grad,Theta_grad)
	return(grad)

# Running the collaberative filtering
def collaberative_filtering(num_games,num_users,num_features,R,regularization):
	import scipy.optimize
	import ReccomenderSystem
	X = np.random.randint(2,size=(num_games,num_features))
	Theta = np.random.randint(2,size=(num_users,num_features))

	X_long = np.reshape(X,(size(X),1))
	Theta_long = np.reshape(Theta,size(Theta),1)
	initial_parameters = np.append(X_long,Theta_long)

	Y = R

	# doing the actual fitting
	params = scipy.optimize.fmin_cg(
	    f = ReccomenderSystem.cost_function,
	    x0 = initial_parameters,
	    fprime = ReccomenderSystem.cost_grad,
	    args=(Y, R, num_users, num_games,num_features, regularization),
	    maxiter=400,
		disp = 0,
		full_output = 0)

	# Rolling the fitted parameters back into X and Theta
	X = np.reshape(params[0:num_games*num_features], (num_games, num_features))
	Theta = np.reshape(params[num_games*num_features:], (num_users, num_features))
	return X, Theta

# Getting to games
def getMostPopularGames(votes,R,titles,user_names,user_id):
	user_index = user_id-1 # Fixing the indexing
	# making a list of the most popular games
	num_games = int(max(votes[:,0]))
	games_votes = zeros(num_games)
	for i in range(0,shape(votes)[0]):
		current_game = int(votes[i,0])
		games_votes[current_game-1] += 1
	# removing from the list of reccomandations games the user allready likes
	to_remove = np.where(R[user_index,:]==1)

	games_votes[to_remove] = 0

	# sorting the list of reccomendations
	sortIndex = sorted(range(len(games_votes)), key=lambda k: games_votes[k],reverse=True)

	# finding the user name
	user_names = np.matrix(user_names)
	name_index = np.where(user_names[:,0]==str(user_id))
	name_index = int(name_index[0])
	name = user_names[name_index,1]

	titles = np.matrix(titles)

	# printing the top 10 reccomendations
	#print 'The top 10 reccomendations for %s' % name + ' (user_id %s' % str(user_index+1) +')'
	#for i in range(0,10,1):#range(10):
	#    title_index = np.where(titles[:,0]==str(sortIndex[i]+1))
	#    print(i+1, titles[title_index[0][0],1])

	reccomendation_list = []
	for i in range(0,10,1):
		title_index = np.where(titles[:,0]==str(sortIndex[i]+1))
		reccomendation_list.append(titles[title_index[0][0],1])

	return reccomendation_list

# Getting reccomendations
def getting_reccomendations(R,Theta,X,titles,user_names,user_id):
	user_index = user_id-1 # Fixing the indexing
	prediction = np.dot(Theta,np.transpose(X))
	reccomendations = prediction[user_index,:]
	# removing from the list of reccomandations games the user allready likes
	to_remove = np.where(R[user_index,:]==1)
	reccomendations[to_remove] = 0

	# sorting the list of reccomendations
	sortIndex = sorted(range(len(reccomendations)), key=lambda k: reccomendations[k],reverse=True)

	# finding the user name
	user_names = np.matrix(user_names)
	name_index = np.where(user_names[:,0]==str(user_id))
	name_index = int(name_index[0])
	name = user_names[name_index,1]

	titles = np.matrix(titles)

	reccomendation_list = []

	for i in range(0,10,1):
		title_index = np.where(titles[:,0]==str(sortIndex[i]+1))
		reccomendation_list.append(titles[title_index[0][0],1])
	return reccomendation_list

def title_index_to_title(titles,title_index):
	titles = np.matrix(titles)
	title_lookup = np.where( titles[:,0] == str(int(title_index)) )
	title = titles[title_lookup[0][0],1]
	return title

def get_assosiation_rules(minSupport,minConf):
	R = np.load('src/cli/R.npy')
	R = np.array(R.tolist())

	assosiationList = []
	for ii in range(0,len(R)):
	    assosiationList_temp = []
	    for jj in range(0,len(np.transpose(R))):
	        if R[ii,jj]==1:
	         assosiationList_temp.append(str(jj+1))

	    assosiationList.append(assosiationList_temp)

	# Removing the empty lists (user IDs deleted)
	for item in assosiationList:
	    if item == []:
	        assosiationList.remove(item)

	# Doing the assosiation analysis
	L,suppData = apriori.apriori(assosiationList,minSupport=minSupport)
	rules = apriori.generateRules(L[0:2],suppData,minConf=minConf)

	# Loading the titles
	titles = reading_titles('CSV/game_titles.csv')

	# Pritty printing the assosiation rules
	rule_string = []
	for rule in rules:
	    conf = round(rule[-1]*1000)/1000
	    temp_title = []
	    for frozen in rule[:-1]:
	        for item in frozen:
	            title = title_index_to_title(titles,str(item))
	        temp_title.append(title)
	    rule_string_temp = temp_title[0]+ ' implies '+ temp_title[1]+ ' with '+ str(conf) + ' confidence'
	    rule_string.append(rule_string_temp)
	return rule_string
