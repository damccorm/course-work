STOCK_A = LOAD '/data/cs4266/finance/NYSE_daily_prices_A.csv' using PigStorage(',') AS (exchange:chararray, symbol:chararray, date:chararray, open:float, high:float, low:float, close:float, volume:int, adj_close:float);
DIV_A = LOAD '/data/cs4266/finance/NYSE_dividends_A.csv' using PigStorage(',') AS (exchange:chararray, symbol:chararray, date:chararray, dividend:float);
C = JOIN STOCK_A BY (symbol, date), DIV_A BY (symbol, date);
D = LIMIT C 10;
dump D;
