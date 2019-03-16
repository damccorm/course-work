from mrjob.job import MRJob

import json

'''
Count the screen name with the most tweets and its counts.

See http://mike.teczno.com/notes/streaming-data-from-twitter.html for parsing info.
Get the screen name by accessing tweet['user']['screen_name']
'''


class GroupMaxTweets(MRJob):
    # The _ means the field does not matter.;
    def mapper(self, _, line):
        try:
            tweet = json.loads(line)
            # yield something
            yield (tweet['user']['screen_name'], 1)
            pass
        except:
            pass

    def reducer(self, key, counts):
        # yield something -- hint you can yield a tuple of values
        i = 0
        for count in counts:
            i = i+1
        tup = (key,i)
        yield("test",tup)
        pass

    def reducer_max(self, _, counts):
        # yield something
        max = 0
        name = ""
        for count in counts:
            if count[1] > max:
                max = count[1]
                name = count[0]
        yield (max,name)
        pass

    def steps(self):
        return [
            self.mr(mapper=self.mapper, reducer=self.reducer),
            self.mr(reducer=self.reducer_max)
        ]


def test_count():
    f = open('2_group.out')
    lines = f.readlines()
    f.close()

    assert lines[0][:-1] in ['31890   "Jayy_LaVey"', '31890\t"Jayy_LaVey"']


if __name__ == '__main__':
    GroupMaxTweets.run()
