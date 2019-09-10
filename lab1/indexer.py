#!/usr/local/anaconda3/bin/python3

import sys
from os import walk
from os.path import join
import regex as re
import pickle
from math import log10
from math import sqrt
import numpy as np


f = []

for (dirpath, dirnames, filenames) in walk(sys.argv[1]):
	for filename in filenames:
		if filename.endswith(".txt"):
			f.append(filename)
	break


N = len(f)

results_dict = {}
word_counts = {}
for file in f:
	results_dict.update({file:{}})
	word_counts.update({file:0})

print (results_dict)
print (word_counts)


master_index = {}
for filename in f:
	path = join(sys.argv[1], filename)
	print (path)
	index = {}
	with open(path) as f:
		file_iterator = re.finditer(r'\p{L}+', f.read().lower())
		for match in file_iterator:
			word_counts[filename] += 1
			word = match.group()
			if word not in index:
				index[word] = [match.start()]
			else:
				index[word].append(match.start())
	pickle.dump(index, open(filename[:-4]+".idx", "wb"))
	for word in index.keys():
		if word not in master_index:
			master_index[word] = {filename:index[word]}
		else:
			master_index[word].update({filename:index[word]})

for word in master_index.keys():
#	print (word, master_index[word])
	nj = len(master_index[word])
#	print (nj)
	for filename in results_dict.keys():
		if filename in master_index[word]:
			tf = len(master_index[word][filename])
			results_dict[filename].update({word: ((tf/word_counts[filename]) * log10(N/nj))})
		else:
			results_dict[filename].update({word: 0.0})


for file in results_dict.keys():
	print (file)
	count = 0
	for word in results_dict[file].keys():
#		print (word)
		if word in  ("känna", "gås", "nils", "et"):
			print (word, results_dict[file][word])
#		if count < 10:
#			print (word, results_dict[file][word])	
#		count += 1
	print ()


#cosines = np.zeros((N,N))
cosines = 	[[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0]]
for i, filename1 in enumerate(results_dict.keys()):
	for j, filename2 in enumerate(results_dict.keys()):
		if filename1 == filename2:
			continue
		print(i, filename1, j, filename2)
		q = list(results_dict[filename1].values())
		d = list(results_dict[filename2].values())
		q2 = 0
		for qi in q:
			q2 += qi*qi
		q2 = sqrt(q2)
		d2 = 0
		for di in d:
			d2 += di*di
		d2 = sqrt(d2)
		for k, _ in enumerate(q):
			cosines[i][j] += q[k] * d[k]
		cosines[i][j] = cosines[i][j]/(q2*d2)
		print (cosines[i][j])

filenames = list(results_dict.keys()) 
print ("\t\t", filenames[0], "\t\t", filenames[1], "\t\t", filenames[2], "\t\t", filenames[3], "\t\t", filenames[4], "\t\t", filenames[5], "\t\t", filenames[6], "\t\t", filenames[7], "\t\t", filenames[8])
for i, row in enumerate(cosines):
	print (list(results_dict.keys())[i],"\t" , row[0],"\t" , row[1],"\t" , row[2],"\t" , row[3],"\t" , row[4],"\t" , row[5],"\t" , row[6],"\t" , row[7],"\t" , row[8])
