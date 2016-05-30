# coding = utf-8
# __author__ = cwandrews

import re
from string import ascii_lowercase
from collections import Counter
from os.path import exists, isfile
from itertools import islice

import matplotlib.pyplot as plt


# 230k+ words from the standard UNIX dict in a local text file
# ('/usr/share/dict/words')
ENGLISH_DICTIONARY_FILENAME = 'static/english_words.txt'
N_MAX_WORDS_TO_PLOT = 30


class WordCounter:
    """
    Read text from string or file, counts words, and returns sorted
    list of tuples with the n most common words and their respective
    counts.
    """

    @staticmethod
    def _word_counter(text, n=None, dictionary_filename=None):
        '''
        Return a list of the n most common words and their counts from
        the most common to the least. If n is None, returns all words.
        Words with equal counts are ordered arbitrarily.

        Words are from text that are in dictionary in specified file.

        If n is None, all words will be returned.
        '''

        with open(dictionary_filename) as f:
            dictionary = set(f.read().lower().split())

        words = text.lower().split()
        word_counts = Counter(word for word in words if word in dictionary)

        return word_counts.most_common(n)

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

    def read_in_file(self, filepath, n=10):
        """
        Return sorted list of the #n# most common words and their
        counts in a tuple.
        """

        with open(filepath) as f:
            text = f.read()

        return self._word_counter(
            self._sanitize(text), n, ENGLISH_DICTIONARY_FILENAME)

    def read_in_string(self, text, n=10):
        """
        Return a sorted list of the #n# most common words and their
        counts in a tuple.
        """

        return self._word_counter(
            self._sanitize(text), n, ENGLISH_DICTIONARY_FILENAME)


class LetterCounter(WordCounter):
    """
    Read text from string or file, counts words, and returns sorted
    list of tuples with the n most common words and their respective
    counts.

    Each letter of the text is defined as a word.
    """

    @staticmethod
    def _word_counter(text, n=None, dictionary_filename=None):
        """
        Overridden method from parent class, WordCounter,
        which counts letters instead of words.
        """

        dictionary = set(ascii_lowercase)

        words = list(text.lower())
        word_counts = Counter(word for word in words if word in dictionary)

        return word_counts.most_common(n)


def plot_word_frequency(word_counts):
    """
    Graph frequency of words
    passed as sequence of (word, count) tuples
    (such as returned by
    WordCounter.most_common() or LetterCounter.most_common()).
    """

    words, counts = zip(*word_counts[:N_MAX_WORDS_TO_PLOT])

    plt.rcdefaults()
    plt.barh(range(len(counts)), counts, align='center')
    plt.tick_params(labelsize='small', pad=2.5)
    plt.title('Word Frequency')
    plt.xlabel('Counts')
    plt.ylabel('Words')
    plt.yticks(range(len(words)), words, fontsize=10)

    plt.show()
