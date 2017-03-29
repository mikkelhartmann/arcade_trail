"""This module runs matrix factorization on a specified matrix. To run it you need
to specifiy the matrix as well as the number of latent features you want to use in
the factorization."""
import numpy as np
import scipy.optimize

def cost_function(params, R, num_features, regularization):
	"""The funtion computes the cost given a speficied goal, R, parameters, and the
	number of features. The cost is used when optimizing the matrix factorization."""
    # Getting the number of users and games
	num_users = R.shape[0]
	num_games = R.shape[1]
	# Unrolling the parameters
	X = np.reshape(params[0:num_games*num_features], (num_games, num_features))
	Theta = np.reshape(params[num_games*num_features:], (num_users, num_features))
	# Calculating predictions
	prediction = np.dot(Theta,np.transpose(X))
	# Calculating the suqared difference
	difference = ( prediction - R )
	square_difference = np.multiply(difference,difference)
	square_difference_votes = np.multiply(square_difference,R)
	# Regularizing Theta
	theta_squared = np.multiply(Theta,Theta)
	theta_regularized = (regularization/2)*np.sum(theta_squared)
	# Regularizing X
	X_squared = np.multiply(X,X)
	X_regularized = (regularization/2)*np.sum(X_squared)
	# Computing th cost
	cost = 0.5* np.sum(square_difference_votes) + theta_regularized + X_regularized
	return cost

def cost_grad(params, R, num_features, regularization):
	"""The function computes the gradient of the cost function when the goasl, R,
	and parameters are specified. The gradient of the cost function is used when
	optimizing the matrix factorization."""
	# Getting the number of users and games
	num_users = R.shape[0]
	num_games = R.shape[1]
	# Unrolling the parameters
	X = np.reshape(params[0:num_games*num_features], (num_games, num_features))
	Theta = np.reshape(params[num_games*num_features:], (num_users, num_features))
	# Calculating the predictions
	prediction = np.dot(Theta,np.transpose(X))
	# Calculating the gradient of X
	difference = prediction - R
	voted = np.multiply(difference, R)
	X_grad = np.dot(np.transpose(voted), Theta) + regularization*X
	# Calculating the gradient of Theta
	Theta_grad = np.dot(voted, X) + regularization*Theta
	# Inrolling the parameters
	grad = np.append(X_grad, Theta_grad)
	return(grad)

def matrix_factorization(R, num_features, regularization):
	"""Factorizing the ratings matrix into a user matrix and a items matrix
	both with a specified number of hidden layers."""
	# Getting the number of users and games
	num_users = R.shape[0]
	num_games = R.shape[1]
	# Initializing the factorization matrices X and Theta
	X = np.random.randint(2, size=(num_games, num_features))
	Theta = np.random.randint(2, size=(num_users, num_features))
	# Rolling out the factorization matrices
	X_long = np.reshape(X, (X.size, 1))
	Theta_long = np.reshape(Theta, Theta.size, 1)
	# Reshaping the parameters
	initial_parameters = np.append(X_long, Theta_long)
	# Specifying the goal to uptimize against. 
	# doing the actual fitting
	params = scipy.optimize.fmin_cg(
	    f = cost_function,
	    x0 = initial_parameters,
	    fprime = cost_grad,
	    args = (R, num_features, regularization),
	    maxiter = 400,
		disp = 0,
		full_output = 0)
	# Rolling the fitted parameters back into X and Theta
	X = np.reshape(params[0:num_games*num_features], (num_games, num_features))
	Theta = np.reshape(params[num_games*num_features:], (num_users, num_features))
	return X, Theta