# Vanderbilt - Big Data 2017 - Homework 4

In this homework assignment, you will:

    * Solve the word search interview problem.
    * Develop code to predict all stars.
    * Implement a nearest neighbor classifier and k-means clustering.
    * Implement a spam classifier.

## Environments

To load the environment run:

    source activate venv

You should see "(venv)" at the start of your terminal.

Install the following:
    
    conda install scikit-learn matplotlib

## Data

We will be using MLB data sets:

    ls -larth *.csv

    -rw-r--r-- 1 fabbrid vu_ldap 192K Apr  1 23:05 AllstarFull.csv
    -rw-r--r-- 1 fabbrid vu_ldap 5.9M Apr  1 23:05 Batting.csv

Digit data sets:

    hadoop fs -ls -h /data/cs4266/digits

    -rw-r--r--   3 fabbrid fabbrid     48.8 M 2017-04-04 23:02 /data/cs4266/digits/digit_test.csv
    -rw-r--r--   3 fabbrid fabbrid     73.2 M 2017-04-04 23:02 /data/cs4266/digits/digit_train.csv

Spam data:

    ls -larth SMSSpamCollection 

    -rw-r--r-- 1 fabbrid vu_ldap 463K Apr  5 16:53 SMSSpamCollection

## Source Code

Repositories will be created for each student. You should see yours at 

    https://github.com/vu-bigdata-2017/<GITHUB USERNAME>-homework-4

Clone the repository to your home directory on the cluster using:

    git clone https://github.com/vu-bigdata-2017/<GITHUB USERNAME>-homework-4.git

I may push updates to this homework assignment in the future. To setup an upstream repo, do the following:

    git remote add upstream https://github.com/vu-bigdata-2017/homework-4.git

To pull updates do the following:
    
    git fetch upstream
    git merge upstream/master

You will need to resolve conflicts if they occur. 


## Scikit Learn

You will be using scikit-learn for part of the assignment (http://scikit-learn.org/).

## Part 0 - Word Search

Given a start word and end word of the same length, and an operation that flips a character to another,
return the sequence of intermediate words between the start and end. Every intermediate word must be a valid english word
(use the provided english\_words dictionary). 
If no sequence exists, return None.

Note that string.ascii\_lowercase results 'a' through 'z'.

Do not implement any operator besides the character flip.

To run, use:

    python 0_words.py

Once coded, you should see solutions like:

    ['spot', 'soot', 'boot', 'bort', 'bore', 'bare', 'bark']
    ['bail', 'ball', 'bale', 'bate', 'fate']
    ['fat', 'pat', 'pit', 'pig']

Run tests with:

    nosetests 0_words.py

## Part 1 - All-Star Classifiers

I setup a system to load data from the batting and all star files. Your task is to construct the input matrix X and
output matrix Y using these data sets. Once X and Y are created, the system I setup will test three classifiers' ability
to predict all stars.
This task is not fancy; just load the data into a matrix.

Note 1: Do not use the first five columns from the batting file in prediction (SKIP\_COLUMNS).

Note 2: If a field is empty (== ''), set the value to 0.

To run the code, use:

    python 1_all_stars.py

Which should give AUCs for each classifier like:

      SGDClassifier [0.71756050954537132, 0.66269976324967483, 0.71314732544826431, 0.56729475167649956, 0.43387118447305567] 0.618914706879
      GaussianNB [0.77261737426914268, 0.83291179219280154, 0.82562509740687084, 0.81190869554921496, 0.79888288431175281] 0.808389168746
      RandomForestClassifier [0.8566500131475151, 0.87727940338257238, 0.88265020483666756, 0.89382155446771927, 0.88102715166614631] 0.8782856655

Notice how the random forest predicts all stars more accurately than logistic classifiers. 

To run the test case, do:

    nosetests 1_all_stars.py


## Part 2 - Digit Classification

Build a nearest neighbor classifier for hand written digits. The image data set can be found on hadoop:

Download the data set to your local directory:

    hadoop fs -get /data/cs4266/digits/digit_train.csv

You can find more about the data set at https://www.kaggle.com/c/digit-recognizer/data.

Implement the following functions: knn\_predict, k\_means, knn\_predict\_with\_means.

To run, use:

    python 2_knn.py

To test, use:

    nosetests 2_knn.py

## Part 3 - Spam Classification

Given the spam data set, build a spam / ham prediction model and implement the is\_spam function. 
You should evaluate your accuracy against the full file. We will test you model with a holdout set.

You can use whatever classifier you want, and construct whatever features you want. 

Do not hard code results.

To run, use:

    python 3_spam.py

To test, use:

    nosetests 3_spam.py

