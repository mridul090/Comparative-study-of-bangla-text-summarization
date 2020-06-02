# -*- coding: utf-8 -*-
"""text_summarization_using_word2vec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15DPGRh0Nweyiq33-RpXcCoEFyhFAvQGp
"""

from google.colab import drive
drive.mount('/content/drive')

import re
from os.path import dirname, realpath
from flask import Blueprint, render_template, request, make_response, session, redirect, url_for
import operator
import math
import numpy as np
import gensim
from gensim.models import Word2Vec

class BengaliSentTok:
    def __init__(self, corpus):
        self._bangla_corpus = corpus

    def bn_corpus(self):
        bn_paragraphs = self._bangla_corpus

        return bn_paragraphs.strip('\n')

    def bn_stop_words(self, file_name='/content/drive/My Drive/Colab Notebooks/Text Summarization of my thesis/Bangla text summarization using word2vec/stop_words.txt'):
        # get the files path
#        file_dir_path = dirname(realpath(__file__))
#        file = file_dir_path + "/" + file_name
        file = file_name
        with open(file, 'r') as bn_stw:
            stop_words = "".join(bn_stw.readlines())

        return set(stop_words.split())

    def file_write(self, token_list, file_name):
        with open(file_name, 'w') as file:
            for index, token in enumerate(token_list):
                file.write(str(index + 1) + ') ' + token + '। \n')

    def bn_sentence_tok(self, pattern):
        corpus = self.bn_corpus()
        bn_tokens = re.split(pattern, corpus)

        return bn_tokens

    def bn_word_tok(self, pattern):
        word_tokens = []
        for tokenized_sent in self.bn_sentence_tok(pattern):
            word_list = tokenized_sent.split()
            word_tokens.append([word for word in word_list if word not in self.bn_stop_words()])

        return word_tokens

    def connecting_word(self, sentences):
        #cw_file = 'connecting_words.txt'
        # get the files path
       # file_dir_path = dirname(realpath(__file__))
       # file = file_dir_path + "/" + cw_file
        file = '/content/drive/My Drive/Colab Notebooks/Text Summarization of my thesis/Bangla text summarization using word2vec/connecting_words.txt'
        with open(file) as cw:
            connecting_words = cw.read()

        cw = 0
        for cword in connecting_words:
            if cword.strip() in sentences:
                cw += 1

        return cw

class word2vec:
  def __init__(self, corpus):
    self._tokenize_word = corpus
  def word_2_vec(self):
    model = Word2Vec(self._tokenize_word, min_count=1,size=1,workers=4,window=5)
    #model = gensim.Word2Vec(self._tokenize_word, size=150, window=10, min_count=2, workers=10, iter=10)
    return model

def document_summarizer(bangla_corpus):
    pattern = r'[?|।!]'
    bn_tok = BengaliSentTok(bangla_corpus)
    tokenized_sentences = bn_tok.bn_sentence_tok(pattern)
    tokenized_documents = bn_tok.bn_word_tok(pattern)
    corpora = ' '.join(bn_tok.bn_sentence_tok(pattern))
    pv_counter = 5
    sent_count = 0
    top_weighting_sentences = {}
    W2V = word2vec(tokenized_documents) 
    model = W2V.word_2_vec()
    for index, doc in enumerate(tokenized_documents):
        stf = 0
        if len(doc) > 0:
            for word in set(doc):
                vec = float(abs(model[word]))
                stf = round(stf + vec, 6)
            sentence = ' '.join(doc)
            pv_counter = round(pv_counter-0.01, 2)
            # pv_counter = 1 / (index + 1)
            # S=α*STF+β*PV+δ+λ
            alpha = 1
            beta = 1
            if pv_counter >= 3 and len(sentence.split()) >= 4:
                sent_count += 1
                cw = bn_tok.connecting_word(sentence)
                sent_score = round(alpha * stf + beta * pv_counter + cw, 6)
                # top_weighting_sentences[sentence] = sent_score
                top_weighting_sentences[tokenized_sentences[index]] = sent_score
                
    return top_weighting_sentences

response = {}
 
with open('/content/drive/My Drive/Colab Notebooks/Text Summarization of my thesis/Bangla text summarization using word2vec/dataset/Document_5.txt','r',encoding = 'utf-8') as f:
     document =  f.read()
    
if len(document) > 0:
    
    print(document)
    top_weighting_sentences = document_summarizer(document)
    summary_frequency = math.ceil(math.sqrt(len(top_weighting_sentences)))
    
    top_sentence = [
        sentence[0] for sentence in sorted(
            top_weighting_sentences.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:summary_frequency]]

    response["original_document"] = document
    response["summary_frequency"] = summary_frequency
    response["summery"] = '। '.join(top_sent.strip() for top_sent in top_sentence)
    
print('original_document',' ', response["original_document"])    
print('summary_frequency',' ',response["summary_frequency"]) 
#print('summery',' ', response["summery"]) 
print('summery')
for sent in response["summery"].split('। '):
    print(sent,'। ')
    

dac = np.zeros(2)
for sent in document.split('। '):
    dac[0] += 1
    
for sent in response["summery"].split('। '):
    dac[1] += 1
    

print('\n\n\n\n','Number of sentence in input text=',dac[0],'\n\n','Number of sentence in summary=',dac[1])

"""  Raff or Test """

bn_tok = BengaliSentTok(document)
pattern = r'[?|।!]'
tfidf_obj = TFIDF()

tokenized_sentences = bn_tok.bn_sentence_tok(pattern)
tokenized_documents = bn_tok.bn_word_tok(pattern)
corpora = ' '.join(bn_tok.bn_sentence_tok(pattern))

for index, doc in enumerate(tokenized_documents):
        stf = 0
        if len(doc) > 0:
            for word in set(doc):
                #print(tfidf_obj.tf(word, corpora))
                #stf = round(stf + tfidf_obj.tf(word, corpora), 6)

#print(tokenized_sentences)

#print(tokenized_documents)

#print(corpora)

bangla_corpus = document
pattern = r'[?|।!]'
bn_tok = BengaliSentTok(bangla_corpus)
tokenized_sentences = bn_tok.bn_sentence_tok(pattern)
tokenized_documents = bn_tok.bn_word_tok(pattern)
corpora = ' '.join(bn_tok.bn_sentence_tok(pattern))
pv_counter = 5
sent_count = 0
top_weighting_sentences = {}
""" train the model using word2vec """
W2V = word2vec(tokenized_documents) 
model = W2V.word_2_vec()
""" END train """
model['অনুভূতিতে']
stf = 0
vec =  model['অনুভূতিতে']
#vec = model.wv.most_similar('অনুভূতিতে')
print(vec)
#stf = round(stf + vec, 6)

vec = float(abs(model['অনুভূতিতে']))
#vec = model.wv.most_similar('অনুভূতিতে')

stf = round(stf + vec, 6)
print(stf)

vocab = list(model.wv.vocab)
for w in vocab:
  print(abs(model[w]))

