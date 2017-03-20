#! /bin/bash

#Usage: This script takes two inputs: The HLT menu python file and a payload hash for the corresponding L1 xml.
#       It then checks that every instance of "L1SeedsLogicalExpression" in the HLT menu
#       matches to an algorithm name in the L1 xml.
#       If the HLTL1TSeed module L1Seed parameter name changes or the L1 xml format changes,
#       the script will need to be updated.

if [ "$#" -ne 2 ]; then
    echo "Need exactly two arguments: (1) the HLT menu python and (2) a payload hash for the L1 xml"
    exit 1
fi

if [[ -z "$CMSSW_VERSION" ]]; then
    echo "You need to do cmsenv first"
    exit 1
fi

#can get GT from menu with:
#   grep "globaltag" /opt/hltd/python/HiltonMenu.py | sed 's/.*"\(.*\)".*$/\1/g'

menu=$1
xmlhash=$2

#All this is to get around the fact that conddb dump tries to modify the release base
#I have tried to make this robust, but I am not very confident. I have no doubt that this will break sometime in the future...
srcpath=`echo $CMSSW_SEARCH_PATH | sed '0,/:.*$/s/:.*$//'`
scramv1 project CMSSW $CMSSW_VERSION 2> /dev/null
cd $CMSSW_VERSION/src
eval `scramv1 runtime -sh`
mkdir -p ../python/CondCore
mkdir -p CondCore
mkdir -p ../bin/$SCRAM_ARCH
cp -r $srcpath/../python/CondCore/Utilities ../python/CondCore/
cp -r $srcpath/CondCore/Utilities CondCore/
cp $srcpath/../bin/$SCRAM_ARCH/conddb ../bin/$SCRAM_ARCH/
cmsset=`echo $srcpath | sed 's/\/opt\/\(......\).*$/\1/'`
if [ "$cmsset" == "offlin" ]; then
    sed -i 's/\/afs\/cern.ch\/cms\/cmsset_default.sh/\/opt\/offline\/cmsset_default.sh/' CondCore/Utilities/python/cond2xml.py
elif [ "$cmsset" == "hilton" ]; then
    sed -i 's/\/afs\/cern.ch\/cms\/cmsset_default.sh/\/opt\/hilton\/cmssw\/cmsset_default.sh/' CondCore/Utilities/python/cond2xml.py
else
    echo "Could not determine release base (/opt/offline or /opt/hilton). L1MenuCheck is going to fail."
fi
../bin/$SCRAM_ARCH/conddb --db "oracle+frontier://@frontier%3A%2F%2F%28proxyurl%3Dhttp%3A%2F%2Flocalhost%3A3128%29%28serverurl%3Dhttp%3A%2F%2Flocalhost%3A8000%2FFrontierOnProd%29%28serverurl%3Dhttp%3A%2F%2Flocalhost%3A8000%2FFrontierOnProd%29%28retrieve%2Dziplevel%3D0%29/CMS_CONDITIONS" dump $xmlhash >& ../../tmp.xml 2> /dev/null
cd ../..
rm -r $CMSSW_VERSION
#You can run this script offline, just change the line above this one and up to "^srcpath" to the following line:
#conddb dump $xmlhash >& tmp.xml

xml=tmp.xml

xmllines=`grep "<first>" $xml | sed 's/^.*<first>\(.*\)<\/first>*$/\1/g' | sed '/--/d'`
menulines=`grep "L1SeedsLogicalExpression" $menu | sed 's/^.*"\(.*\)".*$/\1/g'`

count=0

for line in $menulines ; do
    #echo $line
    if [[ $line == L1* ]]; then
        chk=0
        for seed in $xmllines ; do
            #echo "   $seed"
            if [ $line == $seed ]; then
                chk=1
                break
            fi
        done
        if [ $chk -eq 0 ]; then
            echo "$line does not exist in L1 xml!!!"
            ((count++))
        fi
    fi
done
echo "Found $count instances in $menu of an L1 seed which is not present in L1 xml from payload hash $xmlhash"
echo " "
rm tmp.xml
