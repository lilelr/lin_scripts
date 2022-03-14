#!/bin/bash
# the first parameter is the interval of Perf
while true
do
 tempcoarse=$(jps|grep Coarse)
 coarse=${tempcoarse:0:5}
 if [ -n "$coarse" ];then
 break
 fi
done

tempdatanode=$(jps|grep Data)
tempworker=$(jps|grep Worker)
#tempcoarse=$(jps|grep Coarse)
datanode=${tempdatanode:0:4}
worker=${tempworker:0:4}
#coarse=${tempcoarse:0:5}
ulimit -n 4096
sudo /usr/src/perf/perf stat -e $2 -I $1 -p $datanode,$worker,$coarse -o /usr/src/data/perf.txt
