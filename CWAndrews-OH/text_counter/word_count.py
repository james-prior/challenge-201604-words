# coding = utf-8
# __author__ = cwandrews

import re
from collections import Counter, OrderedDict
from os.path import exists, isfile
from itertools import islice

import matplotlib.pyplot as plt


class WordCounter:
    """
    Read text from string or text file, counts words, and returns sorted
    list of tuples with the n most common words and their respective
    counts.
    """

    @staticmethod
    def _char_counter(
            genexp_text_sanitized,
            n,
            dictionary_filename='static/english_words.txt'):
        """
        Iterate through genexp provided by one of the read_in methods,
        counting all words passed and cross-checking results against the
        UNIX words file/dictionary and adding those that are to the
        output list until the list length meets passed n param or
        all English words if n=None. The list of valid English
        words is sorted in descending order before being returned.
        """

        # 230k+ words from the standard UNIX dict in a local text file
        # ('/usr/share/dict/words')
        # dictionary_filename = 'static/english_words.txt'

        with open(dictionary_filename) as f:
            dictionary = set([word.lower() for word in f.read().split()])

        count_words_master = Counter()

        for line_working in genexp_text_sanitized:
            count_words_master.update(Counter(line_working.split()))

        list_words_master = list()
        genexp_words_common_most = (
            word for word in count_words_master.most_common()
            if word[0] in dictionary)

        if n:
            for word in islice(genexp_words_common_most, n):
                list_words_master.append(word)
        else:
            for word in genexp_words_common_most:
                list_words_master.append(word)

        list_words_master.sort(
            key=lambda counter_obj: counter_obj[1], reverse=True)
        return list_words_master

    @staticmethod
    def _sanitize(list_strings):
        """
        Performs additional processing (sanitization) of text.
        Will strip white space from start and end of string, remove
        special characters, downcase all letters, replace any white
        space w/single space. Private method utilized by class methods.
        """

        white_space_re = re.compile("\s+")
        special_chars_re = re.compile("[-\"\'|:;.?!,\(\)\d]+")

        text_trimmed = (
            line_working.strip()
            for line_working in list_strings if line_working)
        text_no_extra_ws = (
            white_space_re.sub(' ', line_working)
            for line_working in text_trimmed)
        text_no_spec_chars = (
            special_chars_re.sub('', line_working)
            for line_working in text_no_extra_ws)
        text_sanitized = (
            line_working.lower()
            for line_working in text_no_spec_chars)

        for line_sanitized in text_sanitized:
            yield line_sanitized

    def read_in_file(self, filepath, n=10):
        """
        Return sorted list of the #n# most common words and their
        counts in a tuple.
        """

        assert exists(filepath) and isfile(filepath)

        with open(filepath, 'rt') as infile:

            gberg_split_re = re.compile("\n{10}")
            neline_working_re = re.compile("[\n\r]")

            read_text = infile.read()

            if ("GUTENBERG" in read_text) and gberg_split_re.search(read_text):
                working_text = gberg_split_re.split(read_text)[1]
            else:
                working_text = read_text

            if neline_working_re.search(working_text):
                chunked_text = neline_working_re.split(working_text)
            else:
                chunked_text = [working_text]

        return self._char_counter(self._sanitize(chunked_text), n)

    def read_in_string(self, string: str, n: int=10):
        """
        Return a sorted list of the #n# most common words and their
        counts in a tuple.
        """

        newline_working_re = re.compile("[\n\r]")

        if newline_working_re.search(string):
            chunked_text = newline_working_re.split(string)
        else:
            chunked_text = list(string)

        return self._char_counter(self._sanitize(chunked_text), n)


class LetterCounter(WordCounter):
    """
    Letter counter object which counts letters instead of words like
    it's parent class wherein the only difference is the _char_counter
    method which has been overidden.
    """

    @staticmethod
    def _char_counter(genexp_text_sanitized, n: int):
        """
        Overridden method from parent class, WordCounter,
        which counts letters instead of words.
        """

        english_ltrs = re.compile("[a-z]")

        master_ltr_count = Counter()

        for line_working in genexp_text_sanitized:
            ns_line_working = list(''.join(line_working))
            master_ltr_count.update(Counter(ns_line_working))

        master_ltr_list = list()
        common_ltrs_gen = (
            ltr
            for ltr in master_ltr_count.most_common()
            if english_ltrs.match(ltr[0]))

        if n:
            while len(master_ltr_list) < n:
                try:
                    master_ltr_list.append(next(common_ltrs_gen))
                except StopIteration:
                    break
        else:
            for ltr in common_ltrs_gen:
                master_ltr_list.append(ltr)

        master_ltr_list.sort(
            key=lambda counter_obj: counter_obj[1], reverse=True)
        return master_ltr_list


def frequency_plot(word_counter_obj):
    """
    Graph frequency of passed counter objects
    (WordCounter, LetterCounter).
    """

    if len(word_counter_obj) > 30:
        word_counter_obj = word_counter_obj[:30]

    dict_counted = OrderedDict()
    for wco in word_counter_obj:
        dict_counted[wco[0]] = wco[1]

    plt.rcdefaults()
    plt.barh(range(len(dict_counted)), dict_counted.values(), align='center')
    plt.tick_params(labelsize='small', pad=2.5)
    plt.title('Word Frequency')
    plt.xlabel('Counts')
    plt.ylabel('Counted')
    plt.yticks(range(len(dict_counted)), dict_counted.keys(), fontsize=10)

    plt.show()
