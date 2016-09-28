#!/bin/bash

nTot=`grep -c processor /proc/cpuinfo`
n=$nTot

#Second statement is a requirement that the argument be a positive integer
if [[ $# -eq 1 && $1 =~ [0-9]+$ ]]; then
n=$1
fi

#Quarantine all cores
sudo mv /etc/appliance/resources/idle/core* /etc/appliance/resources/quarantined/

for i in `seq 1 $n`; do
if [[ $i -gt $nTot ]]; then
echo This machine only has $nTot cores
n=$nTot
break
fi
#Hyperthreaded cores are paired so start with the even ones
if [[ $i -le $(( $nTot/2 )) ]]; then
iCore=$(( ($i - 1)*2 ))
#If asked for more than nTot/2 cores, use hyperthreading
else
iCore=$(( ($i - 1 - $nTot/2)*2 + 1 ))
fi
sudo mv /etc/appliance/resources/quarantined/core${iCore} /etc/appliance/resources/idle/
done

echo Hilton will run hltd with $n cores