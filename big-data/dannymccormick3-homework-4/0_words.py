import itertools, string, Queue

def load_words():
    f = open('english_words.txt')
    lines = f.readlines()
    f.close()

    words = {}
    for word in lines:
        words[word.strip()] = 1
    return words


def path(english_words, start, end):
    # do something
    # you probably want to keep track of which words you have seen.
    alreadySeen = {}
    q = Queue.Queue()
    q.put([start])
    alreadySeen[start] = 1
    while not q.empty():
        curList = q.get()
        lastWord = curList[-1]
        for i, c in enumerate(lastWord):
            for x in range(97,123):
                lastWord = lastWord[:i]+chr(x)+lastWord[i+1:]
                if((lastWord in english_words) and (lastWord not in alreadySeen)):
                    if lastWord == end:
                        return (curList + [lastWord])
                    q.put(curList + [lastWord])
                    alreadySeen[lastWord] = 1
            lastWord = lastWord[:i]+c+lastWord[i+1:]
    return None


def main():
    english_words = load_words()
    print path(english_words, 'spot', 'bark')
    print path(english_words, 'bail', 'fate')
    print path(english_words, 'fat', 'pig')


def is_valid_path(english_words, path, src, dst):
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    assert path[0] == src
    assert path[-1] == dst

    for w1, w2 in pairwise(path):
        assert w1 in english_words
        assert len(w1) == len(w2)
        assert 1 == len([(a, b) for a, b in zip(w1, w2) if a != b])

    return True

def test_1():
    english_words = load_words()
    r = path(english_words, 'spot', 'bark')
    assert len(r) == 7
    assert is_valid_path(english_words, r, 'spot', 'bark')


def test_2():
    english_words = load_words()
    r = path(english_words, 'bail', 'fate')
    assert len(r) == 5
    assert is_valid_path(english_words, r, 'bail', 'fate')


def test_3():
    english_words = load_words()
    r = path(english_words, 'fat', 'pig')
    assert len(r) == 4
    assert is_valid_path(english_words, r, 'fat', 'pig')
    

if __name__ == '__main__':
    main()
