#!/bin/bash

if [[ $# -ge 2 && $2 =~ [0-9]+$ ]]; then
    nCores=$2
fi

run=$1
if [[ $# -ge 1 && $run =~ [0-9]+$ ]]; then
    /nfshome0/hltpro/scripts/addMissingEoLS.sh $run
    sudo chmod -R 777 /fff
    sudo /sbin/service hltd restart
    /nfshome0/hltpro/scripts/nCoresOnly.sh $nCores
    sleep 5
    curl "http://localhost:9000/cgi-bin/start_cgi.py?run=${run}"
else
    echo "Need at least one positive integer argument: the run number"
fi
