from mrjob.job import MRJob

import json

'''
Count the number of tweets.
Parse tweets with json.loads -- note how the tweets are huge JSON blobs.
Ignore tweets that error on load.
'''


class CountTweets(MRJob):
    def mapper(self, _, line):
        try:
            # Parse with: tweet = json.loads(line)
            #### yield some output
            tweet = json.loads(line)
            yield ("lines",1)
            pass
        except:
            pass

    def reducer(self, _, counts):
        ### yield some output
        i = 0
        for count in counts:
            i = i+1
        yield ("lines",i)
        pass


def test_count():
    f = open('1_count.out')
    lines = f.readlines()
    f.close()

    assert lines[0][:-1] in ['"lines"\t3640407']


if __name__ == '__main__':
    CountTweets.run()
