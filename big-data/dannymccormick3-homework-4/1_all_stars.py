# conda install scikit-learn
import scipy
import numpy
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold


# player,year,stint,teamId,lgID,G,AB,R,H,2B,3B,HR,RBI,SB,CS,BB,SO,IBB,HBP,SH,SF,GIDP
def load_batting():
    f = open('Batting.csv', 'r')
    lines = f.readlines()
    f.close()

    batting = []
    for line in lines:
        line = line.strip()
        if line[0] == '#':
            continue
        batting.append(line.split(','))
    return batting


# playerID,yearID,gameNum,gameID,teamID,lgID,GP,startingPos
def load_allstars():
    f = open('AllstarFull.csv', 'r')
    lines = f.readlines()
    f.close()

    all_stars = {}
    for line in lines:
        line = line.strip().split(',')
        if line[0] == '#':
            continue
        player = line[0]
        year = line[1]
        all_stars[(player, year)] = 1

    return all_stars


def load():
    return load_batting(), load_allstars()


def create_input(batting):
    SKIP_COLUMNS = 5
    WIDTH = len(batting[0]) - SKIP_COLUMNS
    X = scipy.zeros((len(batting), WIDTH))

    # ignore player,year,stint,teamId,lgID in input matrix
    # do something
    yCor = 0
    while yCor < len(batting):
        xCor = 0
        while xCor < WIDTH:
            val = batting[yCor][xCor+SKIP_COLUMNS]
            if val == '':
                val = 0
            X[yCor][xCor] = float(val)
            xCor += 1
        yCor += 1

    return X


def create_output(batting, all_stars):
    Y = scipy.zeros(len(batting))

    # use batting fields to creat all star entries
    # do something
    # if in all stars = 1, else = 0
    i = 0
    while i < len(batting):
        line = batting[i]
        if (line[0],line[1]) in all_stars:
            Y[i] = 1
        i += 1
    return Y


def run_classifier(clf, X, Y):
    skf = StratifiedKFold(n_splits=5)
    aucs = []

    for train, test in skf.split(X, Y):
        clf.fit(X[train], Y[train])
        prediction = clf.predict_proba(X[test])
        aucs.append(roc_auc_score(Y[test], prediction[:, 1]))
    name, aucs, mean_auc = clf.__class__.__name__, aucs, numpy.mean(aucs)
    print name, aucs, mean_auc
    return name, aucs, mean_auc


def main():
    batting, all_stars = load()
    X = create_input(batting)
    Y = create_output(batting, all_stars)

    clf = linear_model.SGDClassifier(loss='log')
    run_classifier(clf, X, Y)

    clf = GaussianNB()
    run_classifier(clf, X, Y)

    clf = RandomForestClassifier(n_estimators=10, max_depth=10)
    run_classifier(clf, X, Y)


def test_1():
    batting, all_stars = load()
    X = create_input(batting)
    Y = create_output(batting, all_stars)

    clf = linear_model.SGDClassifier(loss='log')
    n1, a1, m1 = run_classifier(clf, X, Y)

    clf = GaussianNB()
    n2, a2, m2 = run_classifier(clf, X, Y)

    clf = RandomForestClassifier(n_estimators=10, max_depth=10)
    n3, a3, m3 = run_classifier(clf, X, Y)

    assert m1 < m2
    assert m2 < m3

if __name__ == '__main__':
    main()
