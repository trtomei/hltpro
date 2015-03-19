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

echo "dumping $menu from ConfDB v1..."
/nfshome0/hltpro/scripts/hltConfigFromDB --v1 --daq --configName $menu > confdb_v1.py
echo "dumping $menu from ConfDB v2..."
/nfshome0/hltpro/scripts/hltConfigFromDB --v2 --gdr --configName $menu > confdb_v2.py

# check that v1 and v2 databases give the same HLT menu
echo "comparing dumps"
if
    # use -B to ignore blank lines
    # do not use -b/-w for python files
    diff -q -B confdb_v1.py confdb_v2.py > /dev/null
then
    mv confdb_v2.py hlt.py
    rm confdb_v1.py
else
    echo "Error: $menu is different between ConfDB v1 and v2"
    diff -u -B confdb_v1.py confdb_v2.py
    exit 1
fi

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

echo "HLTD config:"
cat /etc/hltd.conf | grep test_hlt_config1
echo "heading of /opt/hltd/python/HiltonMenu.py:"
head -1 /opt/hltd/python/HiltonMenu.py

