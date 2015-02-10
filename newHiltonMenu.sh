#!/bin/bash

#Usage: This script takes an HLT menu in ORCOFF as argument and changes the menu on the Hilton. 
#       It assumes that the HLT browser is currently not broken (if you get a menu without the 
#       name in the heading, check the browser).
#       It also assumes that the test_hlt_config1 in /etc/hltd.conf is set to 
#       python/HiltonMenu.py. If this is not the case, you will need to change it by hand.

if [ "$#" -ne 1 ]; then
    echo "Need exactly one argument: the menu in ORCOFF ConfDB"
    return 1
fi

if [[ -z "$CMSSW_VERSION" ]]; then
    echo "You need to do cmsenv first"
    return 1
fi

menu=$1

edmConfigFromDB --orcoff --configName $menu > tempHLT.py
python /nfshome0/hltpro/scripts/onlineConverterHilton.py tempHLT.py tempHLTOnlineConverted.py
sudo cp tempHLTOnlineConverted.py /opt/hltd/python/HiltonMenu.py
rm tempHLT.py tempHLTOnlineConverted.py

echo "HLTD Config:"
cat /etc/hltd.conf | grep test_hlt_config1
echo "Heading of /opt/hltd/python/HiltonMenu.py:"
head -1 /opt/hltd/python/HiltonMenu.py

