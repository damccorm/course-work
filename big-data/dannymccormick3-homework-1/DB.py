import psycopg2


class DB:
    def __init__(self, db_name):
        try:
            self.conn = psycopg2.connect("dbname='%s'" % db_name)
        except:
            print "I am unable to connect to the database"
            exit()
        self.cur = self.conn.cursor()

    def cursor(self):
        return self.cur

    def getNewCursor(self):
        return self.conn.cursor()

    def connection(self):
        return self.conn

    def query(self, q):
        self.cur.execute(q)
        return self.cur.fetchall()


def main():
    db1 = DB('mlb')
    q = 'select * from allstarfull limit 10;'
    print 'MLB DB', db1.query(q)
    print 'Success!'


if __name__ == '__main__':
    main()
