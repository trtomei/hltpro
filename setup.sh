
#Usage: Without arguments, this script sets up the SCRAM_ARCH and
#       sources cmsset_default.sh.
#       The first argument is assumed to be the CMSSW release and
#       cmsenv is done in this release.

# SCRAM_ARCH changes rarely so it's OK to hard-code the value
# Just remember to change it two or three times per year

export http_proxy="http://cmsproxy.cms:3128/"
export https_proxy="https://cmsproxy.cms:3128/"
export NO_PROXY=".cms,localhost"
#export SCRAM_ARCH=slc6_amd64_gcc493
#export SCRAM_ARCH=slc6_amd64_gcc530
export SCRAM_ARCH=slc7_amd64_gcc530
#source /opt/hilton/cmssw/cmsset_default.sh
source /opt/offline/cmsset_default.sh

export TZ='-01:00'

# do cmsenv in the release installation directory
if [ "$#" -eq 1 ]; then
    VERSION=$1
    BASE=`scram list -c CMSSW | grep "\<$VERSION\>" | awk '{ print $3; }'`

    if ! [ "$BASE" ]; then
        echo "CMSSW release $VERSION is not installed for the architecture $SCRAM_ARCH"
        scram list CMSSW
    elif ! [ -d "$BASE" ]; then
        echo "The directory $BASE does not exist; the release installation is probably broken."
    else
        pwd=$PWD
        echo "Setting up the CMSSW environment from $BASE" 
        cd $BASE
        eval `scram runtime -sh`
        cd $pwd
    fi
fi
unset VERSION
unset BASE
