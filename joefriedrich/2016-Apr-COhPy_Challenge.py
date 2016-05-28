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

from collections import defaultdict

VALID_ONE_LETTER_WORDS = ('A', 'a', 'I')

def get_user_input():
    return input(
        'Type the number of the Gutenberg publication you wish to see:  ')

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

def creating_a_dictionary(from_words_list):
    word_counts = defaultdict(int)
    for word in from_words_list:
        if len(word) > 1 or word in VALID_ONE_LETTER_WORDS:
            word_counts[word] += 1
    return word_counts

def organizing_data(from_dictionary):
    organized_words = []
    for entry in from_dictionary.items():
        organized_words.append(entry)

    return sorted(organized_words, key = lambda entry: entry[1], reverse = 1)

def main():
    print('Welcome to the Friedrich Gutenberg word-counter thingy.')
    book_number = get_user_input()

    print('\nGrabbing website data...')
    website = get_book_from_gutenberg_website(book_number)

    find_book = re.split(r'\*{3}[\s\w]*\*{3}', website.text)
    book = find_book[1]

    find_words = re.compile(r'[a-zA-Z]+')
    words = find_words.findall(book)

    print('Creating dictionary...')
    web_dictionary = creating_a_dictionary(words)

    print('Organizing data...')
    count_words = organizing_data(web_dictionary)

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
            if user_choice in web_dictionary:
                print(user_choice + ' => ' + str(web_dictionary[user_choice]))
            else:
                print('***The word does not appear in the text.***')
        else:
            user_choice = int(user_choice)
            if user_choice >= len(count_words):
                user_choice = len(count_words)
            for user_number in range(0, int(user_choice)):
                print(count_words[user_number])

if __name__ == '__main__':
    main()
