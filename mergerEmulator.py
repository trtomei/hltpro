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
runNumber = '274442'
runDir = '/fff/BU0/output/run'+runNumber      
outDir = '/tmp/avetisya/MacroMergeOutput/run'+runNumber

if (not os.path.exists(outDir)):
   print "Output directory" + outDir + "does not exist!"
   exit

if (not os.path.exists(runDir)):
   print "Input directory" + runDir + "does not exist!"
   exit

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

#Copy the End-of-Run file
os.system('cp '+runDir+'/*EoR*jsn '+outDir)

#Loop over streams
streamPaths = glob.glob(runDir+'/stream*')

for streamPath in streamPaths:
   streamName = streamPath.replace(runDir,"").replace("/","")

   if (not os.path.exists(outDir+"/"+streamName)):
      os.mkdir(outDir+"/"+streamName)

   if (not os.path.exists(outDir+"/"+streamName+"/jsns")):
      os.mkdir(outDir+"/"+streamName+"/jsns")

   if (not os.path.exists(outDir+"/"+streamName+"/data")):
      os.mkdir(outDir+"/"+streamName+"/data")
      
   #Get list of unique lumi sections
   lumis = [ ]
   jsnPath = streamPath+"/jsns"
   inputJsns = glob.glob(jsnPath+'/*jsn')

   for jsn in inputJsns:
      if (jsn.endswith('_BoLS.jsn') or '_EoR_' in jsn): continue

      jsnNameString = jsn.replace(jsnPath,"").replace("/","").split('_')

      unique = True
      for lumi in lumis:
         if (lumi == jsnNameString[1]):
            unique = False
            break
      if (unique):
         lumis.append(jsnNameString[1])

   #Loop over lumi sections
   for lumi in lumis:
      specialStreams = False
      if (streamName == "streamDQMHistograms" or streamName == "streamHLTRates" or streamName == "streamL1Rates"):
         specialStreams = True  
         
      #First, edit and merge the JSON files
      inputJsns = glob.glob(jsnPath+'/*'+lumi+'_'+streamName+'_*jsn')

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
         if (jsn.endswith('_BoLS.jsn') or '_EoR_' in jsn):
            outJsnPath = outDir + '/' + streamName + '/jsns/'
            os.system('cp '+jsn+' '+outJsnPath)
            continue

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
         jsnNameString = jsn.replace(jsnPath,"").replace("/","").split('_')
         fileName      = jsnNameString[0]+"_"+jsnNameString[1]+"_"+jsnNameString[2]+"_"

      suffix = 'StorageManager'
      if ('DQM' in streamName): suffix = 'mrg-c2f12-23-01'
      fileName += suffix

      outJsnPath = outDir + '/' + streamName + '/jsns/' + fileName + '.jsn'

      extension = '.dat'
      if   (streamName == "streamDQMHistograms"): extension = '.pb'
      elif ('Rates' in streamName):               extension = '.jsndata' 

      fileName += extension
         
      theMergedJSONfile = open(outJsnPath, 'w')
      theMergedJSONfile.write(json.dumps({'data': (eventsInput, eventsOutput, errorCode, fileName, fileSize, checkSum, nFilesBU, eventsInput, nLostEvents, transferDest)}))
      theMergedJSONfile.close()         

      dataPath = streamPath+"/data"
      inis = glob.glob(dataPath+'/*ini')

      if (len(inis) == 0):
         continue

      if (specialStreams == False):
         ini  = inis[0]            

         inputDats = glob.glob(dataPath+'/*'+lumi+'_'+streamName+'_*dat')

         if (len(inputDats) == 0):
            continue

         fout = outDir + '/' + streamName + '/data/' + fileName

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

      elif (streamName == "streamDQMHistograms"):
         outMergedFileFullPath = outDir + "/" + streamName + '/data/' + fileName
         msg = "fastHadd add -j 7 -o %s " % (outMergedFileFullPath)

         inputPbs = glob.glob(dataPath+'/*'+lumi+'_'+streamName+'_*pb')

         if (len(inputPbs) == 0):
            continue

         for pb in inputPbs: msg = msg + pb + " "
         
         os.system(msg)

