#! /bin/bash

#Usage: This script takes two inputs: The HLT menu python file and a global tag.
#       It then checks that every instance of "L1SeedsLogicalExpression" in the HLT menu
#       matches to an algorithm name in the L1 xml from the latest IOV in the global tag.
#       If the HLTL1TSeed module L1Seed parameter name changes or the L1 xml format changes,
#       the script will need to be updated.

if [ "$#" -ne 2 ]; then
    echo "Need exactly two arguments: (1) the HLT menu python and (2) a global tag"
    exit 1
fi

if [[ -z "$CMSSW_VERSION" ]]; then
    echo "You need to do cmsenv first"
    exit 1
fi

#can get GT from menu with:
#   grep "globaltag" /opt/hltd/python/HiltonMenu.py | sed 's/.*"\(.*\)".*$/\1/g'

menu=$1
gt=$2

tagname=`conddb --db "oracle+frontier://@frontier%3A%2F%2F%28proxyurl%3Dhttp%3A%2F%2Flocalhost%3A3128%29%28serverurl%3Dhttp%3A%2F%2Flocalhost%3A8000%2FFrontierOnProd%29%28serverurl%3Dhttp%3A%2F%2Flocalhost%3A8000%2FFrontierOnProd%29%28retrieve%2Dziplevel%3D0%29/CMS_CONDITIONS" list $gt 2> /dev/null | grep "L1TUtmTriggerMenuRcd" | sed 's/ *$//g' | sed 's/^.* //g'`
xmlhash=`conddb --db "oracle+frontier://@frontier%3A%2F%2F%28proxyurl%3Dhttp%3A%2F%2Flocalhost%3A3128%29%28serverurl%3Dhttp%3A%2F%2Flocalhost%3A8000%2FFrontierOnProd%29%28serverurl%3Dhttp%3A%2F%2Flocalhost%3A8000%2FFrontierOnProd%29%28retrieve%2Dziplevel%3D0%29/CMS_CONDITIONS" list $tagname  2> /dev/null | tail -n 2 | head -n 1 | sed 's/^.*  \(.*\)  L1TUtmTriggerMenu/\1/g'`
#this is taken from the connect string in the HLT menu, but I had to convert the symbols to hex manually, hopefully the connect string never changes...

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
cp `type -p conddb` ../bin/$SCRAM_ARCH/
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
#You can run this script offline, just change the line above this one and up to "^tagname" to the following 3 lines:
#tagname=`conddb list $gt | grep "L1TUtmTriggerMenuRcd" | sed 's/ *$//g' | sed 's/^.* //g'`
#xmlhash=`conddb list $tagname | tail -n 2 | head -n 1 | sed 's/^.*  \(.*\)  L1TUtmTriggerMenu/\1/g'`
#conddb dump $xmlhash >& tmp.xml

xml=tmp.xml

xmllines=`grep "<first>" $xml | sed 's/^.*<first>\(.*\)<\/first>*$/\1/g' | sed '/--/d'`
menulines=`grep "L1SeedsLogicalExpression" $menu | sed 's/^.*"\(.*\)".*$/\1/g'`

count=0

for line in $menulines ; do
    #echo $line
    # Remove spurious symbols from L1 seed names, like parenthesis
    correctedLine="$(echo $line | sed 's/)//g' | sed 's/(//g')"
    line="$correctedLine"
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
echo "Found $count instances in $menu of an L1 seed which is not present in Global Tag $gt"
echo " "
rm tmp.xml
