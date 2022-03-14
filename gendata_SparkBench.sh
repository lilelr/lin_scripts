#!/bin/bash
#algrs=("KMeans" "LogisticRegression" "LinearRegression" "SVM" "DecisionTree" "Terasort" "SQL" "PCA" "PageRank" "PregelOperation" "ConnectedComponent" "LabelPropagation" "MatrixFactorization" "SVDPlusPlus" "ShortestPaths" "Streaming" "StronglyConnectedComponent" "TriangleCount")
#algrs=("LogisticRegression" "SVM" "KMeans" "LinearRegression" "DecisionTree")
#algrs=("LinearRegression" "DecisionTree")
#algrs=("PageRank" "PregelOperation")
algrs=("KMeans")
#algrs=("KMeans" "LinearRegression" "DecisionTree")
#algrs=("ConnectedComponent" "LabelPropagation" "MatrixFactorization" "SVDPlusPlus")
#algrs=("ShortestPaths" "Streaming" "StronglyConnectedComponent" "TriangleCount")
for algr in ${algrs[*]}
 do
  /usr/lib/hadoop/spark-bench/$algr/bin/gen_data.sh
 wait
 done
