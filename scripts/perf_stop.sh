#!/bin/bash

perfpids=`ps -ef|grep perf|grep -v grep|awk '{print $2}'`

for pid in $perfpids
do 
if [ $pid != '' ];then
kill -9 $pid
fi 
done
