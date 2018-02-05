import gensim
import logging
import os
import pickle
import sys
from gensim.models.phrases import Phraser
from gensim.models import Phrases, Word2Vec

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
lang='fr'
mincount=50
#mincount=1
size=300
ngram_level=2
threshold=2
remove_accents=True

#on passe en argument le mot que l'on souhaite tester avec word2vec
word = sys.argv[1]

assert ngram_level in [0, 1, 2]

extra = ""
if remove_accents:
    extra = "_remove_accents"

#Chargement du modèle
if ngram_level > 0:
    phraser_file = 'phraser/phraser_web{}_mincount{}_t{}_level{{}}.bin'.format(lang, mincount, threshold)
word2vec_model_file = 'word2vec/word2vec_web{}_mincount{}_size{}{}_phrases.bin'.format(lang, mincount, size, extra)

model = Word2Vec.load(word2vec_model_file)


#Divers tests    
#test = model.wv.most_similar(positive=['Nicolas', 'Sarkozy'], negative=['Francois'])

test = model.wv.most_similar(positive=[word], negative=[], topn=100)

# print(model['fille'])


for t in test:
    print(t)
