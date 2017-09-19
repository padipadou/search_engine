# -*- coding: utf-8 -*-

import os
import time
import collections

def word_count_dict(filename):
    """
    Returns a word/count DICT for this filename.
    """

    word_count = {}
    input_file = open(filename, 'r')

    for line in input_file:
        words = line.split()
        for word in words:
            word = word.lower()
            if not word in word_count:
                word_count[word] = 1
            else:
                word_count[word] = word_count[word] + 1

    input_file.close()

    return word_count

def main():
    dir = 'data/lemonde-utf8'
    os.chdir('..')
    word_count = {}

    for filename in os.listdir(dir):
        word_count_update = word_count_dict('{}/{}'.format(dir, filename))

        #merge
        first = collections.Counter(word_count)
        second = collections.Counter(word_count_update)
        word_count = dict(first + second)

    word_count_list = sorted(word_count.items(), key=lambda t: t[1])
    print('{}'.format(word_count_list[-1::-21]).decode('string_escape'))

if __name__ == '__main__':
    time0 = time.time()

    main()
    duration = time.time() - time0

    print "Temps d'execution = {} seconde(s)\n".format(duration)
