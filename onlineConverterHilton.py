import sys

inputName  = 'ConfDBMenu.py'
outputName = 'OnlineMenu.py'

if len(sys.argv) > 1: inputName  = sys.argv[1]
if len(sys.argv) > 2: outputName = sys.argv[2]

f1 = open(inputName, 'r')
f2 = open(outputName, 'w')

for line in f1:
    f2.write(line)
f1.close()

f2.write('import FWCore.ParameterSet.VarParsing as VarParsing\n')
f2.write('import os\n')
f2.write('\n')
f2.write('cmsswbase = os.path.expandvars(\'$CMSSW_BASE/\')\n')
f2.write('\n')
f2.write('options = VarParsing.VarParsing (\'analysis\')\n')
f2.write('\n')
f2.write('options.register (\'runNumber\',\n')
f2.write('                  1, # default value\n')
f2.write('                  VarParsing.VarParsing.multiplicity.singleton,\n')
f2.write('                  VarParsing.VarParsing.varType.int,          # string, int, or float\n')
f2.write('                  "Run Number")\n')
f2.write('\n')
f2.write('options.register (\'buBaseDir\',\n')
f2.write('                  \'/fff/BU0\', # default value\n')
f2.write('                  VarParsing.VarParsing.multiplicity.singleton,\n')
f2.write('                  VarParsing.VarParsing.varType.string,          # string, int, or float\n')
f2.write('                  "BU base directory")\n')
f2.write('\n')
f2.write('options.register (\'dataDir\',\n')
f2.write('                  \'/fff/data\', # default value\n')
f2.write('                  VarParsing.VarParsing.multiplicity.singleton,\n')
f2.write('                  VarParsing.VarParsing.varType.string,          # string, int, or float\n')
f2.write('                  "FU data directory")\n')
f2.write('\n')
f2.write('options.register (\'numThreads\',\n')
f2.write('                  1, # default value\n')
f2.write('                  VarParsing.VarParsing.multiplicity.singleton,\n')
f2.write('                  VarParsing.VarParsing.varType.int,          # string, int, or float\n')
f2.write('                  "Number of CMSSW threads")\n')
f2.write('\n')
f2.write('options.register (\'numFwkStreams\',\n')
f2.write('                  1, # default value\n')
f2.write('                  VarParsing.VarParsing.multiplicity.singleton,\n')
f2.write('                  VarParsing.VarParsing.varType.int,          # string, int, or float\n')
f2.write('                  "Number of CMSSW streams")\n')
f2.write('\n')
f2.write('options.parseArguments()\n')
f2.write('\n')
f2.write('process.options = cms.untracked.PSet(\n')
f2.write('    numberOfThreads = cms.untracked.uint32(options.numThreads),\n')
f2.write('    numberOfStreams = cms.untracked.uint32(options.numFwkStreams),\n')
f2.write('    multiProcesses = cms.untracked.PSet(\n')
f2.write('    maxChildProcesses = cms.untracked.int32(0)\n')
f2.write('    )\n')
f2.write(')\n')
f2.write('\n')
f2.write('process.EvFDaqDirector.buBaseDir    = options.buBaseDir\n')
f2.write('process.EvFDaqDirector.baseDir      = options.dataDir\n')
f2.write('process.EvFDaqDirector.runNumber    = options.runNumber\n')


f2.close()

