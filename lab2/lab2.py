#!/usr/local/anaconda3/bin/python3
import sys
import regex as re
import math

unigram_frequency = {}
bigram_frequency = {}
total = 0
unigram_probabilities = {}
bigram_probabilities = {}

def sentence_tokenizer(text):
    text = re.sub(r'[^\P{P}\.\?!]', "", text)
    text = re.sub(r'\n', "", text)
    text = re.sub(r'(\p{Lu}.*?)[\.\?!]', r'<s> \1 </s> ', text, flags=re.DOTALL)
#    text = re.sub(r'.*<s>', "<s>", text)
    return text.lower()

def analyze(text):
    text = sentence_tokenizer(text)
    global total

    #Unigrams
    words = text.split(' ')
    total = len(words)
    for word in words:
#      if word == "<s>" or word == "</s>":
#        print(word)

      if word in unigram_frequency.keys():
        unigram_frequency[word] += 1
      else:
        unigram_frequency[word] = 1
    for word in unigram_frequency.keys():
      unigram_probabilities[word] = unigram_frequency[word]/total

    #Bigrams
    bigrams = [tuple(words[inx:inx+2]) for inx in range(len(words) - 1)]
    for bigram in bigrams:
      if bigram in bigram_frequency.keys():
        bigram_frequency[bigram] += 1
      else:
        bigram_frequency[bigram] = 1
    for bigram in bigram_frequency.keys():
      bigram_probabilities[bigram] = bigram_frequency[bigram]/unigram_frequency[bigram[0]]

def preprocess_sentence(sentence):
    sentence = re.sub(r"\n", "", sentence)
    sentence = sentence.lower()
    sentence = re.sub(r'\p{P}', "", sentence)
    sentence += ' </s>'
#    print(sentence)	
    return sentence.split(' ')

def sentence_probability_unigram(sentence):
    words = preprocess_sentence(sentence)

    probability = 1
    entropy = 0
    print ("Unigram model")
    print ("="*54)
    print ("wi", "C(wi)", "#words", "P(wi)")
    print ("="*54)

    for word in words:
      print(
        word,
        str(unigram_frequency[word]),
        str(total),
        str(unigram_probabilities[word])
      )
      probability *= unigram_probabilities[word]
      entropy += math.log2(unigram_probabilities[word])

    print ("="*54)

    print ("Prob. unigrams:", probability)
    print ("Geometric mean prob.:", math.pow(probability, 1/len(words)))
    entropy = -1/len(words)*entropy
    print ("Entropy rate:", entropy)
    print ("Perplexity:", math.pow(2,entropy))
    print ()

def sentence_probability_bigram(sentence):
    words = preprocess_sentence("<s> " + sentence)
    bigrams = [tuple(words[inx:inx+2]) for inx in range(len(words)-1)]

    probability = 1
    entropy = 0

    print ("Bigram model")
    print ("="*54)
    print ("wi wi+1", "Ci,i+1", "C(i)", "P(wi+1|wi)", "backoff")
    print ("="*54)

    for bigram in bigrams:
      bigram_str = str(bigram[0]) + " " + str(bigram[1])  
      prob = 0
      freq = 0
      backoff = ""
      if bigram in bigram_probabilities:
        freq = bigram_frequency[bigram] 
        prob = bigram_probabilities[bigram]
      else:
        backoff = "backoff:" + bigram[1]
        prob = unigram_probabilities[bigram[1]]

      print(
        bigram_str,
        str(freq),
        str(unigram_frequency[bigram[0]]),
        str(prob),
        backoff
      )

      probability *= prob
      entropy += math.log2(prob)

    print("="*54)

    print("Prob. bigrams:", str(probability))
    print("Geometric mean prob.:", str(math.pow(probability, 1/len(words))))
    entropy = -1/len(bigrams)*entropy
    print("Entropy rate:", str(entropy))
    print("Perplexity:", math.pow(2, entropy))

if __name__ == '__main__':
    text = sys.stdin.read()
    analyze(text)

    sentence = "Det var en gång en katt som hette Nils"
    sentence2 = "Gorgo var bara tre åt gammal och hade ännu inte tänkt på att skaffa sig hustru och bli bofast, när han en dag blev fångad av en jägare och såld till Skansen."

    sentence_probability_unigram(sentence)
    sentence_probability_bigram(sentence)
