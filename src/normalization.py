from src import Const
import src.handle_data as hd


def accents_removal(word):
    """
    é->e
    è->e
    ã->e
    :param word: dirty word
    :return: clean word
    """
    word1 = word.replace("é", "e")
    word2 = word1.replace("è", "e")
    word3 = word2.replace("ã", "e")

    final_word = word3

    return final_word


def normalization(word, stopwords_set, stemmer=None):
    """
    - not in stopwords
    - length >= min_length
    - stem (if needed)
    - lower letters
    - accents removal
    :param word: dirty word
    :param stopwords_set:
    :param stemmer: if needed
    :return: clean word
    """
    min_length = 3
    if word not in stopwords_set and len(word) >= min_length:
        word_semiclean = accents_removal(word)
        if Const.STEMMER is True and stemmer:
            word_stem = stemmer.stemWord(word_semiclean)
        else:
            word_stem = word_semiclean

        word_stem_low = word_stem.lower()
        word_final = word_stem_low

        return word_final

    # No need to keep this word
    else:
        return None


if __name__ == '__main__':
    stopwords_set = hd.load_stopwords_set(path='../data/stopwords-fr.txt')
    words = "Jérusalem délégation de la Palestine"

    for word in words.split(" "):
        norm_word = normalization(word, stopwords_set)
        if norm_word:
            print(norm_word)
