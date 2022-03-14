#!/bin/bash

algrs=("LogisticRegression" "SVM" "KMeans" "LinearRegression" "DecisionTree")
rootPath=/usr/lib/hadoop/spark-bench/
for algr in ${algrs[*]}
do
  $rootPath$algr'/conf/env.sh'
