# Vanderbilt - Big Data 2017 - Homework 2

In this homework assignment, you will do the following:

    * Write some core algorithmic functions
    * Write map reduce programs to analyze Twitter data and Finance data
    * Write Pig programs to analyze MLB data

## Environments

To load the environment run:

    source activate venv

You should see "(venv)" at the start of your terminal.

Install the following:
    
    pip install mrjob beautifulsoup4 happybase

Set the path to hadoop in ~/.bashrc:

    export HADOOP_HOME=/opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/

Note you will need to `source ~/.bashrc` the first time after making the change. 

## Data

We will be using three data sets:

    hadoop fs -ls /data/cs4266
    
    drwxr-xr-x   - fabbrid hadoop          0 2016-02-13 00:26 /data/cs4266/baseball
    drwxr-xr-x   - fabbrid hadoop          0 2016-02-13 00:26 /data/cs4266/finance
    drwxr-xr-x   - fabbrid hadoop          0 2016-02-13 00:49 /data/cs4266/tweets

## Source Code

Repositories will be created for each student. You should see yours at 

    https://github.com/vu-bigdata-2017/<GITHUB USERNAME>-homework-2

Clone the repository to your home directory on the cluster using:

    git clone https://github.com/vu-bigdata-2017/<GITHUB USERNAME>-homework-2.git

I may push updates to this homework assignment in the future. To setup an upstream repo, do the following:

    git remote add upstream git@github.com:vu-bigdata-2017/homework-2.git

To pull updates do the following:
    
    git fetch upstream
    git merge upstream/master

You will need to resolve conflicts if they occur. 


## Part 1 - The Basics

Write a permute function and index of function. You can evaluate test cases with:

    nosetests basics.py

## Part 2 - Map Reduce

Analyze tweets from Nashville.

    hadoop fs -ls /data/cs4266/tweets

    -rwxr-xr-x   3 hdfs supergroup  203538004 2016-12-20 12:25 /data/cs4266/tweets/nashville-tweets-2015-08-24
    -rwxr-xr-x   3 hdfs supergroup  145423948 2016-12-20 12:25 /data/cs4266/tweets/nashville-tweets-2015-08-31
    ...

Write map reduce functions as specified in the following files. To test each MR job, we will read in an output file.


### 2.1

Count the number of tweets in the data set by updating the map and reduce functions in 1\_count.py.

You can start by testing your code on a small sample, without having to deal with Hadoop's setup. To start, you will need a local copy of a tweets file:

    hadoop fs -get /data/cs4266/tweets/nashville-tweets-2015-08-24 .

You can then run the map reduce job locally with:

    python 1_count.py nashville-tweets-2015-08-24

To run against all tweets and store the result in an output file, do the following:

    python 1_count.py -r hadoop hdfs:///data/cs4266/tweets/nashville-tweets-* > 1_count.out

Alteratively, you could run on a single file:

    python 1_count.py -r hadoop hdfs:///data/cs4266/tweets/nashville-tweets-2015-08-24

To evaluate if your result is correct, run the test case:

    nosetests 1_count.py


### 2.2
You can run the second task 2\_group.py with:

    python 2_group.py -r hadoop hdfs:///data/cs4266/tweets/nashville-tweets-* > 2_group.out


### 2.3
Run the third task with:

    python 3_days.py -r hadoop hdfs:///data/cs4266/tweets/nashville-tweets-* > 3_days.out


### 2.4
For the fourth task, implement the pig code as described in 4\_stock\_join.py.
Note you can run the associated pig program with:

    pig pig_scripts/stock_join.pig

To run the task, use:

    python 4_stock_join.py -r hadoop hdfs:///data/cs4266/finance/NYSE_daily_prices_A.csv hdfs:///data/cs4266/finance/NYSE_dividends_A.csv > 4_stock_join.out

## Part 3 - Pig

Analyze the MLB stats from http://seanlahman.com/files/database/readme2014.txt

    hadoop fs -ls -h /data/cs4266/baseball/Fielding.csv /data/cs4266/baseball/Salaries.csv
    /data/cs4266/baseball/AllstarFull.csv

    -rwxr-xr-x   3 fabbrid fabbrid      7.8 M 2016-12-20 12:13 /data/cs4266/baseball/Fielding.csv
    -rwxr-xr-x   3 fabbrid fabbrid    731.9 K 2016-12-20 12:13 /data/cs4266/baseball/Salaries.csv
    -rwxr-xr-x   3 fabbrid fabbrid    200.3 K 2016-12-20 12:13 /data/cs4266/baseball/AllstarFull.csv


Useful pig tutorials can be found at: http://www.rohitmenon.com/index.php/apache-pig-tutorial-part-1/ and http://www.rohitmenon.com/index.php/apache-pig-tutorial-part-2/

### 3.1

Write a pig program that outputs the average salary by position.
You will want to use the Fielding.csv and Salaries.csv files.
You will want to join by playerID and yearID (as a pair).
Specific pig commands you will want to use are: load, foreach, filter, join, group and dump.

Run the code as:

    pig 5_avg_salary.pig > 5_avg_salary.out

Note you will want to filter out the header row (which can be done by filtering on values like 'POS' and 'playerID').

Expected results for catchers are:
    
    (C,1323465.548234281)


### 3.2

Write a pig program that outputs the average salary for all star players in 2000 vs non all stars in 2000.
You will want to use the AllstarFull.csv and Salaries.csv files.
You will want to use an outer join and check for `IS NULL` or `IS NOT NULL`.
You can refernce specific attributes in a `table` with the notation `table::attribute`.
You can use the `union` command to combine results.
You can use `group [field] ALL` to group all tuples into a single group.

Run the code as:

    pig 6_all_stars.pig > 6_all_stars.out

Expected results for all stars and non all stars are:

    (5388841.029411765)
    (1692309.78125)
