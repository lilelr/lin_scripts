#!/bin/bash
slavers=("2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19")
#slavers=("2" "3" "4" "5" "6" "7" "8" "19")
#slavers=("2" "19")
for i in ${slavers[*]}
do
  i="slaver"${i}
  ssh $i "/usr/src/scripts/perf_stop.sh ; exit"
  echo "$i ---perf stoped---"
done

#for i in slaver2 slaver3 slaver4 slaver5
#do
#  ssh $i "/usr/src/scripts/perf_stop.sh ; exit"
#  echo "OK"
#done
