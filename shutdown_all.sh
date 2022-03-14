#!/bin/bash

for i in master slaver2 slaver3 slaver4 slaver5 slaver6 slaver7 slaver8 slaver9 slaver10 slaver11 slaver12 slaver13 slaver14 slaver15 slaver16 slaver17 slaver18 slaver19 slaver20
do 
 ssh $i "shutdown -h now"
done
shutdown -h now
