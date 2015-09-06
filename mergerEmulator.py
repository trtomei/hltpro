#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time, sys, getopt, fcntl, random
import shutil
import json
import glob
import multiprocessing
from multiprocessing.pool import ThreadPool
import thread
import datetime
import fileinput
import socket
import filecmp
import zlib

#Input parameters -- must change these before using!
outDir = '/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/temp/macroMerged/run251643'
runDir = '/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/temp/run251643_DQMHiltonTest'


#Function for reading JSON files borrowed from merger code
def readJsonFile(inputJsonFile):
   try:
      settingsLS = "bad"
      if(os.path.getsize(inputJsonFile) > 0):
         try:
            settings_textI = open(inputJsonFile, "r").read()
            settingsLS = json.loads(settings_textI)
         except Exception, e:
             print "Failed to load JSON file:"
             print inputJsonFile

      return settingsLS
   except Exception, e:
       print "Failed to load JSON file:"
       print inputJsonFile

#End readJsonFile function-------------------------------------------

# Get list of unique streams
streams = [ ]
inis    = [ ]
inputInis = glob.glob(runDir+'/*ini')

for ini in inputInis:
    iniNameString = ini.replace(runDir,"").replace("/","").split('_')
    
    unique = True
    for stream in streams:
        if (stream == iniNameString[2]):
            unique = False
            break
    if (unique):
        streams.append(iniNameString[2])
        inis.append(ini)

#Get list of unique lumi sections
lumis = [ ]
inputJsns = glob.glob(runDir+'/*jsn')

for jsn in inputJsns:
   if (jsn.endswith('_BoLS.jsn') or '_EoR_' in jsn): continue

   jsnNameString = jsn.replace(runDir,"").replace("/","").split('_')

   unique = True
   for lumi in lumis:
      if (lumi == jsnNameString[1]):
         unique = False
         break
   if (unique):
      lumis.append(jsnNameString[1])

dictStreamIni = dict(zip(streams, inis))
         
#Loop over lumi sections, then streams
for lumi in lumis:
   for stream in streams:
      specialStreams = False
      if (stream == "streamDQMHistograms" or stream == "streamHLTRates" or stream == "streamL1Rates"):
         specialStreams = True  

      #First, edit and merge the JSON files
      inputJsns = glob.glob(runDir+'/*'+lumi+'_'+stream+'_*jsn')

      eventsInput       = 0
      eventsOutput      = 0
      errorCode         = 0
      fileName          = ""
      fileErrorString   = None
      fileSize          = 0
      nFilesBU          = 0
      checkSum          = 0
      nLostEvents       = 0
      transferDest      = "dummy"


      for jsn in inputJsns:
         if (jsn.endswith('_BoLS.jsn') or '_EoR_' in jsn): continue

         settings = readJsonFile(jsn)
         if("bad" in settings): continue

         eventsInput       += int(settings['data'][0])
         eventsOutput      += int(settings['data'][1])
         errorCode         += int(settings['data'][3]) #These should all be 0 anyway
         fileSize          += int(settings['data'][5])
         nFilesBU          += 1
         transferDest       = str(settings['data'][8]) #These should all be the same so I take the last one

         #There is no zlibextras on the Hilton. Hopefully, nobody actually cares about this checksum
#         checkSum           = zlibextras.adler32_combine(settings['data'][7], checkSum, fileSize) #Order matters here: checksum before file size
         checkSum          += int(settings['data'][7])

         #These should all be the same so take the last one
         jsnNameString = jsn.replace(runDir,"").replace("/","").split('_')
         fileName      = jsnNameString[0]+"_"+jsnNameString[1]+"_"+jsnNameString[2]+"_"

      suffix = 'StorageManager'
      if ('DQM' in stream): suffix = 'mrg-c2f12-23-01'
      fileName += suffix

      outJsnPath = outDir + '/' + fileName + '.jsn'

      extension = '.dat'
      if   (stream == "streamDQMHistograms"): extension = '.pb'
      elif ('Rates' in stream):               extension = '.jsndata' 

      fileName += extension
         
      theMergedJSONfile = open(outJsnPath, 'w')
      theMergedJSONfile.write(json.dumps({'data': (eventsInput, eventsOutput, errorCode, fileName, fileSize, checkSum, nFilesBU, eventsInput, nLostEvents, transferDest)}))
      theMergedJSONfile.close()         

      if (specialStreams == False):
         ini = dictStreamIni[stream]
         inputDats = glob.glob(runDir+'/*'+lumi+'_'+stream+'_*dat')

         fout = outDir + '/' + fileName

         ofile = open(fout,'w')

         if (os.path.exists(ini)):
            ifile = open(ini,'r')
            shutil.copyfileobj(ifile, ofile)
            ifile.close()
         else:
            print "Lost the ini file! "
            print ini

         for dat in inputDats:
            if (os.path.exists(dat)):
               dfile = open(dat,'r') 
               shutil.copyfileobj(dfile, ofile)
               dfile.close()

         ofile.close()

      elif (stream == "streamDQMHistograms"):
         outMergedFileFullPath = outDir + '/' + fileName
         msg = "fastHadd add -j 7 -o %s " % (outMergedFileFullPath)

         inputPbs = glob.glob(runDir+'/*'+lumi+'_'+stream+'_*pb')
         for pb in inputPbs: msg = msg + pb + " "

         os.system(msg)

