import ReccomenderSystem as RC
import scipy.sparse as sp
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.linear_model import SGDClassifier

#-------------------------------------------------------------------------------
#  Building my own word tokenizer to take care of stemming
#-------------------------------------------------------------------------------
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

#-------------------------------------------------------------------------------
#  Loading the data
#-------------------------------------------------------------------------------
titles = RC.reading_titles('../CSV/game_titles.csv')
genres, num_games, num_attributes = RC.reading_votes('../CSV/game_genres.csv')
id, taglines = RC.reading_taglines('../CSV/game_tagline.csv')

#-------------------------------------------------------------------------------
# Restructuring the data
#-------------------------------------------------------------------------------
y_mat = np.zeros((len(id),32))
X_mat = []
X_titles = []
kk = 0;
for ii in range(0,len(id)):
    tagline_index = np.where(genres[:,0]==int(id[ii]))
    #print('Tagline index is: ' + str(tagline_index) + ' and the length is: ' + str(len(tagline_index[0])))

    #temp_title = RC.title_index_to_title(titles,int(id[ii]))
    #X_titles.append(temp_title)
    if len(tagline_index[0])>0:
        X_mat.append(taglines[ii])
        #print('The length of the tagline index is: ' +  str(len(tagline_index)))
        for jj in range(0,len(tagline_index[0])):
            genre = int(genres[tagline_index[0][jj],1])
            #print('The genre is: ' + str(genre))
            y_mat[kk,genre-1] = 1
    else:
        X_mat.append(taglines[ii])
    #print(kk)
    #print(X_mat[kk])
    #print(y_mat[kk])
    kk = kk+1


print('The length of my genre vector is: ' + str(len(y_mat)))
print('The length of my tagline vector is: ' + str(len(X_mat)))

#-------------------------------------------------------------------------------
# Doing sanity check on the taglines and genres. Making sure they are correct
#-------------------------------------------------------------------------------
#print('Doing a sanity check on the data')
#print(X_titles[1])
#print(X_mat[1])
#print(y_mat[1])

#-------------------------------------------------------------------------------
# Setting the genre that defines the classifier
#-------------------------------------------------------------------------------
genre_to_train = 0;

#-------------------------------------------------------------------------------
# Creating the bag-of-words
#-------------------------------------------------------------------------------
train_size = int(round(len(y_mat)*0.8))

print('The training set size is: ' + str(train_size))
print('The number of positive cases in the training set is: ' + str(sum(y_mat[0:train_size,genre_to_train])))

y_train = y_mat[0:train_size,genre_to_train]
X_train = X_mat[0:train_size]

#-------------------------------------------------------------------------------
# Training the Naieve Bayes classifier
#-------------------------------------------------------------------------------
#clf = Pipeline([
#('vect', CountVectorizer(analyzer = 'word',stop_words = 'english')),
#('tfidf', TfidfTransformer(use_idf=True)),
#('clf', MultinomialNB())])

clf = Pipeline([
('vect', TfidfVectorizer(stop_words='english',smooth_idf=1,use_idf=1,analyzer='word')),
('tfidf', TfidfTransformer(norm='l2',use_idf=True,smooth_idf=True)),
('clf', MultinomialNB())
])
clf = clf.fit(X_train, y_train)

#-------------------------------------------------------------------------------
# Testing the calssifier
#-------------------------------------------------------------------------------
X_test = X_mat[train_size:-1];
y_test = y_mat[train_size:-1,genre_to_train];
predicted = clf.predict(X_test)

print('The number of positive cases in the test set is: ' + str(sum(y_test)))
print('The length of the test set is: ' + str(len(y_test)))
print('The number of predictions I make is: ' + str(len(predicted)))

print('The number of positive predictions is: ' + str(sum(predicted)))
#-------------------------------------------------------------------------------
# Calculating precision and recall
#-------------------------------------------------------------------------------
TP = 0.0
FP = 0.0
TN = 0.0
FN = 0.0

for ii in range(0,len(y_test)):
    if (predicted[ii] == 1)&(y_test[ii]==1):
        TP += 1
    if (predicted[ii] == 1)&(y_test[ii]==0):
        FP += 1
    if (predicted[ii] == 0)&(y_test[ii]==0):
        TN += 1
    if (predicted[ii] == 0)&(y_test[ii]==1):
        FN += 1

print('TP,FP,TN,FN:'+ str(TP)+' '+str(FP)+' '+str(TN)+' '+str(FN))

precision = TP/(TP+FP)
recall = TP/(TP+FN)

print('Precision: '+str(precision))
print('recall: '+str(recall))

#-------------------------------------------------------------------------------
# Giving the report using sklearn's metrics function
#-------------------------------------------------------------------------------
print(metrics.classification_report(y_test, predicted))

#-------------------------------------------------------------------------------
# Training the Support vector machine classifier
#-------------------------------------------------------------------------------
clf_SVD = Pipeline([
('vect', CountVectorizer(stop_words='english')),
('tfidf', TfidfTransformer()),
('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=10, random_state=42))
])
clf_SVD = clf_SVD.fit(X_train, y_train)
SVD_predicted = clf_SVD.predict(X_test)

TP = 0.0
FP = 0.0
TN = 0.0
FN = 0.0
for ii in range(0,len(y_test)):
    if (SVD_predicted[ii] == 1)&(y_test[ii]==1):
        TP = TP+1
    if (SVD_predicted[ii] == 1)&(y_test[ii]==0):
        FP = FP+1
    if (SVD_predicted[ii] == 0)&(y_test[ii]==0):
        TN = TN + 1
    if (SVD_predicted[ii] == 0)&(y_test[ii]==1):
        FN = FN + 1

print('TP,FP,TN,FN:'+ str(TP)+' '+str(FP)+' '+str(TN)+' '+str(FN))

precision = TP/(TP+FP)
recall = TP/(TP+FN)
print('Precision: '+str(precision))
print('recall: '+str(recall))

print(metrics.classification_report(y_test, SVD_predicted))
