from gensim.models import Word2Vec
import core_functions.load_data as ld
import os

# from nltk.corpus import brown, movie_reviews, treebank


# b = Word2Vec(brown.sents())
# mr = Word2Vec(movie_reviews.sents())
# t = Word2Vec(treebank.sents())

# print(b.most_similar('money', topn=5))
# print(brown.sents())

from nltk.corpus.reader.plaintext import PlaintextCorpusReader

corpusdir = 'data/lemonde-utf8/' # Directory of corpus.
# corpusdir = '/home/david/PycharmProjects/search_engine/data/lemonde-utf8/' # Directory of corpus.


newcorpus = PlaintextCorpusReader(corpusdir, '.*')


newcorpus_list=newcorpus.sents()
newcorpus_list_without_stopwords=[]

stopwords = ld.load_stopwords_set()
#print(stopwords)
for i in range(len(newcorpus_list)):
    newcorpus_list_without_stopwords.append([x.lower() for x in newcorpus_list[i] if x not in stopwords])


test = Word2Vec(newcorpus_list_without_stopwords)
# print(test.most_similar('délégations', topn=5)) #erreur, not in vocabulary
print(test.most_similar('palestinienne', topn=5)) #erreur, not in vocabulary
# print(test)
