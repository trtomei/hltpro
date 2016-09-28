#! /bin/bash

#Usage: This script takes an HLT menu in ORCOFF as argument and changes the menu on the Hilton. 
#       It assumes that the HLT browser is currently not broken (if you get a menu without the 
#       name in the heading, check the browser).
#       It also assumes that the test_hlt_config1 in /etc/hltd.conf is set to 
#       python/HiltonMenu.py. If this is not the case, you will need to change it by hand.

if [ "$#" -ne 1 ]; then
    echo "Need exactly one argument: the menu in ORCOFF ConfDB"
    exit 1
fi

if [[ -z "$CMSSW_VERSION" ]]; then
    echo "You need to do cmsenv first"
    exit 1
fi

menu=$1

echo "dumping $menu from ConfDB v2..."
/nfshome0/hltpro/scripts/hltConfigFromDB --v2 --gdr --configName $menu > hlt.py


# check for errors in the menu
echo "checking dump consistency, found HLT version:"
python -c 'from hlt import process; print "\t%s" % process.HLTConfigVersion.tableName.value();' || {
    echo "Error: found errors parsing the python dump in hlt.py"
    exit 1
}

# convert the hlt menu for online use in the hilton
echo "converting menu for use on hilton"
python /nfshome0/hltpro/scripts/onlineConverterHilton.py hlt.py hltConverted.py
sudo cp hltConverted.py /opt/hltd/python/HiltonMenu.py
rm -f hlt.py hltConverted.py

# run the menu checker script
echo "running MenuChecker.py"
python /nfshome0/hltpro/RateMon/MenuChecker.py $menu

gtag=`grep "globaltag" /opt/hltd/python/HiltonMenu.py | sed 's/.*"\(.*\)".*$/\1/g'`
echo "checking L1 seeds in HLT menu against L1 xml in global tag $gtag"
bash /nfshome0/hltpro/scripts/L1MenuCheck_FromGT.sh /opt/hltd/python/HiltonMenu.py $gtag
#I have to suppress the error output otherwise we get flooded with permissions errors from the release install.
#Unfortunately this makes debugging difficult in case things go wrong (and they will with this script).

echo "HLTD config:"
cat /etc/hltd.conf | grep test_hlt_config1
cat /etc/hltd.conf | grep cmssw_default_version
echo "heading of /opt/hltd/python/HiltonMenu.py:"
head -1 /opt/hltd/python/HiltonMenu.py

