import FWCore.ParameterSet.Config as cms

process = cms.Process("CMA")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
        "/store/data/Commissioning2014/MinimumBias/RAW/v3/000/229/713/00000/B2097415-5B6A-E411-BE85-02163E010DBC.root",
        "/store/data/Commissioning2014/MinimumBias/RAW/v3/000/229/713/00000/F2AEE60D-5B6A-E411-A19F-02163E010CFA.root"
        ),
                            lumisToProcess = cms.untracked.VLuminosityBlockRange('229713:1-229713:10'),
                            skipEvents = cms.untracked.uint32(0),
                            dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
                            inputCommands=cms.untracked.vstring(
        "drop *",
        "keep *_TriggerResults_*_HLT",
        "keep *_hltL1GtObjectMap_*_*",
        "keep *_hltTriggerSummaryAOD_*_HLT",
        "keep *_rawDataCollector_*_*"
        )
                            );

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('Commissioning2014_Run229713_MinimumBias.root'),
                               outputCommands = cms.untracked.vstring(
        "drop *",
        "keep *_TriggerResults_*_HLT",
        "keep *_hltL1GtObjectMap_*_*",
        "keep *_hltTriggerSummaryAOD_*_HLT",
        "keep *_rawDataCollector_*_*"
));

process.myEndPath = cms.EndPath(process.out)
        
