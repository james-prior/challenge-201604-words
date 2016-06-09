import wordpop as wp


filename = 'pg84.txt'
f = open(filename,'r')
words = wp.get_words_from_gutenberg_file(f)

count = wp.build_dataset(words)

print('Most common words', count[:10])
