import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import os

options = VarParsing.VarParsing ('analysis')
cmsswbase = os.path.expandvars('$CMSSW_BASE/')

options.register ('runNumber',
                  233238, ##Default value: run with tracker from MWGR10
                  #229713, ##Old magnet run from 2014
                  #227451,  ##Even older run from 2014
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "Run Number")

options.register ('buBaseDir',
                  '/bu/', # default value
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,          # string, int, or float
                  "BU base directory")

options.register ('dataDir',
                  '/fff/BU0/ramdisk', # default value (on standalone FU)
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,          # string, int, or float
                  "BU data write directory")

options.parseArguments()

process = cms.Process("FAKEBU")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

process.options = cms.untracked.PSet(
    multiProcesses = cms.untracked.PSet(
    maxChildProcesses = cms.untracked.int32(0)
    )
)

process.MessageLogger = cms.Service("MessageLogger",
                                    destinations = cms.untracked.vstring( 'cout' ),
                                    cout = cms.untracked.PSet(
    FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(100),
    optionalPSet = cms.untracked.bool(True),
    #limit = cms.untracked.int32(10000000)
    ),
    threshold = cms.untracked.string( "INFO" ),
    )
)

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
        'file:/hltdata/TSG/FUVAL_INPUT_FILES/Commissioning2015_Run233238_Cosmics.root'
        #'file:/hltdata/TSG/FUVAL_INPUT_FILES/Commissioning2014_Run229713_Cosmics.root'
        #'file:/hltdata/TSG/FUVAL_INPUT_FILES/Commissioning2014_Run227451_Cosmics.root'
        ),
                            skipEvents = cms.untracked.uint32(0)
                            );

process.EvFDaqDirector = cms.Service("EvFDaqDirector",
                                     runNumber= cms.untracked.uint32(options.runNumber),
                                     baseDir = cms.untracked.string(options.dataDir),
                                     buBaseDir = cms.untracked.string("/fff/BU0/data"),
                                     directorIsBu = cms.untracked.bool(True),
                                     #obsolete:
                                     hltBaseDir = cms.untracked.string("/fff/BU0/ramdisk"),
                                     smBaseDir  = cms.untracked.string("/fff/BU0/ramdisk"),
                                     slaveResources = cms.untracked.vstring('dvfu-c2f37-38-01'),
                                     slavePathToData = cms.untracked.string("/fff/BU/ramdisk")
                                     )
#process.EvFBuildingThrottle = cms.Service("EvFBuildingThrottle",
#                                          highWaterMark = cms.untracked.double(0.90),
#                                          lowWaterMark = cms.untracked.double(0.45)
#                                          )

process.a = cms.EDAnalyzer("ExceptionGenerator",
                           defaultAction = cms.untracked.int32(0),
                           defaultQualifier = cms.untracked.int32(10)
                           )

process.out = cms.OutputModule("RawStreamFileWriterForBU",
                               ProductLabel = cms.untracked.string("rawDataCollector"),
                               numEventsPerFile = cms.untracked.uint32(400),
   			       jsonDefLocation = cms.untracked.string(cmsswbase+"/src/EventFilter/Utilities/plugins/budef.jsd"),
			       debug = cms.untracked.bool(True)
                               )

process.p = cms.Path(process.a)

process.ep = cms.EndPath(process.out)
