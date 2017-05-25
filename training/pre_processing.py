""" This is the python implementation of the reccomender system i first developed"""
from numpy import *
import numpy as np
import operator
from os import listdir
import csv
import itertools

def reading_genres(path_to_data):
	f = open(path_to_data)
	numberOfLines = len(f.readlines())
	genres = zeros((numberOfLines,2))
	f = open(path_to_data)
	index = 0
	for line in f.readlines():
		line = line.strip()
		listFromLine = line.split(',')
		genres[index,:] = listFromLine[0:2]
		index += 1
	return genres

def reading_taglines(path_to_data):
	f = open(path_to_data)
	numberOfLines = len(f.readlines())
	taglines = []
	id = []
	f = open(path_to_data)
	for line in f.readlines():
		listFromLine = line.split(',')
		if len(listFromLine)==2:
			if len(listFromLine[1])>3:
				taglines.append(listFromLine[1])
				id.append(listFromLine[0])
	return id, taglines

def pre_process():
	genres = reading_genres('data/game_genres.csv')
	game_id, taglines = reading_taglines('data/game_tagline.csv')
	y_mat = np.zeros((len(game_id),32))
	X_mat = []
	kk = 0;
	for ii in range(0,len(game_id)):
		tagline_index = np.where(genres[:, 0]==int(game_id[ii]))
		if len(tagline_index[0])>0:
			X_mat.append(taglines[ii])
			for jj in range(0,len(tagline_index[0])):
				genre = int(genres[tagline_index[0][jj],1])
				y_mat[kk,genre-1] = 1
		else:
			X_mat.append(taglines[ii])
		kk = kk+1
	return(X_mat, y_mat)
