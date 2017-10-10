import libs.kea as kea
import Stemmer as pystemmer


def bm25_function(query, stopwords):
    """
    More info https://en.wikipedia.org/wiki/Okapi_BM25
    :param query:
    :param stopwords:
    :return:
    """

    # tokenizer, from Kea
    tokenizer = kea.tokenizer()

    # stemmer, from PyStemmer
    stemmer = pystemmer.Stemmer('french')

    query_list = []
    words_query = tokenizer.tokenize(query)

    for word in words_query:
        if word not in stopwords:
            wordstem = stemmer.stemWord(word)
            query_list.append(wordstem)

    # compute bm25 for each documents
    for keyword in query_list:
        # bm25 += bm25 # à finir
        pass

    return 1


if __name__ == '__main__':
    pass