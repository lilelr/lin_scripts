#!/bin/bash
date=`date +%m%d%H%M%S`
mkdir /usr/src/data/lin/$1'-'$2'MB-'$3'slavers-'$4'ms-'$5'events-'$6'iter-'$date
slavers=("2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19")
#slavers=("2" "3" "4" "5" "6" "7" "8" "19")
#slavers=("2" "19")
for machine in ${slavers[*]}
do
  machine="slaver"${machine}
  echo $machine
  scp root@$machine:/usr/src/data/perf.txt /usr/src/data/lin/$1'-'$2'MB-'$3'slavers-'$4'ms-'$5'events-'$6'iter-'$date/$machine.txt
done


#date=`date +%m%d%H%M%S`
#mkdir /usr/src/data/$1'-'$2'MB-'$3'slavers-'$4'ms-'$date
#for machine in slaver2 slaver3 slaver4 slaver5
#do
#    scp root@$machine:/usr/src/data/perf.txt /usr/src/data/$1'-'$2'MB-'$3'slavers-'$4'ms-'$date/$machine.txt
#done
