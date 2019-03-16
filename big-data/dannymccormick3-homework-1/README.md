# Vanderbilt - Big Data 2017 - Homework 1

In this homework assignment, you will:

    * Verify your account on the cluster
    * Query and analyze MLB data
    * Write solutions to selected programming questions

## Cluster

The cluster is located at bigdata.accre.vanderbilt.edu. To access it run:

    ssh <VUID>@bigdata.accre.vanderbilt.edu

The cluster has many nodes. 
The data nodes, which you will be working on initially are located at abd743 through abd748.
If you are born in January or July use abd743, Feb/Aug use abd744, ..., abd748.

    ssh abd743

## Environments

We will be using anaconda to manage packages and environmens for python.
To create a python 2.7 environment run:

    conda create -n venv python=2.7

To load the environment run:

    source activate venv

You should see "(venv)" at the start of your terminal.

We will then install a Postgres and flake8 packages:

    conda install psycopg2 flake8 nose

In the future, you only need to load the environement (you don't need to re-create or install).

## Source Code

Repositories will be created for each student. You should see yours at 

    https://github.com/vu-bigdata-2017/<GITHUB USERNAME>-homework-1

Clone the repository to your home directory on the cluster using:

    git clone https://github.com/vu-bigdata-2017/<GITHUB USERNAME>-homework-1.git

I may push updates to this homework assignment in the future. To setup an upstream repo, do the following:

    git remote add upstream https://github.com/vu-bigdata-2017/homework-1.git

To pull updates do the following:
    
    git fetch upstream
    git merge upstream/master

You will need to resolve conflicts if they occur. 

To push code to your repo use the git commit and push commands.

## Verify Setup

If you environment is setup, accounts are setup and you have access to the local databases, then
when you run the following command you should see Success!

    python DB.py

## Editor Notes

I use four spaces for tabs in python. If you use vim, you can set that up in your ~/.vimrc file with:

    set expandtab           " enter spaces when tab is pressed
    set textwidth=120       " break lines when line length increases
    set tabstop=4           " use 4 spaces to represent tab
    set softtabstop=4
    set shiftwidth=4        " number of spaces to use for auto indent
    set autoindent          " copy indent from current line when starting a new line

## Code Linting

When submitting code it is recommended to run a linter over the code to verify there are no spacing errors or type
issues. We will be using flake8. Running flake8 FILE will notify you of formatting or variable use errors. 
No output implies success.

    flake8 DB.py

## Homework Submission

We will collect your work through github. Specifically we will clone your repo at a designated time.
Ensure all your code is pushed to your repo.

## SSH Setup

To prevent SSH connections from ending early, it is recommended you add these lines to ~/.ssh/config

    ServerAliveInterval 60
    TCPKeepAlive yes
    KeepAlive yes

## Github

To set up your github environment, run:

    git config --global user.name "Your Name"
    git config --global user.email you@example.com

Once you modify files, use git's add, commit and push commands to push files to your repo. 

    git add file.txt
    git commit -a -m 'commit message'
    git push origin master

## Database

We will be using PostgreSQL for this homework. The database is called: mlb

To login to the mlb db, run the following:
    
    psql mlb 

To see a list of tables run:

    \d

To see table info for the 'allstarfull' table run:

    \d allstarfull

To see ten allstars run:

    select * from allstarfull limit 10;

To exit postgres run:

    \q

Postgres requires semicolons to end statements.

## Part 1 - MLB

Write queries to answer the specified questions in mlb.py

You can run the script with:

    python mlb.py

We will be grading homeworks by code reviews and test cases. You can test your test case results by running:

    nosetests mlb.py

## Part 2 - Targeted Sum

Implement the task defined in targeted\_sums.py.

Evaluate tests with:
    
    nosetests targeted_sums.py

## Part 3 - Bash

Implement the task defined in bash.py.

Evaluate tests with:
    
    nosetests bash.py


