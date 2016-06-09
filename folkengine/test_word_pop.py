import unittest
import wordpop as wp


class TestWordPop(unittest.TestCase):

    def test_wordpop(self):
        filename = 'test.txt'
        f = open(filename, 'r')
        words = wp.get_words_from_gutenberg_file(f)

        count = wp.build_dataset(words)

        print('Most common words', count[:10])
        self.assertEqual(count[0], ('the', 3))
        self.assertEqual(count[1], ('a', 2))
        self.assertEqual(count[2], ('quick', 1))


if __name__ == '__main__':
    unittest.main()
