#Author:  Joe Friedrich
#COhPy Challenge 2016-Apr solution
#
#Word is anything that is not a number or symbol.
#Single letter contractions have been removed.
#Single letters that are not 'offical' words have been removed.
#Examples:  The name 'Ra's al Ghul' would appear as 'Ra' and 'al' and 'Ghul'
#The name Sadu-Hem would appear as 'Sadu' and 'Hem'.
#
#Crap!  I missed the testing part :(
#Ah, well... here is what I have.
#
#Bonuses:  1,2,4,5

import requests
import re

from collections import Counter

VALID_ONE_LETTER_WORDS = set(('A', 'a', 'I'))

def get_book_from_gutenberg_website(book_number):
    if True:  # Temporary hack to read file instead of website.
        class Namespace:
            pass
        foo = Namespace()
        filename = 'efloehr/pg%s.txt' % book_number
        foo.text = open(filename).read()
        return foo

    url = 'http://www.gutenberg.org/cache/epub/{0}/pg{0}.txt'.format(
        book_number)
    return requests.get(url)

def is_valid_word(word):
    return len(word) > 1 or word in VALID_ONE_LETTER_WORDS

def count_words(words):
    return Counter(
        word for word in words
        if is_valid_word(word)
    )

def main():
    print('Welcome to the Friedrich Gutenberg word-counter thingy.')
    book_number = input(
        'Type the number of the Gutenberg publication you wish to see:  ')

    print('\nGrabbing book from website.')
    web_page = get_book_from_gutenberg_website(book_number)

    book_pattern = (
        r'(?P<gutenberg_header>'
            r'^\*{2,} START OF THIS PROJECT GUTENBERG EBOOK.*\n)'
        r'(?P<body>(.*\n)*?)'
        r'(?P<gutenberg_tail>'
            r'^\*{2,} (END OF THIS PROJECT GUTENBERG EBOOK|Notes:).*\n)'
        # r'(?P<gutenberg_tail>^\*{2,} *Notes:)'
    )

    m = re.search(book_pattern, web_page.text, re.MULTILINE)
    book = m.group('body')

    word_pattern = re.compile(r'[a-zA-Z]+')
    words = word_pattern.findall(book)

    print('Counting words.')
    word_counts = count_words(words)

    while True:
        print()
        print('What would you like to see?')
        print('-Type a word to see how many times it appears.')
        print('-Type a number to see that number of top words.')
        print('-Type a super huge number to get all words.')
        user_choice = input('-Type q to quit:  ')
        if user_choice.lower() == 'q':
            break

        print()
        if word_pattern.search(user_choice):
            word = user_choice
            print(word, '=>', word_counts[word])
        else:
            n = int(user_choice)
            for item in word_counts.most_common(n):
                print(item)

if __name__ == '__main__':
    main()

'''TODO
Add docstrings to module and each function.
    Follow PEP 257.
    Avoid internal details; those go in comments.
Generalize to handle non-Project Gutenberg books.
    Allow to specify URL?
Allow user to specify file instead of URL.
Workaround PG request limits?
    Remove hack code of get_book_from_gutenberg_website().
'''
