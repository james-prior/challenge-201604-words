# coding = utf-8
# __author__ = cwandrews

import re
from string import ascii_lowercase
from collections import Counter

import matplotlib.pyplot as plt


# 230k+ words from the standard UNIX dict in a local text file
# ('/usr/share/dict/words')
ENGLISH_DICTIONARY_FILENAME = 'static/english_words.txt'
N_MAX_WORDS_TO_PLOT = 30


class WordCounter(Counter):
    """
    Read text from string or file, counts words, and returns sorted
    list of tuples with the n most common words and their respective
    counts.
    """

    key_name = 'word'

    @staticmethod
    def _sanitize(text):
        """
        Performs additional processing (sanitization) of text.

        Particularly, removes special characters.
        """

        gutenberg_boilerplate_pattern = re.compile("\n{10}")
        if ("GUTENBERG" in text and
                gutenberg_boilerplate_pattern.search(text)):
            text = gutenberg_boilerplate_pattern.split(text)[1]

        special_characters_pattern = re.compile("[-\"\'|:;.?!,\(\)\d]+")

        return special_characters_pattern.sub('', text)

    def _get_words_and_dictionary(self, text, dictionary_filename):
        words = text.lower().split()

        with open(dictionary_filename) as f:
            dictionary = set(f.read().lower().split())

        return words, dictionary

    def __init__(self, text, dictionary_filename=ENGLISH_DICTIONARY_FILENAME):
        '''
        Return a list of the n most common words and their counts from
        the most common to the least. If n is None, returns all words.
        Words with equal counts are ordered arbitrarily.

        Words are from text that are in dictionary in specified file.

        If n is None, all words will be returned.
        '''

        words, dictionary = self._get_words_and_dictionary(
            self._sanitize(text),
            dictionary_filename)

        # print('words', words[:10])
        # print('dictionary', dictionary)

        self.wrapped = Counter(word for word in words if word in dictionary)

    def most_common(self, *args, **kwargs):
        return self.wrapped.most_common(*args, **kwargs)

    def plot_frequency(self, n=N_MAX_WORDS_TO_PLOT):
        """
        Graph frequency of words
        passed as sequence of (word, count) tuples
        (such as returned by
        WordCounter.most_common() or LetterCounter.most_common()).
        """

        words, counts = zip(*self.wrapped.most_common(n))

        plt.rcdefaults()
        plt.barh(range(len(counts)), counts, align='center')
        plt.tick_params(labelsize='small', pad=2.5)
        plt.title('%s Counts' % self.key_name.capitalize())
        plt.xlabel('Counts')
        plt.ylabel('%ss' % self.key_name.capitalize())
        plt.yticks(range(len(words)), words, fontsize=10)

        plt.show()


class LetterCounter(WordCounter):
    """
    Read text from string or file, counts words, and returns sorted
    list of tuples with the n most common words and their respective
    counts.

    Each letter of the text is defined as a word.
    """

    key_name = 'letter'

    def _get_words_and_dictionary(self, text, dictionary_filename):
        words = list(text.lower())

        dictionary = set(ascii_lowercase)

        return words, dictionary
