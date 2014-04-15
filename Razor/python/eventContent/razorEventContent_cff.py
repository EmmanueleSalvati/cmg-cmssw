import FWCore.ParameterSet.Config as cms

razorEventContent = cms.untracked.vstring(
    'drop *',
    'keep *_offlinePrimaryVertices_*_*',
    'keep *_*_*_RZR',
    'keep *_TriggerResults_*_PAT',
    'keep *_source_*_*',
    'keep *_cmgPFMET_*_*',
    )
