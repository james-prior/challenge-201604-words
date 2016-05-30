# coding = utf-8
# __author__ = cwandrews

import re
from string import ascii_lowercase
from collections import Counter, OrderedDict
from os.path import exists, isfile
from itertools import islice

import matplotlib.pyplot as plt


# 230k+ words from the standard UNIX dict in a local text file
# ('/usr/share/dict/words')
ENGLISH_DICTIONARY_FILENAME = 'static/english_words.txt'


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

        special_characters_pattern = re.compile("[-\"\'|:;.?!,\(\)\d]+")

        return special_characters_pattern.sub('', text)

    def read_in_file(self, filepath, n=10):
        """
        Return sorted list of the #n# most common words and their
        counts in a tuple.
        """

        gutenberg_boilerplate_pattern = re.compile("\n{10}")

        with open(filepath) as f:
            raw_text = f.read()

        if ("GUTENBERG" in raw_text and
                gutenberg_boilerplate_pattern.search(raw_text)):
            text_body = gutenberg_boilerplate_pattern.split(raw_text)[1]
        else:
            text_body = raw_text

        return self._word_counter(
            self._sanitize(text_body), n, ENGLISH_DICTIONARY_FILENAME)

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


def frequency_plot(word_counts):
    """
    Graph frequency of passed counter objects
    (WordCounter, LetterCounter).
    """

    dict_counted = OrderedDict(word_counts[:30])

    plt.rcdefaults()
    plt.barh(range(len(dict_counted)), dict_counted.values(), align='center')
    plt.tick_params(labelsize='small', pad=2.5)
    plt.title('Word Frequency')
    plt.xlabel('Counts')
    plt.ylabel('Counted')
    plt.yticks(range(len(dict_counted)), dict_counted.keys(), fontsize=10)

    plt.show()
