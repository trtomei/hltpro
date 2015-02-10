#!/bin/bash

n=16

#Second statement is a requirement that the argument be a positive integer
if [[ $# -eq 1 && $1 =~ [0-9]+$ ]]; then
n=$1
fi

#Quarantine all cores
sudo mv /etc/appliance/resources/idle/core* /etc/appliance/resources/quarantined/

for i in `seq 1 $n`; do
if [[ $i -ge 32 ]]; then
echo This machine only has 32 cores
n=32
break
fi
#Hyperthreaded cores are paired so start with the even ones
if [[ $i -le 16 ]]; then
iCore=$(( ($i - 1)*2 ))
#If asked for more than 16 cores, use hyperthreading
else
iCore=$(( ($i - 17)*2 + 1 ))
fi
sudo mv /etc/appliance/resources/quarantined/core${iCore} /etc/appliance/resources/idle/
done

echo Hilton will run hltd with $n cores