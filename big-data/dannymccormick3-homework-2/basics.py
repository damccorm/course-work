'''
Input: a text string
Returns: a list of all permutations of the characters in the string (a list of strings)
Assume sorted string and unique values.
'''


def permute(text):
    return permuteHelper(text,"")

def permuteHelper(text,prevString):
    if len(text) == 0:
        return [prevString]
    l = []
    for i in range(len(text)):
        l = l+(permuteHelper(text[:i]+text[(i+1):],prevString + text[i]))
    return l



'''
Input: a text string and value (which will be a single character)
Output: the index of v in text, or -1 if v is not in text

Notes:  You cannot use string methods to do the index operation.
    You MUST write a binary search method
    Assume sorted string and unique values.
'''


def index_of(text, v):
    return index_of_helper(text,v,0,len(text)-1)

def index_of_helper(text, v, min, max):
    if(max < min):
        return -1
    mid = (min+max)/2
    if text[mid] == v:
        return mid
    elif text[mid] < v:
        return index_of_helper(text,v,mid+1,max)
    else:
        return index_of_helper(text,v,min,mid-1)


def test_permute1():
    result = permute('abcd')
    assert len(result) == 24
    assert 'adcb' in result
    assert 'badc' in result
    assert 'bacd' in result


def test_permute2():
    result = permute('abc')
    assert len(result) == 6
    assert 'acb' in result


def test_index_of1():
    assert index_of('abcde', 'a') == 0
    assert index_of('abcde', 'b') == 1
    assert index_of('abcde', 'c') == 2
    assert index_of('abcde', 'd') == 3
    assert index_of('abcde', 'e') == 4


def test_index_of2():
    assert index_of('abcde', 'z') == -1


if __name__ == '__main__':
    print permute('abcd')
