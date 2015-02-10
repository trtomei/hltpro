#!/bin/bash

#Usage: Without arguments, this script sets up the SCRAM_ARCH and
#       sources cmsset_default.sh.
#       The first argument is assumed to be the CMSSW release and
#       cmsenv is done in this release.

#SCRAM_ARCH changes rarely so it's OK to hard-code the value
#Just remember to change it two or three times per year

export http_proxy="http://cmsproxy.cms:3128/"
export https_proxy="https://cmsproxy.cms:3128/"
export NO_PROXY=".cms,localhost"
export SCRAM_ARCH=slc6_amd64_gcc481
source /opt/offline/cmssw/cmsset_default.sh

#Do cmsenv
if [ "$#" -eq 1 ]; then
    
    cmsswVers=$1

    cmsenvPath=/opt/offline/cmssw/${SCRAM_ARCH}/cms/cmssw/${cmsswVers}
    if [[ $cmsswVers == *patch* ]]; then
	cmsenvPath=/opt/offline/cmssw/${SCRAM_ARCH}/cms/cmssw-patch/${cmsswVers}
    fi
        
    if [ -d $cmsenvPath ]; then
	echo "Doing cmsenv in $cmsenvPath" 
        cd $cmsenvPath
        eval `scramv1 runtime -sh`
	cd -
    else
	echo "No $cmsenvPath directory found"
    fi
fi
