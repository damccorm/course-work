from pyspark import SparkConf, SparkContext

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN
from operator import add

import sys

index_file = 'hdfs:///user/%s/word_index/*' % VUID
tf_idf_file = 'hdfs:///user/%s/tf_idf/' % VUID


'''
Term frequency inverse document frequency
https://en.wikipedia.org/wiki/Tf%E2%80%93idf

Input:
(u'akrotiri and dhekelia,are', 22)
(u'john roddam spencer stanhope,by', 20)
(u'outline of japan,div', 21)


term frequency(t, d) = # of times t occurs in d / number of words in d
inverse document frequency(t, D) = # of distinct pages in the corpus / # of pages t occurs in D

1. Count the number of words in d. Use map() and reduceByKey(). Output should be: (title, count)
2. Determine the frequency of t in a page. Use keyBy(), join() and map(). Output should be: (title, word, term-freq)
3. Count the number of distinct pages. Use map(), distinct() and count(). Output should be a single int
4. Determine the inverse document frequency. Use map(), groupByKey() and map(). Output should be: (word, inverse-doc-freq)
5. Calculate tf-idf. Use keyBy(), join(), map(), and sortBy(). Output should be: (title, word, tf-idf)
6. Save output to tf_idf_file using saveAsTextFile().

You will need to use the keyBy function to join.

You will want to use groupByKey and reduceByKey.

Save the result to the <tf_idf_file> (i.e., saveAsTextFile(tf_idf_file)). 

It is also useful to use sortBy on title and tf-idf to look at the final results.

'''
def tf_idf(spark):
    word_data = spark.textFile(index_file)
    lines = word_data.map(lambda line: eval(line)) \
        .map(lambda line: split_input(line))

    # do something
    #1
    count = lines.map(lambda line: (line[0],line[2])) \
        .reduceByKey(add)

    #2
    frequency = lines.map(lambda line: (line[0],(line[1],line[2]))) \
        .join(count) \
        .map(lambda line: (line[0],((line[1])[0])[0],float(((line[1])[0])[1])/float((line[1])[1])))

    #3
    numPages = lines.map(lambda line: (line[0])) \
        .distinct() \
        .count()
    

    #4
    idf = lines.map(lambda line: (line[1],line[0])) \
        .groupByKey() \
        .map(lambda line: (line[0],numPages/len(line[1])))

    #5/6
    tfidf = frequency.map(lambda line: (line[1],(line[0],line[2]))) \
        .join(idf) \
        .map(lambda line: (((line[1])[0])[0],line[0],(line[1])[1]*((line[1])[0])[1])) \
        .sortBy(lambda line: (line[0],line[1])) \
        .saveAsTextFile(tf_idf_file)

'''
Take line from input file and convert to tuple of (title, word, count)
'''
def split_input(line):
    return line[0].split(',')[0], line[0].split(',')[1], line[1]



if __name__ == '__main__':
    conf = SparkConf()
    if sys.argv[1] == 'local':
        conf.setMaster("local[3]")
        print 'Running locally'
    elif sys.argv[1] == 'cluster':
        #conf.setMaster("spark://10.0.22.241:7077")
        print 'Running on cluster' 
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.driver.memory", "10g")
    spark = SparkContext(conf = conf)
    tf_idf(spark)


