import os
import numpy as np
import time
import src as src
from flask import Flask
from flask import request, render_template, g
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    text = TextAreaField('Describe a game and we will suggest the tags to use.', validators=[Required()])
    submit = SubmitField('Submit')

@app.before_first_request
def load_huge_file():
    global model_collection
    global top_n_words_dict
    global selected_tag_names
    selected_tag_names = list(np.load('data/selected_tag_names.npy'))
    print('Loading the models')
    num_models = len(selected_tag_names)
    model_collection = src.load_models(1)
    print('Loading the dictionary mapping tag ids to tag names')
    top_n_words_dict = np.load('data/top_n_words_dict.npy').item()
    print('Making a prediction with the models to initiate them')
    zero_padded_example = src.pre_process_for_nn('Making first prediction', top_n_words_dict)
    _ = src.make_prediction_with_nn(zero_padded_example, model_collection, selected_tag_names)
    print('Everything is up and running...')

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    suggested_tags = []
    text = None
    form = NameForm()
    if form.validate_on_submit():
        text = form.text.data
        form.text.data = '' 
        zero_padded_example = src.pre_process_for_nn(text, top_n_words_dict)
        suggested_tags = src.make_prediction_with_nn(zero_padded_example, model_collection, selected_tag_names)
    return render_template('recommendations.html',form=form, text=text, list=suggested_tags)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=8080)