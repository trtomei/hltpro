#!/bin/bash

# Usage: ./cleanGenerateAndRun.sh <run #> <# of cores (optional)> <skipRepack (optional)>
# If no argument for the number of cores is provided, will run with `grep -c processor /proc/cpuinfo`/2 
# See /nfshome0/hltpro/scripts/nCoresOnly.sh for details.
# Repack check is now run by default after hltd jobs finish. If "skipRepack" is given as 2nd or 3rd arg,
# the repack check will be skipped.

if [[ $# -ge 2 && $2 =~ [0-9]+$ ]]; then
    nCores=$2
fi

run=$1
if [[ $# -ge 1 && $run =~ [0-9]+$ ]]; then
    /nfshome0/hltpro/scripts/cleanRun.sh $run
    cmsRun genTestFakeBuFromRAW_cfg.py  runNumber=$run
    /nfshome0/hltpro/scripts/startHiltonRun.sh $run $nCores
else
    echo "Need at least one positive integer argument: the run number"
fi


# This loop looks for running cmsRun jobs and waits until there are no longer any
sleep 10 #<-- this is needed here or else the rest will be skipped
while [ $(ps -u daqlocal | grep "cmsRun" | grep -v "grep" | wc -l) -gt 0 ]; do
    echo "jobs still running ..."
    sleep 10
done
echo "jobs finished."

# Skip repack check if specified:
if [[ $# -ge 2 && ($2 == "skipRepack" || $3 == "skipRepack") ]]; then
    exit
fi

# Now actually run check
echo "Running repack check..."
echo " "
streamFindCommand='find /fff/BU0/output/run'$run'/ -maxdepth 1 -mindepth 1 -type d'
streamList=($($streamFindCommand))
mkdir -p /cmsnfsscratch/globalscratch/hltpro/testRepack/input
mkdir -p /cmsnfsscratch/globalscratch/hltpro/testRepack/output

for streamdir in "${streamList[@]}"; do
    stream=$(basename $streamdir)
    newfile=/cmsnfsscratch/globalscratch/hltpro/testRepack/input/$stream.dat
    cat $streamdir/data/* > $newfile
    cmsRun /nfshome0/hltpro/scripts/RunRepackCfg.py $newfile #> testRepack/output/$stream.log
done

echo " "
echo "Done. Output of repack check is: /cmsnfsscratch/globalscratch/hltpro/testRepack/output/"
