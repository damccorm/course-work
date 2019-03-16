from pyspark import SparkConf, SparkContext

import happybase
import sys
import json

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

tf_idf_files = 'hdfs:///user/%s/tf_idf/*' % VUID
rank_files = 'hdfs:///user/%s/ranks/*' % VUID


'''
Store in hbase: word -> {'column_family:page_title': {'title': title, 'word': word, 'tfidf': tfidf, 'pr': pr}}

1. Join tfidf and page ranks to creates tuples of the form: (title, ((title, word, tf-idf), page_rank))
2. Group by word (will need a map before being able to group) to produce tuples of: (word, (title, tfidf, pr))
3. Foreach() group, write to hbase using the store() function. 
4. Use the scan function in 0_setup.py to check results from the command line.

Hbase put info:
http://happybase.readthedocs.org/en/latest/user.html#performing-batch-mutations

'''
def hbase(spark):
    tf_idf_lines = spark.textFile(tf_idf_files)
    tf_idfs = tf_idf_lines.map(lambda line: eval(line)) 

    rank_lines = spark.textFile(rank_files)
    ranks = rank_lines.map(lambda line: eval(line))

    # do something
    testDirectory = "hdfs:///user/mccord1/test"
    tf_idfs.map(lambda line: (line[0], (line[0],line[1],line[2]))) \
        .join(ranks) \
        .map(lambda line: (line[1][0][1],(line[0],line[1][0][2],line[1][1]))) \
        .groupByKey() \
        .foreach(lambda line: store(line[0],line[1]))


'''
Function to store data to hbase.

The input should be a word and the list of (title, tfidf, pr)s to store.

Create a data dictionary:
        data = {
            'title': title,
            'word': word,
            'tfidf': tfidf,
            'pr': pr
        }

Use json.dumps(data) as the value to put into hbase.

'''
def store(word, info_list):
    connection = happybase.Connection(MACHINE, table_prefix=VUID, timeout=3000000)
    table = connection.table(INDEX_TABLE)
    b = table.batch()

    for title, tfidf, pr, in info_list:
        # update these two lines !!
        data = {'title': title, 'word': word, 'tfidf': tfidf, 'pr': pr}
        b.put(word, {COLUMN_FAMILY + ':' + title: json.dumps(data)})
    b.send()
    
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
    hbase(spark)
