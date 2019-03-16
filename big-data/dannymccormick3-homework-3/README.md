# Vanderbilt - Big Data 2017 - Homework 3

In this homework assignment, you will:

    * Build a Goolge like index on Wikipedia

## Environments

To load the environment run:

    source activate venv

You should see "(venv)" at the start of your terminal.

Install the following:
    
    pip install happybase

Please add the following line to ~/.bashrc, if you have not yet done so.

    export HADOOP_HOME=/opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/

## Data

We will be using three data sets:

    hadoop fs -ls /data/cs4266/wiki/wiki_page*

    -rwxr-xr-x   3 fabbrid fabbrid      26.0 G 2016-12-20 13:21 /data/cs4266/wiki/wiki_page_per_line.txt
    -rwxr-xr-x   3 fabbrid fabbrid       6.2 G 2016-12-20 13:23 /data/cs4266/wiki/wiki_page_per_line_ball.txt
    -rwxr-xr-x   3 fabbrid fabbrid      22.4 K 2016-12-20 13:23 /data/cs4266/wiki/wiki_page_per_line_small.txt

Each line in the file is a wikipedia page (which I made multi line here for reading purposes). They are formatted like:

     <page>    <title>000 Emergency</title>    <ns>0</ns>    <id>2670808</id>    <revision>      <id>703175760</id>
     <parentid>703175688</parentid>      <timestamp>2016-02-03T23:31:00Z</timestamp>      <contributor>
     <username>Oshwah</username>        <id>3174456</id>      </contributor>      <minor />      <comment>Reverted edits
     by [[Special:Contributions/180.190.115.194|180.190.115.194]] ([[User talk:180.190.115.194|talk]]): Unexplained
     removal of content ([[WP:HG|HG]]) (3.1.18)</comment>      <model>wikitext</model>      <format>text/x-wiki</format>
     <text xml:space="preserve">
        ... [[007 Legends]]
     </text></page>

Links to other pages are formatted with [[ ]]. So, the link to the page titles 007 Legends looks like [[007 Legends]].

You can see sample content in the file using:

    hadoop fs -cat /data/cs4266/wiki/wiki_page_per_line.txt | less

You can also get a local copy of the file using:

    hadoop fs -get /data/cs4266/wiki/wiki_page_per_line_small.txt .

## Source Code

Repositories will be created for each student. You should see yours at 

    https://github.com/vu-bigdata-2017/<GITHUB USERNAME>-homework-3

Clone the repository to your home directory on the cluster using:

    git clone https://github.com/vu-bigdata-2017/<GITHUB USERNAME>-homework-3.git

I may push updates to this homework assignment in the future. To setup an upstream repo, do the following:

    git remote add upstream https://github.com/vu-bigdata-2017/homework-3.git

To pull updates do the following:
    
    git fetch upstream
    git merge upstream/master

You will need to resolve conflicts if they occur. 


## Spark

You will be using Spark for this assignment. A good tutorial can be found at: http://www.mccarroll.net/blog/pyspark2/

Documentation is also at: https://spark.apache.org/docs/0.7.2/api/pyspark/pyspark.rdd.RDD-class.html

Remember that spark doesn't actually run until you call collect, cache, take, or other functions to materialize results.

The 'take' function is useful to only look at the first X samples of the data.

## Part 0 - Setup

Modify variables.py to set your VUID.

## Part 1 - Index words

Write a spark program that extracts (title, word) -> counts from wikipedia pages.

Initially run on a small file locally. This will save the output to hdfs in your directory.

    pyspark 1_spark_index.py local hdfs:///data/cs4266/wiki/wiki_page_per_line_small.txt

To see the output, run (with your VUID):

    hadoop fs -cat /user/vuid/word_index/* | sort

    (u'000 emergency,000', 31)
    (u'000 emergency,0', 18)
    (u'000 emergency,1', 18)
    (u'000 emergency,2009', 13)
    (u'000 emergency,a', 29)
    (u'000 emergency,accessdate', 11)
    (u'000 emergency,an', 11)

If you want to re-run the code, you need to delete or move the output directory. To delete, run:

    hadoop fs -rm -f -R /user/vuid/word_index

To run on the subset of wikipedia that has 'ball' on the cluster run (which is all we will do for this homework):

    pyspark 1_spark_index.py cluster hdfs:///data/cs4266/wiki/wiki_page_per_line_ball.txt

## Part 2 - Extract Links

Write a spark program that extracts links from Wikipeia. Links are enclosed in [[title]].

    pyspark 2_links.py local hdfs:///data/cs4266/wiki/wiki_page_per_line_small.txt

You should see the following output:

    hadoop fs -cat /user/vuid/link_index/*

    (u'000 emergency', u'emergency telephone number')
    (u'000 emergency', u'finland')
    (u'000 emergency', u'government of australia')
    (u'000 emergency', u'norway')


To run on the subset of wikipedia that has 'ball' on the cluster run:

    pyspark 2_links.py cluster hdfs:///data/cs4266/wiki/wiki_page_per_line_ball.txt

## Part 3 - Calculate Term frequency - Inverse Document Frequency

Identify important words in a page. 
I recommend you build each part of the calculation one-by-one. Then combine them.

    pyspark 3_tfidf.py cluster

You can view the output with:

    hadoop fs -cat /user/vuid/tf_idf/* | less

Sample output looks like:

    (u'michael jordan', u'the', 0.11754849790361308)
    (u'michael jordan', u'mvp', 8.459374812297817)
    (u'michael jordan', u'jordan', 26.485210266492054)


You can delete the output with:

    hadoop fs -rm -R -f /user/vuid/tf_idf

## Part 4 - Page Rank

Use the extracted links from part 2 to calculate page rank.

    pyspark 4_page_rank.py cluster 10

The 10 refers to the number of iterations to run.

To view the results run:

    hadoop fs -cat /user/vuid/ranks/* | less

The highest ranked pages at the end of the file (if sorted) will look like:

    (u'baseball', 94.58879758629737)
    (u'football (soccer)', 99.82634799064857)
    (u'basketball', 104.69536483500916)
    (u'college football', 106.4944323069795)
    (u'national football league', 120.6350040323033)
    (u'major league baseball', 127.80469819047917)
    (u'american football', 177.01236495305528)
    (u'united states', 204.68917317253945)
    (u'wikipedia:persondata', 291.7456160982039)
    (u'category:living people', 312.91471412995185)
    (u'association football', 358.5487286834513)

You can delete the results with:

    hadoop fs -rm -r -R /user/vuid/ranks

## Part 5 - Hbase

Run the setup.py script to create your Hbase environment with associated tables. Make sure you updated your VUID in
variables.py.

    python 0_setup.py

If you want to delete the table and start over, run:

    python 0_setup.py delete

If you want to scan the data in a table run (print 100 rows):

    python 0_setup.py scan

Store the results of the tf-idf and page rank computation in Hbase. You will store:

    word -> {'column_family:page_title': {'title': title, 'word': word, 'tfidf': tfidf, 'pr': pr}}

To do a small test, try:

    pyspark 5_hbase.py local

To run across the cluster, run:

    pyspark 5_hbase.py cluster

You can check your results by running:

    python 0_setup.py scan

## Part 6 - Search

Given a keyword search (which may contain multiple words), return the top-K (10) pages. 
You should use the scoring function: tf-idf + W * page\_rank.
Rank pages by that scoring function.

To search for pages with 'nfl' do:

    python 6_search.py nfl

The results I see with W = 4 are:

    Searching for ['nfl']
    [(708.8916152258975, u'american football'), (485.6541559373692, u'national football league'), (426.36064572769106,
    u'college football'), (133.80996584050172, u'quarterback'), (97.05174604543102, u'super bowl'), (87.51840899591404,
    u'green bay packers'), (76.15414544127205, u'american football league'), (70.42001501075907, u'new york giants'),
    (69.00211121715267, u'chicago bears'), (63.60110284177957, u'washington redskins')]

TO search for pages with 'air jordan' do:

    python 6_search.py air jordan

The results I see are:

    Searching for ['air', 'jordan']
    [(68.45531560644798, u'air jordan'), (26.296558543734292, u'tinker hatfield'), (13.631317260002795, u'fibber mcgee and molly')]
