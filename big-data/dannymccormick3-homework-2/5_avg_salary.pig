O_FIELDING = LOAD '/data/cs4266/baseball/Fielding.csv' using PigStorage(',') AS (playerid:chararray,yearid:chararray,stint:chararray,teamid:chararray,lgid:chararray,pos:chararray,g:chararray,gs:chararray,innouts:chararray,po:chararray,a:chararray,e:int,dp:chararray,pb:chararray,wp:chararray,sb:chararray,cs:chararray,zr:chararray);
O_SALARY = LOAD '/data/cs4266/baseball/Salaries.csv' using PigStorage(',') AS (yearid:chararray,teamid:chararray,lgid:chararray,playerid:chararray,salary:int);
FIELDING = FILTER O_FIELDING BY pos != 'POS';
SALARY = FILTER O_SALARY BY playerid != 'playerID';
TOGETHER = JOIN FIELDING BY (playerid,yearid), SALARY BY (playerid,yearid);
POSITION_GROUPS = GROUP TOGETHER BY pos;
AVG_SAL = FOREACH POSITION_GROUPS GENERATE group,AVG(TOGETHER.salary);
DUMP AVG_SAL;