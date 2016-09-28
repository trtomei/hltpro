import FWCore.ParameterSet.Config as cms

process = cms.Process("LHC")

process.source = cms.Source("ErrorStreamSource",
                            fileNames = cms.untracked.vstring(
        'file:/store/error_stream/run278509/run278509_ls0652_index000178_fu-c2d36-12-01_pid154239.raw'
#'file:/cmsnfshltdata/hltdata/TSG/ErrorStream/run277096/run277096_ls0423_index000118_fu-c2e45-32-03_pid105476.raw',
#'file:/cmsnfshltdata/hltdata/TSG/ErrorStream/run277127/run277127_ls0252_index000018_fu-c2d46-34-02_pid172512.raw',
#'file:/hltdata/TSG/FUVAL_INPUT_FILES/temp/run278346_ls0117_index000265_fu-c2d31-12-01_pid82053.raw',
#'file:/nfshome0/gesmith/run278346_ls0117_index000150_fu-c2e35-26-02_pid63007.raw',
#        'file:/cmsnfshltdata/hltdata/TSG/ErrorStream/run276870/run276870_ls1956_index000155_fu-c2e31-26-03_pid107412.raw',
#        'file:/cmsnfshltdata/hltdata/TSG/ErrorStream/run276870/run276870_ls1964_index000106_fu-c2e35-36-04_pid103629.raw',
#        'file:/cmsnfshltdata/hltdata/TSG/ErrorStream/run276870/run276870_ls1972_index000039_fu-c2d33-24-04_pid135358.raw',
#        'file:/cmsnfshltdata/hltdata/TSG/ErrorStream/run276870/run276870_ls1972_index000057_fu-c2e46-12-01_pid108145.raw',
        ),
                            firstRun  = cms.untracked.uint32(278509)
                            )


from EventFilter.RawDataCollector.rawDataCollectorByLabel_cfi import rawDataCollector
process.rawDataCollector = rawDataCollector.clone(
        verbose = cms.untracked.int32(0),
            RawCollectionList = cms.VInputTag( cms.InputTag('source') )
        )

process.output = cms.OutputModule( "PoolOutputModule",
                                   #fileName = cms.untracked.string( "Run252488_ls1482_streamError_bu-c2e18-39-01.root" ),
#                                   fileName = cms.untracked.string( "Run276870_ls39_155_ErrorStream_RAW.root" ),
                                   fileName = cms.untracked.string( "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/temp/Run278509_ls0652_fu-c2e36-12-01_pid154239_ErrorStream_RAW.root" ),
                                   outputCommands = cms.untracked.vstring(
                                                                          'drop *',
                                                                          'keep *_rawDataCollector_*_*'
                                   )
)

process.raw = cms.Path( process.rawDataCollector )
process.end = cms.EndPath( process.output ) 
