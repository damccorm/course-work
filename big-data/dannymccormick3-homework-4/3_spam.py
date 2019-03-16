

def load_data():
    f = open('SMSSpamCollection')
    lines = f.readlines()
    f.close()

    X = []
    Y = []
    for line in lines:
        lineArray = line.split(' ')
        if line[0] == 's':
            Y.append(1)
            lineArray[0]=lineArray[0][5:]
        else:
            Y.append(0)
            lineArray[0]=lineArray[0][4:]
        X.append(lineArray)
        pass
    return X, Y

#Naive Bayes Classifer
#Returns dictionary mapping words to probability of them being spam
def train_model(X, Y):
    #Get num of times a given word appears as spam vs not spam
    words = {}
    appearances = {}
    totalSpam = 0
    totalHam = 0
    i = 0
    while i < len(X):
        if Y[i] == 1:
            totalSpam += 1
        else:
            totalHam += 1
        for word in X[i]:
            if (word,Y[i]) in appearances:
                appearances[(word,Y[i])] += 1
            else:
                appearances[(word,Y[i])] = 1
            words[word] = 1
        i+=1
    model = {}
    for word in words:
        spamAppearances = 0
        hamAppearances = 0
        if (word, 1) in appearances:
            spamAppearances = appearances[(word,1)]
        if (word, 0) in appearances:
            hamAppearances = appearances[(word, 0)]
        WgivenS = float(spamAppearances)/float(totalSpam)
        WgivenH = float(hamAppearances)/float(totalHam)
        prob = (WgivenS)/(WgivenS + WgivenH)
        model[word] = prob
    return model


def is_spam(model, text):
    words = text.split()
    probsMult = 1
    inverseProbsMult = 1
    for word in words:
        if word in model:
            prob = model[word]
            if prob == 0:
                prob = 0.01
            probsMult = probsMult*prob
            inverseProbsMult = inverseProbsMult*(1-prob)
    totalProb = probsMult/(probsMult + inverseProbsMult)
    return totalProb > 0.5


def main():
    X, Y = load_data()
    model = train_model(X, Y)
    print is_spam(model, 'Just sleeping..and surfing')
    print is_spam(model, 'PRIVATE! Your 2003 Account Statement for shows 800 un-redeemed S.I.M. points. Call 08718738001 Identifier Code:')
    print is_spam(model, 'Sorry, Ill call later')


class TestClass:
    def setUp(self):
        X, Y = load_data()
        self.model = train_model(X, Y)

    def test_1(self):
        assert False == is_spam(self.model, 'Just sleeping..and surfing')

    def test_2(self):
        assert True == is_spam(self.model, 'PRIVATE! Your 2003 Account Statement for shows 800 un-redeemed S.I.M. points. Call 08718738001 Identifier Code:')

    def test_3(self):
        assert False == is_spam(self.model, 'Sorry, Ill call later')


if __name__ == '__main__':
    main()
