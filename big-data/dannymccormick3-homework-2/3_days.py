from mrjob.job import MRJob

import json


'''
Count the tweets per day.

See http://mike.teczno.com/notes/streaming-data-from-twitter.html for parsing info.
Get the screen name by accessing tweet['user']['screen_name']
Look at tweet['created_at'] for datetime of creation. Just use the first word in the date to get the day.
'''


class DaysTweets(MRJob):
    def mapper(self, _, line):
        try:
            tweet = json.loads(line)
            created_at = tweet['created_at']
            yield(created_at.split(' ', 1)[0],1)
            pass
        except Exception as e:
            pass

    def reducer(self, key, counts):
        i = 0
        for count in counts:
            i = i+1
        yield (key,i)
        pass


def test_count():
    f = open('3_days.out')
    lines = f.readlines()
    f.close()

    for line in lines:
        if line[:-1] in ['"Fri"   522399', '"Fri"\t522399']:
            return
    assert False


if __name__ == '__main__':
    DaysTweets.run()
