# To run this go to
# cd Documents/ArcadeTrail
# export FLASK_APP=flaskrReccomender.py
# python -m flask run

from flask import Flask
from flask import request, render_template

app = Flask(__name__)

@app.route('/user_id/<int:user_id>')
def show_post(user_id):
    import ReccomenderSystem
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

    # Constructing R
    R = ReccomenderSystem.construct_R(votes,ownerships,num_users,num_games)

    # ------------------------------------------------------------------------------
    # Non-personalized reccomendations
    # Getting the reccomendations from the simple sorting
    # ------------------------------------------------------------------------------
    pop_recs = ReccomenderSystem.getMostPopularGames(votes,R,titles,user_names,user_id)

    # ------------------------------------------------------------------------------
    # Personalized reccomendations
    # Content Based Reccomendations
    # ------------------------------------------------------------------------------
    attrVec = ReccomenderSystem.construct_attrVec(genres,num_games,num_attributes)
    ContentBasedPredictions = ReccomenderSystem.construct_ContentBasedPredictions(attrVec,R)
    content_recs = ReccomenderSystem.getContentBasedPrecition(ContentBasedPredictions,titles,user_names,user_id)

    # ------------------------------------------------------------------------------
    # Personalized reccomendations
    # Running collaborative filtering
    # ------------------------------------------------------------------------------
    X = np.load('src/cli/X.npy')
    Theta = np.load('src/cli/Theta.npy')
    svd_recs= ReccomenderSystem.getting_reccomendations(R,Theta,X,titles,user_names,user_id)

    # ------------------------------------------------------------------------------
    # returning the template
    # ------------------------------------------------------------------------------
    return render_template('reccomendations.html',
        svd_recs=svd_recs, pop_recs=pop_recs, content_recs=content_recs, user_id=user_id)

@app.route('/')
def hello_world():
    import ReccomenderSystem
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

    assosiation_rules = ReccomenderSystem.get_assosiation_rules(0.08,0.55)
    return render_template('landingPage.html',
        assosiation_rules = assosiation_rules)


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=8080)
