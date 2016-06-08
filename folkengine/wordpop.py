import collections
from itertools import takewhile

MAX_N_VOCABULARY_WORDS = 50000

TEXT_BOUNDARY = '***'


def strip_header(lines):
    pass_on = False
    for line in lines:
        if pass_on and line != '\n':
            yield line.strip()
        elif line.startswith(TEXT_BOUNDARY):
            pass_on = True


def strip_header(lines):
    for line in lines:
        if line.startswith(TEXT_BOUNDARY):
            yield from lines


def strip_footer(lines):
    return takewhile(
        lambda line: not line.startswith(TEXT_BOUNDARY),
        lines,
    )


def strip_header_and_footer(lines):
    return strip_footer(strip_header(lines))


def get_words_from_lines(lines):
    for line in lines:
        yield from line.lower().split()


def parse(f):
    return get_words_from_lines(strip_header_and_footer(f))


def build_dataset(words):
    # What's the - 1 in (MAX_N_VOCABULARY_WORDS) - 1 for?
    count = collections.Counter(words).most_common(MAX_N_VOCABULARY_WORDS - 1)
    return count
