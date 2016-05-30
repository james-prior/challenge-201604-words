# coding = utf-8
# __author__ = cwandrews

import re
import pytest

from text_counter.word_count import LetterCounter
from text_counter.word_count import WordCounter


ENGLISH_DICTIONARY_FILENAME = 'static/english_words.txt'

MULTI_LINE_STRING = (
    'This is?\r my |file.\n'
    'It is alright\t 123 I suppose...\n'
    'This is !really! test.\nI hope it, works')
ONE_LINE_STRING = (
    'This is just another string but longer and with no newlines '
    'to test the read_in_string method. is is.')

FRANKENSTEIN_BOOK_FILENAME = 'static/pg84.txt'
ABRIDGED_FRANKENSTEIN_BOOK_FILENAME = 'static/pg84_super_abridged.txt'
MOON_BOOK_FILENAME = 'static/pg83.txt'
MULTI_LINE_FILENAME = 'static/test.txt'
ONE_LINE_FILENAME = 'static/one_line_test.txt'


@pytest.fixture("class")
def generator_words_good():
    return 'This is just for a test.. to see how well...'


@pytest.fixture("class")
def generator_words_dirty():
    return (
        'This is just| test.. dfadfskj see 123 ?!%G1 is ?!%G1 will dfadfskj')


@pytest.fixture("class")
def strings_list():
    return MULTI_LINE_STRING


@pytest.mark.usefixtures(
    "generator_words_good", "generator_words_dirty", "strings_list")
class TestWordCounter:
    def test_char_counter_io(self):
        counted_list = WordCounter(
            generator_words_good(),
            dictionary_filename=ENGLISH_DICTIONARY_FILENAME).most_common(5)
        counts_only = [obj[1] for obj in counted_list]

        assert WordCounter(
            generator_words_dirty(), ENGLISH_DICTIONARY_FILENAME
        ).most_common(5)

        assert isinstance(counted_list, list)

        for obj in counted_list:
            assert isinstance(obj, tuple)
            assert isinstance(obj[0], str)
            assert isinstance(obj[1], int)

        for i in range(len(counts_only) - 1):
            assert counts_only[i] >= counts_only[i + 1]

        assert WordCounter(
            generator_words_good(),
            dictionary_filename=ENGLISH_DICTIONARY_FILENAME
        ).most_common(5)

    def test_char_counter_returns_only_english_words(self):
        english_words = './static/english_words.txt'
        with open(english_words, 'rt') as eng_dict:
            english_dict = set([
                eng_word.lower().rstrip('\n')
                for eng_word in eng_dict.readlines()])

        clean_counted_list = WordCounter(
            generator_words_dirty(),
            dictionary_filename=ENGLISH_DICTIONARY_FILENAME
        ).most_common(3)
        words_only = [word[0] for word in clean_counted_list]

        for not_word in ('dfadfskj', '?!%G1'):
            assert not_word not in english_dict

        for word in words_only:
            assert word in english_dict

    def test_length_matches_returned_word_count(self):
        for n_words in (15, 35):
            assert len(WordCounter(
                open(FRANKENSTEIN_BOOK_FILENAME).read()).most_common(n_words)
            ) == n_words

    def test_return_all_if_length_gt_words_in_text(self):
        assert WordCounter(open(MULTI_LINE_FILENAME).read()).most_common(500)

    def test_length_none_returns_all_words(self):
        assert WordCounter(open(MULTI_LINE_FILENAME).read()).most_common(None)

    def test_sanitizer_io(self):
        for text in (strings_list(), ):
            assert WordCounter._sanitize(text)

    def test_sanitizer_sanitizes(self):
        spec_chars_re = re.compile("[\d?|!]")

        for text in (WordCounter._sanitize(strings_list()),):
            assert not spec_chars_re.findall(text)

    def test_read_in_file_io(self):
        gutenberg_re = re.compile("(ebook|electronic|computer)")

        for test_text in (MULTI_LINE_FILENAME, ONE_LINE_FILENAME):
            assert isinstance(
                WordCounter(open(test_text).read()).most_common(), list)

        for count_tuple in WordCounter(
                open(ABRIDGED_FRANKENSTEIN_BOOK_FILENAME).read()
                ).most_common(None):
            assert not gutenberg_re.findall(count_tuple[0])

    def test_read_in_file_any_gutenbook(self):
        for test_text in (FRANKENSTEIN_BOOK_FILENAME, MOON_BOOK_FILENAME):
            assert WordCounter(open(test_text).read()).most_common(5)

    def test_read_in_string_io(self):
        for text in (MULTI_LINE_STRING, ONE_LINE_STRING):
            assert isinstance(WordCounter(text).most_common(), list)


class TestLetterCounter:

    def test_char_counter_io(self):
        assert isinstance(
            LetterCounter(generator_words_good()).most_common(5), list)

    def test_letter_counter_io(self):
        assert LetterCounter(
            open(ABRIDGED_FRANKENSTEIN_BOOK_FILENAME).read()).most_common()
        assert isinstance(LetterCounter(
            open(ABRIDGED_FRANKENSTEIN_BOOK_FILENAME).read()).most_common(),
            list)

        assert LetterCounter(MULTI_LINE_STRING).most_common()
        assert isinstance(
            LetterCounter(MULTI_LINE_STRING).most_common(), list)

    def test_read_in_file_any_gutenbook(self):
        for test_text in (FRANKENSTEIN_BOOK_FILENAME, MOON_BOOK_FILENAME):
            assert LetterCounter(open(test_text).read()).most_common(5)

    def test_diff_n_letters(self):
        n_letters_tup = 1, 26

        for n_letters in n_letters_tup:
            letter_count = LetterCounter(
                open(FRANKENSTEIN_BOOK_FILENAME).read()).most_common(n_letters)
            assert len(letter_count) == n_letters

    def test_all_letters(self):
        assert LetterCounter(
            open(ABRIDGED_FRANKENSTEIN_BOOK_FILENAME).read()).most_common(None)

    def test_counts_letters_only(self):
        assert len(LetterCounter(
            open(FRANKENSTEIN_BOOK_FILENAME).read()
        ).most_common(27)) == 26
