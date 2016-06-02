# coding = utf-8
# __author__ = cwandrews

import re
from string import ascii_lowercase
from collections import Counter

import matplotlib.pyplot as plt


# 230k+ words from the standard UNIX dict in a local text file
# ('/usr/share/dict/words')
ENGLISH_DICTIONARY_FILENAME = 'static/english_words.txt'
N_MAX_ITEMS_TO_PLOT = 30


class WordCounter(Counter):
    '''
    Read text from string or file, counts words, and returns sorted
    list of tuples with the n most common words and their respective
    counts.

     (subclassed from Counter)

    Return a list of the n most common words and their counts from
    the most common to the least. If n is None, returns all words.
    Words with equal counts are ordered arbitrarily.

    If n is None, all words will be returned.
    '''

    key_name = 'word'

    @staticmethod
    def _sanitize(text):
        '''
        Returns text
            without "special characters" and
            without Project Gutenberg header and tail.
        '''

        gutenberg_boilerplate_pattern = re.compile("\n{10}")
        if ("GUTENBERG" in text and
                gutenberg_boilerplate_pattern.search(text)):
            text = gutenberg_boilerplate_pattern.split(text)[1]

        special_characters_pattern = re.compile("[-\"\'|:;.?!,\(\)\d]+")

        return special_characters_pattern.sub('', text)

    def _get_words_and_dictionary(self, text, dictionary_filename):
        '''Returns words and dictionary
        for given text and dictionary_filename.

        text is a (possibly large, multi-line) string.
        dictionary_filename is the name of a file which has one word per
        line.

        words is a list of the words
        from text converted to lowercase, delimited by whitespace.
        dictionary is a set of the words read from the
        dictionary_filename, converted to lowercase.
        '''

        words = text.lower().split()

        with open(dictionary_filename) as f:
            dictionary = set(f.read().lower().split())

        return words, dictionary

    def __init__(self, text, dictionary_filename=ENGLISH_DICTIONARY_FILENAME):
        '''
        Creates an object that counts words
        from the (possibly large, multi-line) text
        that are in the dictionary read from the
        dictionary_filename file.

        The dictionary file has one word per line.

        The default dictionary_filename is '%s'.
        ''' % (ENGLISH_DICTIONARY_FILENAME, )

        words, dictionary = self._get_words_and_dictionary(
            self._sanitize(text),
            dictionary_filename)

        # print('words', words[:10])
        # print('dictionary', dictionary)

        self.counter = Counter(word for word in words if word in dictionary)

    def most_common(self, *args, **kwargs):
        return self.counter.most_common(*args, **kwargs)

    def plot_counts(self, n=N_MAX_ITEMS_TO_PLOT):
        '''
        Graph counts of n most common words.

        n is optional and defaults to N_MAX_ITEMS_TO_PLOT.
        If n is None, counts of all words will be plotted.
        '''

        words, counts = zip(*self.counter.most_common(n))

        plt.rcdefaults()
        plt.barh(range(len(counts)), counts, align='center')
        plt.tick_params(labelsize='small', pad=2.5)
        plt.title('%s Counts' % self.key_name.capitalize())
        plt.xlabel('Counts')
        plt.ylabel('%ss' % self.key_name.capitalize())
        plt.yticks(range(len(words)), words, fontsize=10)

        plt.show()


class LetterCounter(WordCounter):
    '''
    Counts letters in given text.
    text is converted to lowercase before counting the letters.

    Subclass of WordCounter, so see WordCounter for inherited methods.
    '''

    key_name = 'letter'

    def _get_words_and_dictionary(self, text, dictionary_filename):
        '''Returns words and dictionary
        for given text and dictionary_filename.

        text is a (possibly large, multi-line) string.
        dictionary_filename is ignored.

        words is a list of the individual characters
        of text converted to lowercase.
        In other words, each character of text is defined to be a word.
        dictionary is a set of the lowercase letters of the English
        alphabet.
        '''

        words = list(text.lower())

        dictionary = set(ascii_lowercase)

        return words, dictionary
