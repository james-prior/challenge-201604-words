#!/usr/bin/env python
import requests
import zipfile
import os
import string
import collections
import re
import boto3
import json

def url_factory(id):
    try:
        is_single_digit = id <= 9
    except ValueError:
        raise Exception('BAD ID, PLEASE TRY AN INTEGER VALUE FOR ID...')

    if is_single_digit:
        directories = ['0']
    else:
        digits = list(str(id))
        directories = digits[:-1]
    directories.append(str(id))
    path = '/'.join(directories)
    url = "http://www.gutenberg.lib.md.us/%s/%s.zip" % (path, id)
    print(url)
    return url

def get_book_txt_zip(zip_url, local_zip_filename):
    resp = requests.get(zip_url, stream=True)
    with open(local_zip_filename, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def get_words(local_zip_filename, id):
    file_name = "%s.txt" % id
    zf = zipfile.ZipFile(local_zip_filename)
    text = zf.read(file_name).lower()
    # Remove punctuation.
    text = ''.join(c for c in text if c not in string.punctuation)
    words = text.replace('\r\n',' ').replace('\"','').split(' ')
    words = filter(None, words)  # Removes empty strings.
    return words

def test(results):
    """This function tests that words in result sets satisfy the
    definition in README.md

    >>> test('word')
    True
    >>> test('This-Word')
    if you got word problems I feel bad for you son. I got 99 problems, but " This-Word " aint one: Exception
    Traceback(most recent call last):
    File "/var/task/lambda_function.py", line 73, in lambda_handler
    test(sorted_count_word_tuples) File "/var/task/lambda_function.py", line 57, in test
    raise Exception(exception)
    Exception: if you got word problems I feel bad for you son. I got 99 problems, but " This-Word " aint one
    """

    for result_set in results:
        word = result_set[1]
        match_obj = re.match(r'\b[a-z]+\b', word)
        if not match_obj:
            exception = (
                "if you got word problems I feel bad for you son.  "
                "I got 99 problems, but \" %s \" aint one" % word
            )
            raise Exception(exception)
    return True

def upload_to_s3(id, word_counts):
    s3 = boto3.resource('s3')
    bucket = 'gutenberg-out'
    key = "%s.json" % id
    body = json.dumps(word_counts)
    s3.Object(bucket, key).put(Body=body)

def clean_up(local_zip_filename):
    os.remove(local_zip_filename)

def lambda_handler(event, context):
    id = event['id']
    local_zip_filename = "/tmp/%s.zip" % id
    print(id)
    print(local_zip_filename)
    
    zip_url = url_factory(id)
    get_book_txt_zip(zip_url, local_zip_filename)
    words = get_words(local_zip_filename, id)
    word_counts = collections.Counter(words)
    most_common_words = word_counts.most_common(10)
    test(most_common_words)
    upload_to_s3(id, word_counts)
    
    print(most_common_words)
    clean_up(local_zip_filename)
