import unittest
import src.index_data as id
import tests.load_data_test as ld

class test_search_engine(unittest.TestCase):

    def test_word_num_dict(self):

        # test OK pour majuscule, tiret, retour de ligne, stemming, mots vides, ponctuation
        # ne prend pas en compte les accents
        # retourne OK si 'expected' et 'word_num_dict' correspondent

        data_dict, name_num_dict, num_name_dict = ld.load_hiboudata_dict()
        stopwords = ld.load_stopwords_set()
        index_dict, word_num_dict, num_word_dict, info_doc_dict = id.create_index_dict(data_dict, stopwords)
        expected = 14
        self.assertEqual(word_num_dict["vernaculair"], expected, msg='Test failed')

    def test_num_word_dict(self):

        # test OK pour majuscule, tiret, retour de ligne, stemming, mots vides, ponctuations
        # ne prend pas en compte les accents
        # retourne OK si 'expected' et 'num_word_dict' correspondent

        data_dict, name_num_dict, num_name_dict = ld.load_hiboudata_dict()
        stopwords = ld.load_stopwords_set()
        index_dict, word_num_dict, num_word_dict, info_doc_dict = id.create_index_dict(data_dict, stopwords)
        expected = 'term'
        self.assertEqual(num_word_dict[1], expected, msg='Test failed')

if __name__ == '__main__':
    unittest.main()
