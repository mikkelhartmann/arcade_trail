"""

"""

from flask import Flask
from flask import request, render_template

class LemmaTokenizer(object):
        def __init__(self):
            self.wnl = WordNetLemmatizer()
        def __call__(self, doc):
            return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('landingPage.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = [request.form['text']]
    genre_names = ['Action', 'Indie', 'Strategy', 'Early Access', 'Free to Play', 'Massively Multiplayer', 'RPG',
                'Adventure', 'Casual', 'Simulation', 'Racing', 'Sports', 'Audio Production', 'Utilities', 
                'Video Production', 'Education', 'Design & Illustration', 'Web Publishing', 'Photo Editing',
                'Software Training', 'Animation & Modeling', 'Puzzle', 'Platformer', 'Survival', 'Shooter', 
                'Horror', 'Sandbox', 'Music', 'Fighting', 'Hidden Objects', 'Accounting']
    model_collection = joblib.load('data/model_collection.pkl') 
    pred_list = []
    for idx, clf in enumerate(model_collection):
        pred = clf.predict_proba(text)
        pred_list.append(pred[:,1])
    sort_idx = sorted(range(len(pred_list)), key=lambda k: pred_list[k], reverse=True)
    my_list = ["{}: {}".format(pred_list[idx], genre_names[idx]) for idx in sort_idx]
    return render_template('recommendations.html', list=my_list)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=8080)
