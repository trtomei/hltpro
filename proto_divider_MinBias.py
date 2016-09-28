import FWCore.ParameterSet.Config as cms

process = cms.Process("CMA")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
        #"file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/temp/Collisions_HIL1_Run261622_HIVirginRawPD.root"
        #"file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015D_L1REPACK_ZeroBias2.root"
        'file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Commissioning2016_Run267375_MinimumBias_L1REPACK.root'
#        "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/temp/Collisions_ppRefL1_Run261544_MinBiasPD.root"
#        "/store/data/Commissioning2014/MinimumBias/RAW/v3/000/229/713/00000/B2097415-5B6A-E411-BE85-02163E010DBC.root",
#        "/store/data/Commissioning2014/MinimumBias/RAW/v3/000/229/713/00000/F2AEE60D-5B6A-E411-A19F-02163E010CFA.root"
#        "//cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Commissioning2015_241422_MinimumBias_1to20.root",
#        "file:/tmp/hiltonTest.root",        
#        "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248558_MinimumBias_LS318to340_tmp.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_DoubleEG_TMP.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_DoubleMuonLowMass_TMP.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_DoubleMuon_TMP.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_HTMHT_TMP.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_JetHT_TMP.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_MET_TMP.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_MuOnia_TMP.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_MuonEG_TMP.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_NoBPTX_TMP.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_SingleElectron_TMP.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_SingleMuon_TMP.root",
        # "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015A_Run248038_SinglePhoton_TMP.root",
#        "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015B_Run251562_SingleElectron1.root",
#        "file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Run2015B_Run251562_SingleElectron2.root"
        ),
                            lumisToProcess = cms.untracked.VLuminosityBlockRange('267375:0-267375:99999'),
                            skipEvents = cms.untracked.uint32(0),
                            dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
                            inputCommands=cms.untracked.vstring(
        "drop *",
        "keep *_TriggerResults_*_HLT",
        "keep *_hltL1GtObjectMap_*_*",
        "keep *_hltTriggerSummaryAOD_*_HLT",
        #"keep *_rawDataCollector_*_*"
        "keep *_rawDataCollector_*_L1REPACK"
        )
                            );

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('file:/cmsnfshltdata/hltdata/TSG/FUVAL_INPUT_FILES/Commissioning2016_MinimumBiasrun267375_L1REPACK.root'),
                               outputCommands = cms.untracked.vstring(
        "drop *",
        "keep *_TriggerResults_*_HLT",
        "keep *_hltL1GtObjectMap_*_*",
        "keep *_hltTriggerSummaryAOD_*_HLT",
        #"keep *_rawDataCollector_*_*"
        "keep *_rawDataCollector_*_L1REPACK"
));

process.myEndPath = cms.EndPath(process.out)
        
