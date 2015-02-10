#!/bin/bash

run=$1

lsMax=0
for f in `ls /fff/BU0/ramdisk/run${run} | grep EoLS`; do
nls=`echo $f | sed s/run${run}_ls// | sed s/_EoLS.jsn// | sed s/^0*//`
if [[ $nls -gt $lsMax ]]; then
lsMax=$nls
fi
done

if [[ $lsMax -gt 0 && $lsMax -le 9999 ]]; then
    wzMax=`printf '%04d' ${lsMax}`
    fileMax=/fff/BU0/ramdisk/run${run}/run${run}_ls${wzMax}_EoLS.jsn

    cat $fileMax | sed '2 s/[0-9][0-9]*/0/g' > tempEoLS.jsn

    for ff in `seq 1 $lsMax`; do
	wz=`printf '%04d' ${ff}`
	file=/fff/BU0/ramdisk/run${run}/run${run}_ls${wz}_EoLS.jsn
	if [[ ! -e ${file} ]]; then
	    echo Adding missing End-of-Lumi-Section file ${file}
	    cp tempEoLS.jsn ${file}
	fi
    done
    rm tempEoLS.jsn
fi