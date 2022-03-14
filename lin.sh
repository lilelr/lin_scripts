#!/bin/bash
#
#date=`date +%m%d%H%M%S`
#mkdir /usr/src/data/$1'-'$2'MB-'$3'slavers-'$4'ms-'$date
slavers=("2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19")
#slavers=("2" "3" "4" "5" "6" "7" "8" "19")
for machine in ${slavers[*]}
do
  machine="slaver"${machine}
  echo $machine
  scp /usr/src/scripts/lin_scripts/scripts/perf_start.sh root@$machine:/usr/src/scripts/perf_start.sh
done

<<!
function getdir(){
  for element in `ls $1`
  do
    file=$1'/'$element
    #echo $file
    cat $file | while read line
    do
      echo "$line"
      #echo "$line" | awk '{for(i=1;i<=NF;i++) print $i}'
    done
  done
}

function getfile(){
  cat $1 | while read line
  do
   echo "$line"
  done
}

path=/usr/src/scripts/lin_scripts/perf_events
getdir $path

events=("archi_1.txt" "archi_2.txt")
for event in ${events[*]}
do
  a=`getfile $path'/'$event`
  echo $a
done
!
