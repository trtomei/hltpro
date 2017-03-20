#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

#Input parameters -- must change these before using!
runNumber = '274442'
mergedDir = '/tmp/avetisya/MacroMergeOutput/run'+runNumber
dqmDir    = '/fff/BU0/output/playback_files/run'+runNumber

#Change the list of streams if necessary
#Interesting streams are typically DQM, DQMHistograms and sometimes DQMCalibration
streams = ['DQM', 'DQMHistograms']

#List of lumi sections; change if necessary
lumis = range(1,5)

for lumi in lumis:
    lumiString = "{0:0>4}".format(lumi)
    for stream in streams:
        os.system('cp '+mergedDir+'/stream'+stream+'/data/*ls'+lumiString+'* '+dqmDir)

    for stream in streams:
        os.system('cp '+mergedDir+'/stream'+stream+'/jsns/*ls'+lumiString+'*_mrg* '+dqmDir)

    #Change this time if it is too short to process the data
    if lumi == 1: os.system('sleep 20')
    else:         os.system('sleep 15')

os.system('cp '+mergedDir+'/*EoR*jsn '+dqmDir)

