import commands

FILE_NAME = 'bonds.csv'

'''
Use cat, grep, wc, cut, sort, head and tail to implement the following tasks.
You can use the man page for each command for detailed instructions.

1. A command to count the lines in bonds.csv

2. A command to count the number of lines between 2000-2009.
The second column is the year.

3. A command to count the number of lines not between 2000-2009.

4. A command to extract the largest number of games Bonds played in a year.
Games played is column six.

5. A command to extract the distinct teams Bonds played for.
Team is column four.

6. A command to extract the year from the first row in file.
'''


c1 = 'cat bonds.csv | wc -l'

c2 = "cut -d, -f2 bonds.csv | grep 200. | wc -l"

c3 = "cut -d, -f2 bonds.csv | grep -v 200. | wc -l"

c4 = "cut -d, -f6 bonds.csv | sort -r | head -1"

c5 = "cut -d, -f4 bonds.csv  | sort -u"

c6 = "cut -d, -f2 bonds.csv  | head -1"


def main():
    for c in [c1, c2, c3, c4, c5, c6]:
        print commands.getstatusoutput(c)


if __name__ == '__main__':
    main()


def test_c1():
    v, out = commands.getstatusoutput(c1)
    assert out == '22'


def test_c2():
    v, out = commands.getstatusoutput(c2)
    assert out == '8'


def test_c3():
    v, out = commands.getstatusoutput(c3)
    assert out == '14'


def test_c4():
    v, out = commands.getstatusoutput(c4)
    assert out == '159'


def test_c5():
    v, out = commands.getstatusoutput(c5)
    assert out == 'PIT\nSFN'


def test_c6():
    v, out = commands.getstatusoutput(c6)
    assert out == '1986'
