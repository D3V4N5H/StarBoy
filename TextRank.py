text='''
// Paste the lyrics from starboy.txt here
'''

from summa import summarizer
print(summarizer.summarize(text))

from summa import keywords
print(keywords.keywords(text))

// Alternatively, use the following code from a command line console:
// textrank -t starboy.csv
