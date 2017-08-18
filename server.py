import os
import numpy as np
from datetime import datetime
from flask import Flask
from flask import request, render_template, session
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from src import load_models, pre_process_for_nn, make_prediction_with_nn

#----------------------------------------------------------------------------------------
# Configuring the app
#----------------------------------------------------------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))

#----------------------------------------------------------------------------------------
# Defining classes
#----------------------------------------------------------------------------------------
class NameForm(FlaskForm):
    text = TextAreaField('Describe a game and we will suggest the tags to use.',
                         validators=[Required()])
    submit = SubmitField('Submit')

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    game_description = db.Column(db.Text)
    suggested_tags = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

#----------------------------------------------------------------------------------------
# Initializing models
#----------------------------------------------------------------------------------------
def initialize_models():
    tags = list(np.load('data/selected_tag_names.npy'))
    words = np.load('data/top_n_words_dict.npy').item()
    models = load_models( 2 ) #len(tags)
    input_vec = pre_process_for_nn('Making first prediction', words)
    _ = make_prediction_with_nn(input_vec, models, tags)
    return tags, words, models

tags, words, models = initialize_models()

#----------------------------------------------------------------------------------------
# VIEWS
#----------------------------------------------------------------------------------------
@app.route('/', methods=['POST', 'GET'])
def hello_world():
    text, pred_tags = None, []
    form = NameForm()
    if form.validate_on_submit():
        text = form.text.data
        input_vec = pre_process_for_nn(text, words)
        pred_tags = make_prediction_with_nn(input_vec, models, tags)
        db.session.add( Post(game_description=text, suggested_tags=str(pred_tags)) )
        print('text:', text)
        print('pred_tags:', pred_tags)
    return render_template('recommendations.html',form=form, text=text, list=pred_tags)

if __name__ == '__main__':
    manager.run()