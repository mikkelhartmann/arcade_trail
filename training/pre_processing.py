""" This is the python implementation of the reccomender system i first developed"""
from numpy import *
import numpy as np
import operator
from os import listdir
import csv
import itertools

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
	return titles

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
				#print(listFromLine[1])
				id.append(listFromLine[0])
	return id, taglines
