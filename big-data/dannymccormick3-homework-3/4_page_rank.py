import sys

from pyspark import SparkConf, SparkContext

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

from operator import add

link_file = 'hdfs:///user/%s/link_index' % VUID
rank_file = 'hdfs:///user/%s/ranks' % VUID


'''
Implement page rank.

Mimic the pyspark code: https://github.com/apache/spark/blob/master/examples/src/main/python/pagerank.py

Use the iterations input to control the number of times to loop.

The results should be written to the rank_file.

You will want to use sortBy to order pages by rank.

'''


def propagate(links, rank):
    num_links = len(links)
    for link in links:
        yield (link, rank / num_links)


def page_rank(spark, iterations):
    links = spark.textFile(link_file)
    links = links.map(lambda line: eval(line)) \
        .map(lambda line: (line[0], line[1])) \
        .distinct() \
        .groupByKey() \
        .cache()

    # do something

    #initialize ranks
    ranks = links.map(lambda line: (line[0],1.0))

    for iteration in range(iterations):
        contributions  = links.join(ranks).flatMap(lambda line: propagate(line[1][0],line[1][1]))
        ranks = contributions.reduceByKey(add).mapValues(lambda rank: rank*.85 + .15)

    ranks.saveAsTextFile(rank_file)


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
    page_rank(spark, int(sys.argv[2]))


