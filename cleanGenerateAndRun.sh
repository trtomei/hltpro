#!/bin/bash

#If no argument for the number of cores is provided, will run with `grep -c processor /proc/cpuinfo`/2 
#See /nfshome0/hltpro/scripts/nCoresOnly.sh for details
if [[ $# -ge 2 && $2 =~ [0-9]+$ ]]; then
    nCores=$2
fi

run=$1
if [[ $# -ge 1 && $run =~ [0-9]+$ ]]; then
    /nfshome0/hltpro/scripts/cleanRun.sh $run
    cmsRun genTestFakeBuFromRAW_cfg.py
    /nfshome0/hltpro/scripts/startHiltonRun.sh $run $nCores
else
    echo "Need at least one positive integer argument: the run number"
fi