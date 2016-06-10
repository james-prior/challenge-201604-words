import collections

MAX_N_VOCABULARY_WORDS = 50000

TEXT_BOUNDARY = '***'


def read_lines(f):
    for line in f:
        yield line
    # Of course, f.readlines() or just iterating through r would have sufficed.
    # So this function can be omitted.


def strip_header(lines):
    pass_on = False
    for line in lines:
        if pass_on and line != '\n':
            yield line.strip()
        elif line.startswith(TEXT_BOUNDARY):
            pass_on = True


def strip_footer(lines):
    pass_on = True
    for line in lines:
        if pass_on:
            if line.startswith(TEXT_BOUNDARY):
                pass_on = False
            else:
                yield line.strip()  # This strip is superfluous.
    return stripped_lines


def strip_all(lines):
    return strip_footer(strip_header(lines))


def get_words_from_lines(lines):
    for line in lines:
        yield from line.lower().split()


def parse(f):
    return get_words_from_lines(strip_all(read_lines(f)))


def build_dataset(words):
    # What's the - 1 in (MAX_N_VOCABULARY_WORDS) - 1 for?
    count = collections.Counter(words).most_common(MAX_N_VOCABULARY_WORDS - 1)
    return count
