import wordpop as wp


filename = 'pg84.txt'
f = open(filename,'r')
words = wp.parse(f)

count = wp.build_dataset(words)

print('Most common words', count[:10])