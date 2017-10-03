import unittest
import core_functions.index_data as id
import tests.load_data_test as ld

class test_search_engine(unittest.TestCase):

    def test_index(self):

        # test OK pour majuscule, tiret, retour de ligne, saut de ligne, mots vides
        # ne prend pas en compte les accents et les ponctuations
        # retourne OK si 'expected' et 'index_dict' retournent
        # la même séquence (num_mot: {num_doc: [position])

        data_dict, name_num_dict, num_name_dict = ld.load_data_dict()
        stopwords = ld.load_stopwords_set()
        index_dict, word_num_dict, num_word_dict = \
        test = id.create_index_dict(data_dict, stopwords)
        expected = {0: {0: [1]}, 1: {0: [2, 7]}, 2: {0: [3]}, 3: {0: [4]}, 4: {0: [5]}, 5: {0: [6]}, 6: {0: [8]}}
        self.assertEqual(index_dict, expected, msg='Test failed')

if __name__ == '__main__':
    unittest.main()