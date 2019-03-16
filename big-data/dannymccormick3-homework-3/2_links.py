from pyspark import SparkConf, SparkContext

import sys
import re

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

MAX_WORDS = 5000
link_file = 'hdfs:///user/%s/link_index' % VUID


'''
Write a spark program that saves to the <link_file> pairs of links (title -> link). 

Links in wikipedia are [[title]]. 
'''
def links(spark, wiki_file):
    wiki_data = spark.textFile(wiki_file)
    wiki_data = wiki_data.map(lambda line: get_title_and_text(line)) \
        .flatMap(lambda (title, text): [(title, link) for link in get_links(text)]) \
        .saveAsTextFile(link_file)

'''
Extract the links in a given wikipedia page text.

Should return a list of links.

Note: If there is a pipe ("|") in the link, only use the text up to the pipe. 
See https://en.wikipedia.org/wiki/Help:Wiki_markup#Links_and_URLs
'''
def get_links(text):
    # implement
    i = 1
    link = 0
    linkList = []
    s = ""
    while i+1 < len(text):
        if link == 1:
            if text[i+1]=="]" and text[i]=="]":
                link = 0
                linkList.append(s)
                s = ""
            else:
                s = s+text[i]
        if text[i-1]=="[" and text[i]=="[":
            link = 1
        i+=1
    toBeReturned = []
    for l in linkList:
        toBeReturned.append(l.split('|')[0])

    return toBeReturned
   
def get_title_and_text(text):
    return (get_title(text), get_text(text))


def get_title(text):
    title = '<title>'
    title_end = '</title>'
    start = text.index(title) + len(title)
    end = text.index(title_end)
    return text[start:end].lower()


# note this function does not remove punctuation.
def get_text(text):
    text_tag = '<text xml:space="preserve">'
    text_end = '</text>'
    start = text.index(text_tag) + len(text_tag)
    end = min(text.index(text_end), start + MAX_WORDS)
    return text[start:end].lower()


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
    links(spark, sys.argv[2])


