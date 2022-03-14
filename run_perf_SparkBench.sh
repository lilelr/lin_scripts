#!/bin/bash
#algrs=("KMeans" "LogisticRegression" "LinearRegression" "SVM" "DecisionTree" "Terasort" "SQL" "PCA" "PageRank" "PregelOperation" "ConnectedComponent" "LabelPropagation" "MatrixFactorization" "SVDPlusPlus" "ShortestPaths" "Streaming" "StronglyConnectedComponent" "TriangleCount")
#algrs=("LogisticRegression" "SVM" "KMeans" "LinearRegression" "DecisionTree")
#algrs=("LinearRegression" "DecisionTree")
#algrs=("PageRank" "PregelOperation")
#algrs=("LogisticRegression")
algrs=("KMeans")
#algrs=("KMeans" "LinearRegression" "DecisionTree")
#algrs=("ConnectedComponent" "LabelPropagation" "MatrixFactorization" "SVDPlusPlus")
#algrs=("ShortestPaths" "Streaming" "StronglyConnectedComponent" "TriangleCount")
#iters=("1" "2" "3" "4" "5" "6")
iters=("1")
#for algr in ${algrs[*]}
# do
#  /usr/src/scripts/lin_scripts/perf_start_all.sh 1000
#  /usr/lib/hadoop/spark-bench/$algr/bin/run.sh
#  sleep 2
#  /usr/src/scripts/lin_scripts/perf_stop_all.sh
#  wait
#  /usr/src/scripts/lin_scripts/getresult.sh $algr 4096 18 1000 
#  wait
# done

function get_event(){
  cat $1 | while read line
  do
    echo "$line"
  done
}

path=/usr/src/scripts/lin_scripts/perf_events
events=("archi_1" "archi_2" "archi_3" "archi_4" "archi_5" "archi_6" "archi_7" "archi_8" "archi_9" "archi_10" "archi_11" "archi_12")

for algr in ${algrs[*]}
do
  for event in ${events[*]}
  do
    eventSet=`get_event $path'/'$event'.txt'`
    for iter in ${iters[*]}
    do
      /usr/src/scripts/lin_scripts/perf_start_all.sh 1000 $eventSet
      /usr/lib/hadoop/spark-bench/$algr/bin/run.sh
      sleep 2
      /usr/src/scripts/lin_scripts/perf_stop_all.sh
      wait
      /usr/src/scripts/lin_scripts/getresult.sh $algr 256 18 1000 $event $iter
      wait
    done
  done
done
