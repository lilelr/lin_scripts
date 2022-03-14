#!/bin/bash
# the first parameter is the interval of Perf

while true
do
 tempExecutors=$(jps |grep CoarseGrainedExecutor |  cut -d" " -f 1)
#  tempExecutors=${tempcoarse:0:4}
 if [ -n "$tempExecutors" ];then
 break
 fi
done

sleep 1
echo "sleep 1"
# tempdatanode=$(jps|grep Data)
# tempExecutor=$(jps|grep CoarseGrainedExecutor)


tempExecutors=$(jps |grep CoarseGrainedExecutor |  cut -d" " -f 1)

pros=${tempExecutors[0]}

pros=$(echo $pros | tr -t [:space:] ",")
pros=$(echo $pros | sed 's/[ ][ ]*/,/g')

# for(( i=1;i<${#tempExecutors[@]};i++)) do
#       pros="$pros,${tempExecutors[i]}"
# echo 
# done;

echo ${pros}
# jps |grep NameNode |  cut -d" " -f 1
#tempcoarse=$(jps|grep Coarse)
# datanode=${tempdatanode:0:4}
# worker=${tempExecutor:0:4}
#coarse=${tempcoarse:0:5}
# date  '+%Y-%m-%d %H:%M'
ulimit -n 4096
# sudo /usr/src/perf/perf stat -e $2 -I $1 -p $datanode,$worker,$coarse -o /usr/src/data/perf.txt
date_str=$(date '+%Y-%m-%d-%H:%M')
echo ${date_str}
sudo /usr/bin/perf stat -e cycles,instructions,cache-misses,branch-misses,context-switches,cpu-migrations,page-faults,dTLB-load-misses,iTLB-load-misses,LLC-loads,LLC-load-misses,LLC-stores,LLC-prefetches -B -p ${pros} -o ./${date_str}-perf.txt

