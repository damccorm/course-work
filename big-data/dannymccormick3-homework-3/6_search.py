import happybase
import sys
import json
import operator

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN


'''
Get top-10 pages for given keyword search.

You must manage multiple keyword searches: [nfl], [air jordan]

You can get a row for a given keyword with: table.row(keyword)

Recall from part 5 that the data is JSON formatted like:
    data = {
        'title': title,
        'word': word,
        'tfidf': tfidf,
        'pr': pr
    }
Which can be loaded with json.loads(data)

Calculate a score per page with: tf-idf + W * page_rank

If there are multiple keywords, ADD the scores for each keyword.

Note that the every keyword must occur in a given page to be in the result.
If one of the keywords is not in a page, discard the page.
'''
def search(keywords):
    print 'Searching for %s' % keywords
    W = 4
    TOP_K = 10

    connection = happybase.Connection(MACHINE, table_prefix=VUID)
    table = connection.table(INDEX_TABLE)
    numAppearances = {}
    scores = {}
    for word in keywords:
        word_rows = table.row(word)
        for key in word_rows:
            data = json.loads(word_rows[key])
            if data['title'] in numAppearances:
                numAppearances[data['title']] += 1
                scores[data['title']] += (data['tfidf']+W*data['pr'])
            else:
                numAppearances[data['title']] = 1
                scores[data['title']] = (data['tfidf']+W*data['pr'])

    #Takes out any keys that don't appear for all keywords
    for key in numAppearances:
        if numAppearances[key] != len(keywords):
            del scores[key]

    #Sort scores into list
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))

    #List is currently in reverse order, tuples are backwards, this fixes that
    reverseList = sorted_scores[-10:]
    toBeReturned = []
    i = len(reverseList)-1
    while i >= 0:
        reverseTuple = reverseList[i]
        toBeReturned.append((reverseTuple[1],reverseTuple[0]))
        i-=1
    return toBeReturned

if __name__ == '__main__':
    keywords = sys.argv[1:]
    print search(keywords)
