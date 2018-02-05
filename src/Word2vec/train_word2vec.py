import gensim
import logging
import os
from os.path import isfile
import pickle
from gensim.models.phrases import Phraser
from gensim.models import Phrases, Word2Vec
import unicodedata

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

lang = 'fr'

sentence_file = 'vraiall.txt'
workers = 25
mincount = 50
# mincount=1
size = 300
ngram_level = 2
threshold = 2
remove_accents = True
rebuild = False
build_word2vec = True

assert ngram_level in [0, 1, 2]

extra = ""
if remove_accents:
    extra = "_remove_accents"

if ngram_level > 0:
    phraser_output_file = 'phraser/phraser_web{}_mincount{}_t{}{}_level{{}}.bin'.format(lang, mincount, extra,
                                                                                        threshold)
word2vec_output_file = 'word2vec/word2vec_web{}_mincount{}_size{}{}_phrases.bin'.format(lang, mincount, size, extra)


# test = 0

class SentenceIterator(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        # i = 0
        for line in open(os.path.join(self.filename)):
            # if i < 100000000:
            line = line.rstrip()
            if remove_accents:
                line = unicodedata.normalize('NFD', line).encode('ascii', 'ignore').decode()

            sentence = line.lower().split(' ')
            # if ('new' in sentence and 'york' in sentence and 'times' in sentence):
            # print(sentence)
            # if i % 100 == 0:
            #     print('{} ({})'.format(i, test))
            # i = i + 1
            yield sentence
            # else:
            #     break


class PhraserIterator(object):
    def __init__(self, sentence_iterator, bigram_phraser, trigram_phraser):
        self.sentence_iterator = sentence_iterator
        self.bigram_phraser = bigram_phraser
        self.trigram_phraser = trigram_phraser

    def __iter__(self):
        if self.trigram_phraser is not None:
            for sentence in self.sentence_iterator:
                yield self.trigram_phraser[self.bigram_phraser[sentence]]
        elif self.bigram_phraser is not None:
            for sentence in self.sentence_iterator:
                yield self.bigram_phraser[sentence]
        else:
            for sentence in self.sentence_iterator:
                yield sentence


if __name__ == '__main__':

    sentences = SentenceIterator(sentence_file)  # a memory-friendly iterator

    ## Unigrams only
    if ngram_level == 0:
        # iterator = sentences
        bigram_phraser = None
        trigram_phraser = None
    ## Bigrams or trigrams
    elif ngram_level in [1, 2]:
        bigram_file = phraser_output_file.format(1)
        if isfile(bigram_file) and not rebuild:
            print('Loading existing bigram phraser from {}'.format(bigram_file))
            bigram_phraser = Phraser.load(bigram_file)
        else:
            print('Building bigram phraser')
            bigram_transformer = Phrases(sentences, min_count=mincount, threshold=threshold)
            bigram_phraser = Phraser(bigram_transformer)
            bigram_phraser.save(bigram_file)
        bigram_tokens = bigram_phraser[sentences]
        ## Bigrams only
        if ngram_level == 1:
            # iterator = bigram_tokens
            phraser = bigram_phraser
            trigram_phraser = None
        ## Trigrams
        elif ngram_level == 2:
            trigram_file = phraser_output_file.format(2)
            if isfile(trigram_file) and not rebuild:
                print('Loading existing trigram phraser from {}'.format(trigram_file))
                trigram_phraser = Phraser.load(trigram_file)
            else:
                print('Building trigram phraser')
                trigram_transformer = Phrases(bigram_tokens, min_count=mincount, threshold=threshold)
                trigram_phraser = Phraser(trigram_transformer)
                trigram_phraser.save(trigram_file)
                # iterator = trigram_phraser[bigram_phraser[sentences]]
    else:
        raise ValueError("")

    if build_word2vec:
        phraser_iterator = PhraserIterator(sentences, bigram_phraser, trigram_phraser)

        model = gensim.models.Word2Vec(phraser_iterator, min_count=mincount, size=size, workers=workers)
        model.save(word2vec_output_file)
