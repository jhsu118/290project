from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import re

WORD_RE = re.compile(r"[\w']+")

'''Finds unique words in the course descriptions.'''

class UniqueWordCount(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def extract_words(self, _, record):
        for i in record:
		    for word in WORD_RE.findall(record[i]['desc']):
		        yield [word.lower(), 1]

    def count_words(self, word, counts):
        yield [word, sum(counts)]

    def steps(self):
        return [self.mr(self.extract_words, self.count_words)]

if __name__ == '__main__':
    UniqueWordCount.run()
