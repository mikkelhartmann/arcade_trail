
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
from keras.models import Sequential
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn import metrics
# -----------------------------------------------------------------------------------------------------
# Functions that are used to make plotting figures in the notebook easier
# -----------------------------------------------------------------------------------------------------
def make_prediction(X_test, model):
    y_score = model.predict_proba(X_test)
    if y_score.shape[1]<2:
        nn_pred = y_score
        y_score = np.zeros( (len(X_test), 2) )
        y_score[:, 0] = 1-nn_pred[:,0]
        y_score[:, 1] = nn_pred[:,0]
    return y_score

def add_legend_and_labels(ax0, ax1):
    # Setting up labels and axis for ax0
    ax0.set(xlabel='False positive rate', ylabel='recall (true positive rate)', title='ROC curve')
    ax0.legend(loc="lower right", fontsize='20')
    ticks_and_gridlines(ax0)

    # Setting up labels and axis for ax1
    ax1.set(xlabel='recall', ylabel='precision', title='precision-recall curve')
    ax1.legend(loc="lower left", fontsize='20')
    ticks_and_gridlines(ax1)

def create_color_cycle():
    color_cycle = cycler(color=['r', 'g', 'b', 'c', 'm', 'k', 'y'])
    marker_cycle = cycler(marker=['o', 's', 'v', 'x','*'])
    cycle = marker_cycle * color_cycle
    return cycle

def ticks_and_gridlines(ax):
    ax.set(xlim=[0.0, 1.0], ylim=[0.0, 1.0])
    ax.set(xticks=np.arange(0,1,0.05), yticks=np.arange(0,1,0.05))
    ax.grid(color='gray', linestyle='--', linewidth=.5, which='major');

def make_roc_pr_plot(X_test, y_test, model_collection, legend_names):
    cycle = create_color_cycle()

    fig, (ax0, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(28,14))

    # Initializing variables that will be updated in the loop
    aggregate_tpr = 0.0
    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)
    aggregate_roc_auc = 0
    aggregate_pr_auc = 0

    # Looping over the models
    for idx, (model, sty) in enumerate( zip(model_collection, cycle)):
        # Making the prediction
        y_score = make_prediction(X_test, model)        

        # Calculating false and true positive rate
        fpr, tpr, threshold = metrics.roc_curve(y_test[:, idx], y_score[:, 1])
        roc_auc = metrics.auc(fpr, tpr)
        aggregate_tpr += np.interp(mean_fpr, fpr, tpr)

        # Calculating precision and recall
        precision, recall, threshold = metrics.precision_recall_curve(y_test[:, idx], y_score[:, 1]);
        pr_auc = metrics.auc(recall, precision)
        aggregate_pr_auc += pr_auc 

        # Plotting the metrics
        ax0.plot(fpr, tpr, **sty, label='{0} ({1:.2f})'.format(legend_names[idx], roc_auc))
        ax1.plot(recall, precision, **sty, label='{0} ({1:.2f})'.format(legend_names[idx], pr_auc))

    # Plotting the average metrics
    mean_tpr = np.divide(aggregate_tpr, (idx+1))
    mean_roc_auc = metrics.auc(mean_fpr, mean_tpr)
    mean_pr_auc = aggregate_pr_auc/(idx+1)

    ax0.plot(mean_fpr, mean_tpr, lw=3, color='k', label='Average recall ({0:.2f})'.format(mean_roc_auc))
    ax1.plot(1,1, lw=3, color='k', label='Mean PR AUC ({0:.2f})'.format(mean_pr_auc))

    add_legend_and_labels(ax0, ax1)
    plt.show()

def plot_top_tags_barplot(y_label_names, aggregate, sort_idx, top_n):
    fig, ax = plt.subplots(figsize=(8, 10))
    
    ax.barh(range(len(y_label_names[:top_n])), aggregate[sort_idx[:top_n]])

    ax.set_ylim([-1, top_n + 1])
    ax.set_yticks(range(0, top_n))
    
    ax.set_yticklabels(y_label_names[:top_n]);
    ax.xaxis.set_label_position('top')
    ax.xaxis.tick_top()
    ax.set(xlabel='Number of games with tag');
    ax.invert_yaxis()
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.show()
