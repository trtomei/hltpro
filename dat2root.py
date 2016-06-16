import FWCore.ParameterSet.Config as cms

process = cms.Process("LHCX")

process.source = cms.Source("NewEventStreamFileReader",
                            fileNames = cms.untracked.vstring('file:/tmp/avetisya/run273450/streamPhysicsEGammaCommissioning/data/run273450_ls0065_streamPhysicsEGammaCommissioning_StorageManager.dat')
                            )

process.output = cms.OutputModule( "PoolOutputModule",
                                   fileName = cms.untracked.string( "Run273450_ls0065_PhysicsEGammaCommissioning_test.root" )
)

process.end = cms.EndPath( process.output ) 
