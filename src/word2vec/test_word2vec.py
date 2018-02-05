import logging
from gensim.models import Word2Vec


def word2vec_test(positive_word, negative_word=None):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    lang = 'fr'
    mincount = 50
    # mincount = 1
    size = 300
    ngram_level = 2
    threshold = 2
    remove_accents = True

    # on passe en argument le mot que l'on souhaite tester avec word2vec
    # word = sys.argv[1]
    word = positive_word

    assert ngram_level in [0, 1, 2]

    extra = ""
    if remove_accents:
        extra = "_remove_accents"

    # Chargement du modèle
    # root_path = ""
    root_path = "src/word2vec/"
    if ngram_level > 0:
        phraser_file = root_path + 'phraser/phraser_web{}_mincount{}_t{}_level{{}}.bin'.format(lang, mincount, threshold)
    word2vec_model_file = root_path + 'word2vec/word2vec_web{}_mincount{}_size{}{}_phrases.bin'.format(lang, mincount, size, extra)

    model = Word2Vec.load(word2vec_model_file)

    # Divers tests
    # test = model.wv.most_similar(positive=['Nicolas', 'Sarkozy'], negative=['Francois'])
    if not negative_word:
        test = model.wv.most_similar(positive=[word], negative=[], topn=100)
    else:
        test = model.wv.most_similar(positive=[word], negative=[negative_word], topn=100)

    return test


def word2vec_main(positive_word, negative_word=None):
    results = word2vec_test(positive_word)

    for result in results:
        print(result)


if __name__ == '__main__':
    word = "fille"

    word2vec_main(word)