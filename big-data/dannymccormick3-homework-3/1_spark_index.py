from pyspark import SparkConf, SparkContext

import sys
import re

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

MIN_OCCURRENCES = 10
MAX_WORDS = 5000

index_file = 'hdfs:///user/%s/word_index' % VUID


'''
Implement a function that return a list of key-value pairs of the form: 
key: "title,word"
value: count of the word on the page

The result is output to <index_file> using saveAsTextFile(index_file)

'''

def combiner(title, text):
    # implement
	toBeReturned = []
	alreadySeen = {}
	for w in text:
                if (title + "," + w) not in alreadySeen:
                        alreadySeen[(title + "," + w)] = 1
                else:
                        alreadySeen[(title + "," + w)] += 1
        for key, value in alreadySeen.iteritems():
                toBeReturned.append((key,value))
        return toBeReturned


def index(spark, wiki_file):
    wiki_data = spark.textFile(wiki_file) 
    wiki_data = wiki_data.map(lambda line: get_title_and_text(line)) \
        .flatMap(lambda (title, text): combiner(title, text)) \
        .filter(is_frequent) \
        .saveAsTextFile(index_file)


def is_frequent(index_record):
    if index_record[1] > MIN_OCCURRENCES:
            return True
    return False


def get_title_and_text(text):
    return (get_title(text), get_text(text))


def get_title(text):
    title = '<title>'
    title_end = '</title>'
    start = text.index(title) + len(title)
    end = text.index(title_end)
    return text[start:end].lower()


def get_text(text):
    text_tag = '<text xml:space="preserve">'
    text_end = '</text>'
    start = text.index(text_tag) + len(text_tag)
    end = text.index(text_end)
    text_block = text[start:end].lower()
    return re.sub(r"\W+", ' ', text_block).strip().split(' ')[:MAX_WORDS]


if __name__ == '__main__':
    conf = SparkConf()
    if sys.argv[1] == 'local':
        conf.setMaster("local[3]")
        print 'Running locally'
    elif sys.argv[1] == 'cluster':
        #conf.setMaster("spark://10.0.22.241:7077")
        print 'Running on cluster' 
    spark = SparkContext(conf = conf)
    index(spark, sys.argv[2])


