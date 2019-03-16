batting = load '/data/cs4266/baseball/Batting.csv' using PigStorage(',') ;
runs = FOREACH batting GENERATE $0 as playerID, $1 as year, $8 as runs;
grp_data = GROUP runs by (year);
max_runs = FOREACH grp_data GENERATE group as grp, MAX(runs.runs) as max_runs;
join_max_run = JOIN max_runs by ($0, max_runs), runs by (year,runs);
join_data = FOREACH join_max_run GENERATE $0 as year, $2 as playerID, $1 as runs;
dump join_data;
