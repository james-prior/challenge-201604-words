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

VALID_ONE_LETTER_WORDS = ('A', 'a', 'I')

def get_book_from_gutenberg_website(book_number):
    class Namespace:
        pass
    foo = Namespace()
    filename = 'efloehr/pg%s.txt' % book_number
    foo.text = open(filename).read()
    return foo

    return requests.get(
        'http://www.gutenberg.org/cache/epub/' + book_number +
        '/pg' + book_number + '.txt')

def count_words(words):
    return Counter(
        word for word in words
        if len(word) > 1 or word in VALID_ONE_LETTER_WORDS
    )

def main():
    print('Welcome to the Friedrich Gutenberg word-counter thingy.')
    book_number = input(
        'Type the number of the Gutenberg publication you wish to see:  ')

    print('\nGrabbing website data...')
    website = get_book_from_gutenberg_website(book_number)

    find_book = re.split(r'\*{3}[\s\w]*\*{3}', website.text)
    book = find_book[1]

    find_words = re.compile(r'[a-zA-Z]+')
    words = find_words.findall(book)

    print('Creating dictionary...')
    word_counts = count_words(words)

    while True:
        print('\nWhat would you like to see?')
        print('-Type a word to see how many times it appears.')
        print('-Type a number to see that number of top words.')
        print('-Type a super huge number to get all words.')
        user_choice = input('-Type q to quit:  ')
        print('')

        word_test = find_words.search(user_choice)

        if user_choice == 'q':
            break
        elif word_test != None:
            if user_choice in word_counts:
                print(user_choice + ' => ' + str(word_counts[user_choice]))
            else:
                print('***The word does not appear in the text.***')
        else:
            for item in word_counts.most_common(int(user_choice)):
                print(item)

if __name__ == '__main__':
    main()
