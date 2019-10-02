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
		for word in sentence:
			if "-" in word['id']:
				continue
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
	counter = 0
	
	triples = {}
	for sentence in corpus:
		for word in sentence:
			if "-" in word['id']:
				continue
				break
			if word['deprel'] == SUB:
				verb_key = word['head']
				for word2 in sentence:
					if "-" in word2['id']:
						continue
					if word2['deprel'] == OBJ and word2['head'] == verb_key:
						counter += 1
						subject = word['form'].lower()
						verb = sentence[int(verb_key)]['form'].lower()
						obj = word2['form'].lower()
						triple = (subject, verb, obj)
						if triple in triples:
							triples[triple] += 1
						else:
							triples[triple] = 1
	triples_sorted = sorted(triples.items(), key=operator.itemgetter(1), reverse=True)
	
	print("# of pairs:", counter)
	print("Morst frequent triples:")
	for i, triple in enumerate(triples_sorted):
		if i >= 5:
			break
		print(triple[1], triple[0])
						
if __name__ == '__main__':
	column_names = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
	train_file = "./corpus/swedish_talbanken05_train.conll"
	train_corpus = conll.read_sentences(train_file)
	train_corpus = conll.split_rows(train_corpus, column_names)
	
	print(train_file, len(train_corpus))
	get_pairs(train_corpus)	
	get_triples(train_corpus)



	column_names = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']
	SUB = 'nsubj'
	OBJ = 'obj'

	files = conll.get_files("/usr/local/cs/EDAN20/ud-treebanks-v2.4/", "train.conllu")
	for file in files:
		train_corpus = conll.read_sentences(file)
		train_corpus = conll.split_rows(train_corpus, column_names)
		print(file, len(train_corpus))
		get_pairs(train_corpus)
		get_triples(train_corpus)
#		for sentence in train_corpus:
#			for idx, word in enumerate(sentence):
#				if idx >= 5:
#					break
#				print(idx, word)
