#!/usr/local/anaconda3/bin/python3

import conll
import operator

SUB = "SS"
OBJ = "OO"

def get_pairs(corpus):
	counter = 0

	pairs = {}
	for sentence in corpus:
#		print(sentence)
		for idx, word in enumerate(sentence):
#			print (idx, word)
			if word['deprel'] == SUB:
				verb_key = int(word['head'])
				verb = sentence[verb_key]['form'].lower()
				subject = word['form'].lower()
				counter += 1
				pair = (subject, verb)
				if pair in pairs:
					pairs[pair] += 1
				else:
					pairs[pair] = 1
	
	pairs_sorted = sorted(pairs.items(), key=operator.itemgetter(1), reverse=True)

	print("# of pairs:", counter)
	print("Most frequent pairs:")
	for i, pair in enumerate(pairs_sorted):
		if i >= 5:
			break
		print(pair[1], pair[0])


def get_triples(corpus):
	print("asd")	

if __name__ == '__main__':
	column_names = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
	train_file = "./corpus/swedish_talbanken05_train.conll"
	train_corpus = conll.read_sentences(train_file)
	train_corpus = conll.split_rows(train_corpus, column_names)
	
	print(train_file, len(train_corpus))
	
	get_pairs(train_corpus)	
	exit(0)	

	for row in train_corpus:
		print(row)
		exit(0)

	
