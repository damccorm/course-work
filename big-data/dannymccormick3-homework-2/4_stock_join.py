from mrjob.job import MRJob


'''
Implement: A join on NYSE quote and dividend data for symbols starting with A where the symbol and the date are equal.


STOCK_A = LOAD '/data/cs4266/finance/NYSE_daily_prices_A.csv' using PigStorage(',') AS (exchange:chararray, symbol:chararray,
date:chararray, open:float, high:float, low:float, close:float, volume:int, adj_close:float);
DIV_A = LOAD '/data/cs4266/finance/NYSE_dividends_A.csv' using PigStorage(',') AS (exchange:chararray, symbol:chararray,
date:chararray, dividend:float);
C = JOIN STOCK_A BY (symbol, date), DIV_A BY (symbol, date);
D = LIMIT C 10;
dump D;


Notes:
You will need to parse each line using line.split(',')
Use the length of the line to determine if it is a dividend or quote.
'''


class StockJoin(MRJob):
    # Using SORT_VALUES to sort on all fields, not just first
    SORT_VALUES = True

    def mapper(self, _, line):
        cols = line.split(',')
        key = cols[1] + ',' + cols[2]
        yield(key, line)
        pass

    def reducer(self, pair, lines):
        STOCK_A = []
        DIV_A = []
        for line in lines:
            cols = line.split(',')
            if len(cols) == 9:
                STOCK_A.append(cols)
            if len(cols) == 4:
                DIV_A.append(cols)
        for stock in STOCK_A:
            for div in DIV_A:
                joined = stock + div
                yield(1,joined)

        pass

    def reducer_limit(self, _, joins):
        i = 0
        for join in joins:
            if i < 10:
                yield (None,join)
                i = i + 1
        pass

    def steps(self):
        return [
            self.mr(mapper=self.mapper, reducer=self.reducer),
            self.mr(reducer=self.reducer_limit)
        ]


def test_count():
    f = open('4_stock_join.out')
    lines = f.readlines()
    f.close()

    assert lines[0][:-1] in [
        'null  ["NYSE", "AA", "1962-02-06", "59.13", "59.13", "58.25", "58.75", "97600", "0.63", "NYSE", "AA", "1962-02-06", "0.0125"]',
        'null\t["NYSE", "AA", "1962-02-06", "59.13", "59.13", "58.25", "58.75", "97600", "0.63", "NYSE", "AA", "1962-02-06", "0.0125"]']

    assert len(lines) == 10


if __name__ == '__main__':
    StockJoin.run()
