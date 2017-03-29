"""This script loads the csv files crerated by running SQL on the Arcade Trail
database dump. The scripts defines the functions that construct the ratings matrix,
the game-genre matrix and the user-genre matrix. The matrices are used to make game
reccomendations based on matrix factorisation and content-based methods respectively """

# ------------------------------------------------------------------------------------------
# Importing the modules
# ------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matrix_factorization as mf


def loading_game_titles():
    """Loading the game titles. The csv file has a game ID and game title in each row."""
    # Loading the csv file
    game_titles = pd.read_csv('data/CSV/game_titles.csv', header = None)
    # Creating the dictionary relating game ID to game title
    game_ID_to_game_title = {}
    game_title_to_game_ID = {}
    for line in game_titles.values:
        game_ID = line[0]
        game_title = line[1]
        game_ID_to_game_title[game_ID] = game_title
    return(game_ID_to_game_title)

def loading_taglines():
    """Loading the game taglines. The csv file has a game ID and game tagline in each row."""
    # Loading the csv file
    game_taglines = pd.read_csv('data/CSV/game_tagline.csv', header = None)
    # Creating the dictionary relating game ID to game title
    game_ID_to_tagline = {}
    game_tagline_to_game_ID = {}
    for line in game_taglines.values:
        game_ID = line[0]
        game_tagline = line[1]
        game_ID_to_tagline[game_ID] = game_tagline
    return(game_ID_to_tagline)

# ------------------------------------------------------------------------------------------
# Defining the function for creating the ratings matrix as well as the dictionaries
# used to map from IDs to indices.
# ------------------------------------------------------------------------------------------
def loading_votes():
    """Loads the user votes and returns a matric with user votes. The matirx is a nx2
    matrix with n being the number of vores. The first column is user ID and the second
    is game ID"""
    votes = pd.read_csv('data/CSV/game_votes.csv', header = None)
    votes = np.matrix(votes)
    return votes

def make_ID_to_index_dictionaries(votes):
    """Makes the dictionaries that are used to map game and user ID to row and columns
    index in the ratins matrix. The dictionaries for the reverse mapping is also created"""
    # First a set of unique game IDs and user IDs is created
    user_ID = set()
    game_ID = set()
    for row in votes:
        currentUserID = row[0, 1]
        currentGameID = row[0, 0]
        user_ID.add(currentUserID)
        game_ID.add(currentGameID)
    # The dictionaries mapping ID to coloumn and row index are created
    user_ID_to_R_index = {}
    R_index_to_user_ID = {}
    # Looping through the user_ID set to create the dictionaries
    for (row_index, item) in enumerate(user_ID):
        user_ID_to_R_index[item] = row_index
        R_index_to_user_ID[row_index] = item
    # Looping through the game_ID set to create the dictionaries
    game_ID_to_R_index = {}
    R_index_to_game_ID = {}
    for (column_index, item) in enumerate(game_ID):
        game_ID_to_R_index[item] = column_index
        R_index_to_game_ID[column_index] = item
    return(user_ID_to_R_index, R_index_to_user_ID, game_ID_to_R_index, R_index_to_game_ID)

def make_ratings_matrix(votes, user_ID_to_R_index, game_ID_to_R_index):
    """Constructs the ratins matrix from the list of user votes and the dictionaries
    that map user and game ID to row and column index"""
    # Getting the number of users and games
    num_users = len(user_ID_to_R_index)
    num_games = len(game_ID_to_R_index)
    # Constructing the empty ratings matrix
    ratings_matrix = np.zeros((num_users, num_games))
    # Looping over the votes to fill inn the ratings matrix using the dictionaries to 
    # map from ID to matrix index
    for row in votes:
        user_ID = row[0, 1]
        game_ID = row[0, 0]
        row_index = user_ID_to_R_index[user_ID]
        column_index = game_ID_to_R_index[game_ID]
        ratings_matrix[row_index, column_index] = 1
    return(ratings_matrix)

# ------------------------------------------------------------------------------------------
# Defining the function for creating the game genre matrix and the user genre matrix as
# well as the dictionaries nescessary to map from IDs to indices.
# ------------------------------------------------------------------------------------------
def loading_genre_titles():
    """Loads the genre titles and creates a genre ID to genre title dictionary """
    # Loading the csv with genre ID, genre title
    genre_titles = pd.read_csv('data/CSV/genre_titles.csv', header = None)
    
    # Making dictionary from genre ID to genre title
    genre_ID_to_genre_title = {}
    genre_title_to_genre_ID = {}
    # Looping over the list with genre ID, genre titles
    for line in genre_titles.values:
        genre_ID = line[0]
        genre_title = line[1]
        genre_ID_to_genre_title[genre_ID] = genre_title
        genre_title_to_genre_ID[genre_title] = genre_ID
    return(genre_ID_to_genre_title, genre_title_to_genre_ID)

def loading_genres():
    """Loads the genres and makes the genre to index dictionary"""
    # Loading the data
    genres = pd.read_csv('data/CSV/game_genres.csv', header = None)
    genres = np.matrix(genres)
    return(genres)

def make_genre_ID_to_index_dict(genres):
    # Creates a set with game genre IDs
    genre_ID_set = set()
    game_ID_set = set()
    for row in genres: 
        genre_ID_set.add(row[0, 1])
    for row in genres:
        game_ID_set.add(row[0, 0])
    # Create a ditionary mapping genre ID to index in matrix
    genre_ID_to_index = {}
    index_to_genre_ID = {}
    for (index, genre_ID) in enumerate(genre_ID_set):
        genre_ID_to_index[genre_ID] = index
        index_to_genre_ID[index] = genre_ID
    game_ID_to_index = {}
    for (index, game_ID) in enumerate(game_ID_set):
        game_ID_to_index[game_ID] = index
    return(genre_ID_to_index, index_to_genre_ID, game_ID_to_index)

def make_game_genre_matrix(genres, game_ID_to_index, genre_ID_to_index):
    """Makes the game by genre matrix. Uses a different game ID to index dictionary than
    the one used for the ratings matrix, because this matrix cover more games."""
    num_games = len(game_ID_to_index)
    num_genres = len(genre_ID_to_index)
    game_genre_matrix = np.zeros((num_games, num_genres))
    # Looping over the genre data and fill in the game_genre_matrix
    for row in genres:
        current_game_ID = row[0, 0]
        current_genre_ID = row[0, 1]
        game_index = game_ID_to_index[current_game_ID]
        genre_index = genre_ID_to_index[current_genre_ID]
        game_genre_matrix[game_index, genre_index] = 1
    # Normalizing the game_genre_matrix
    return(game_genre_matrix)

def make_user_genre_matrix(R, user_ID_to_row_index_dict, game_ID_to_index_dict, column_index_to_game_ID_dict, game_genre_matrix):
    """Takes the game_genre_matrix and constructs the user genre matrix"""
    # Getting the number of users and genres
    numUsers = R.shape[0]
    numGenres = len(genre_ID_to_index)
    # Initializing the user_genre_matrix
    user_genre_matrix = np.zeros((numUsers, numGenres))
    # Looping over the users to summarize genre preference
    for (user_index, games) in enumerate(R):        
        # Initializing the genre vector for the current user
        genre_vector = np.zeros((1, numGenres))
        # Looping over the games for the current user
        for (game_index, game) in enumerate(games):
            if (game == 0):
                # The user does not have this game
                continue
            else:
                # Getting the game ID from the index in the rating matrix
                gameID = column_index_to_game_ID_dict[game_index]
                # Checking if the game ID has any genres.
                if gameID in game_ID_to_index_dict:
                    # Getting the game index in game_genre_matrix
                    index_in_game_genre_matrix =  game_ID_to_index_dict[gameID]
                    # Filling out the user_genre_matrix 
                    genre_vector = genre_vector + game_genre_matrix[index_in_game_genre_matrix, :]
                else:
                    # The game ID does not have any genres specified
                    continue
                # Adding the summed genre vector to the user genre matrix
        user_genre_matrix[user_index, :] = genre_vector
    return(user_genre_matrix)

# ------------------------------------------------------------------------------------------
# Defining the function that are use to aggregate the information and present it in a
# readable manner. These function are also ment to test the correctness of the ID to
# index mapping.
# ------------------------------------------------------------------------------------------
def get_game_info(game_ID, ratings_matrix, game_ID_to_R_index, game_genre_matrix, game_ID_to_index, index_to_genre_ID):
    """This function retrieves all relevant information about a game given the game id.
    The purpose of the function is to thest the different ID to index dictionaries as well
    as turning recommendations into human comprehensible information."""
    # Making the game ID to game title dictionary
    game_ID_to_game_title = loading_game_titles()
    # Getting the game title from the game ID
    game_title = game_ID_to_game_title[game_ID]
    print('Title: ' + game_title)
    # Making the game ID to game tagline dictionary
    game_ID_to_tagline = loading_taglines()
    # Getting the game tagline from the game ID
    game_tagline = game_ID_to_tagline[game_ID]
    print('Tagline: ' + game_tagline)
    # Making the genre ID to genre title dictionary
    genre_ID_to_genre_title, genre_title_to_genre_ID = loading_genre_titles()
    # Going from game ID to index in game genre matrix
    game_genre_index = game_ID_to_index[game_ID]
    # Selecting the game genre vector for the game
    genre_vector_for_game = game_genre_matrix[game_genre_index, :]
    # Initializing a list to keep all the genre titles for this game
    list_of_game_genres = []
    # Looping over the genres to ignore empty genres and look up the genre titles
    for (genre_index, has_genre) in enumerate(genre_vector_for_game):
        if has_genre == 0:
            continue
        # Going from column in game genre matrix to genre IDa
        genre_ID = index_to_genre_ID[genre_index]
        # Going from Genre ID to genre titles
        genre_title = genre_ID_to_genre_title[genre_ID]
        # Making a list of genre names for the game
        list_of_game_genres.append(genre_title)
    print('The game has the genres: ' + str(list_of_game_genres))
    # Calculating the number of votres
    game_index = game_ID_to_R_index[game_ID]
    num_votes = np.sum(ratings_matrix[:, game_index])
    print('It has: ' + str(num_votes) + ' votes')
    return(num_votes) #title, tagline, genres, 

# ------------------------------------------------------------------------------------------
# Testing the functions for constructing the ratings matrix
# ------------------------------------------------------------------------------------------
votes = loading_votes()
user_ID_to_R_index, R_index_to_user_ID, game_ID_to_R_index, R_index_to_game_ID = make_ID_to_index_dictionaries(votes)
ratings_matrix = make_ratings_matrix(votes, user_ID_to_R_index, game_ID_to_R_index)

# Testing the functions for constructing the use-genre and game-genre matrices
genres = loading_genres()
genre_ID_to_index, index_to_genre_ID, game_ID_to_index = make_genre_ID_to_index_dict(genres)
game_genre_matrix = make_game_genre_matrix(genres, game_ID_to_index, genre_ID_to_index)
user_genre_matrix = make_user_genre_matrix(ratings_matrix, user_ID_to_R_index, game_ID_to_index, R_index_to_game_ID, game_genre_matrix)

# Testing the matrix factorization
regularization = 100
num_features = 5
X, Theta = mf.matrix_factorization(ratings_matrix, num_features, regularization)

# Testing the get game info
loading_game_titles()
game_ID = R_index_to_game_ID[45]
num_votes = get_game_info(game_ID, ratings_matrix, game_ID_to_R_index, game_genre_matrix, game_ID_to_index, index_to_genre_ID)
