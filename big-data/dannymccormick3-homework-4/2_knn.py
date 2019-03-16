from collections import defaultdict
import random
import sys
import numpy as np
from scipy import misc
from scipy.spatial.distance import cosine, euclidean
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score


def load_training(limit=None):
    f = open('digit_train.csv')
    lines = f.readlines()
    f.close()

    labels = []
    images = []

    i = 0
    for line in lines:
        if i == 0:
            i += 1
            continue
        elif limit and i > limit:
            break
        
        line = line.strip().split(',')
        labels.append(int(line[0]))
        images.append(np.array(map(int, line[1:])))
        i += 1

    return np.array(images), np.array(labels)


def run_knn_classifier(clf, X, Y):
    skf = StratifiedKFold(n_splits=5)
    accuracies = []

    for train, test in skf.split(X, Y):
        prediction = clf(X[train], Y[train], X[test])
        accuracies.append(calculate_accuracy(Y[test], prediction))
    return accuracies, np.mean(accuracies)


def calculate_accuracy(Y_test, Y_predict):
    assert len(Y_test) == len(Y_predict)

    correct = 0
    for i in range(0, len(Y_test)):
        if Y_test[i] == Y_predict[i]:
            correct += 1
    return float(correct) / len(Y_test)


''' always predict a digit is a zero '''
def knn_predict_zero(X_train, Y_train, X_test):
    return [0 for i in range(0, len(X_test))]


'''
Input: list of training digits as arrays, training digit number such as 0, 1, ... 9 (i.e., the label), and list of
digits to predict as arrays
Output: list of digit predictions
'''
def knn_predict(X_train, Y_train, X_test):
    # use cosine similarity to measure difference
    labels = []
    for image in X_test:
        nearestVal = 0
        minDist = sys.maxint
        i = 0
        while i < len(X_train):
            dist = cosine(X_train[i],image)
            if dist < minDist:
                minDist = dist
                nearestVal = Y_train[i]
            i += 1
        labels.append(nearestVal)
    
    return labels


'''
Input: list of training digits as arrays, and digit number (label)
Output: K-means of digits, and associated list of labels
'''
def k_means(X_train, Y_train):
    NUM_MEANS = 20
    means = []
    labels = []

    # 1. randomly choose NUM_MEANS digits from X_train as starting means
    initialMeans = random.sample(xrange(len(X_train)), NUM_MEANS)
    for val in initialMeans:
        means.append(X_train[val])

    # 2. while the difference between the last set of means - new means > 0.001
    sum_diff = sys.maxint
    loop_count = 0

    while sum_diff > 0.001 and loop_count < 50:
        # 3. assign images to means using cosine similarity, also track the Y label
        assignments = []
        i= 0
        while i < len(means):
            assignments.append([])
            i+=1

        for image in X_train:
            minDist = sys.maxint
            assignment = 0
            i = 0
            while i < len(means):
                dist = cosine(image, means[i])
                if dist < minDist:
                    minDist = dist
                    assignment = i
                i+=1
            assignments[assignment].append(image)

        # 4. update means based on the assingment
        newMeans = []
        for a in assignments:
            curMean = []
            i = 0
            if len(a) > 0:
                while i < len(a[0]):
                    curSum = 0
                    for image in a:
                        curSum += image[i]
                    curMean.append(curSum/len(a))
                    i+=1
            newMeans.append(curMean)


        # 5. calculate difference between the new means and old using cosine similarity
        i = 0
        sum_diff = 0
        while i < len(newMeans):
            sum_diff += cosine(newMeans[i], means[i])
            i+=1

        # 6. set the new means to the current means
        means = newMeans
        loop_count += 1

    # 7. assign Y labels to final means based on the digits that are most often assigned to a mean
    means_to_labels = {}

    j = 0
    while j < len(X_train):
        minDist = sys.maxint
        assignment = 0
        i = 0
        while i < len(means):
            dist = cosine(X_train[j], means[i])
            if dist < minDist:
                minDist = dist
                assignment = i
            i+=1
        if (i,Y_train[j]) in means_to_labels:
            means_to_labels[(assignment,Y_train[j])] += 1
        else:
            means_to_labels[(assignment,Y_train[j])] = 1
        j+=1

    i = 0
    while i < len(means):
        j = 0
        maxRepetitions = 0
        curLeader = 0
        while j < 10:
            numRepetitions = means_to_labels.get((i,j), 0)
            if numRepetitions > maxRepetitions:
                maxRepetitions = numRepetitions
                curLeader = j
            j+=1
        labels.append(curLeader)
        i+=1


    # 8. return the k-mean, and the Y label for each mean
    return means, labels


'''
Input: list of training digits as arrays, training digit number (label), and list of digits to predict
Output: list of digit predictions
'''
def knn_predict_with_means(X_train, Y_train, X_test):
    means, mean_labels = k_means(X_train, Y_train)

    # do NN search on means
    labels = []
    for image in X_test:
        i = 0
        minDist = sys.maxint
        val = 0
        while i < len(means):
            dist = cosine(means[i],image)
            if dist < minDist:
                minDist = dist
                val = mean_labels[i]
            i += 1
        labels.append(val)
    

    return labels


def main():
    print 'Loading...'
    X, Y = load_training(400)
    print 'Done Loading...'
    print 'Predict 0: ', run_knn_classifier(knn_predict_zero, X, Y)
    print 'Predict: ', run_knn_classifier(knn_predict, X, Y)
    print 'Predict with K-Means: ', run_knn_classifier(knn_predict_with_means, X, Y)


def test_1():
    X, Y = load_training(400)
    a1, m1 = run_knn_classifier(knn_predict_zero, X, Y)
    a2, m2 = run_knn_classifier(knn_predict, X, Y)
    assert m1 < m2


def test_2():
    X, Y = load_training(400)
    a1, m1 = run_knn_classifier(knn_predict_zero, X, Y)
    a2, m2 = run_knn_classifier(knn_predict_with_means, X, Y)
    assert m1 < m2


if __name__ == '__main__':
    main()
