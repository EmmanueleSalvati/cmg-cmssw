import FWCore.ParameterSet.Config as cms

from CMGTools.Razor.objects.trackIsolationMaker_cfi import trackIsolationMaker

##################################
## Isolated Track Veto, hadronic##
##################################

razorTrackIsolationMaker = trackIsolationMaker.clone()
razorTrackIsolationMaker.minPt_cmgCandidate = cms.double(10.0)
razorTrackIsolationMaker.cmgCandidatesTag = cms.InputTag("cmgCandidates")
razorTrackIsolationMaker.vetoCollections = cms.VInputTag()

##################################
## Isolated Track veto, leptonic##
##################################

##muons
from CMGTools.Common.skims.leadingCMGMuonSelector_cfi import *
razorTightMuonLead = leadingCMGMuonSelector.clone(
    inputCollection = 'razorTightMuon',
    index = 1
    )

##electrons
from CMGTools.Common.skims.leadingCMGElectronSelector_cfi import *
razorTightElectronLead = leadingCMGElectronSelector.clone(
            inputCollection = 'razorTightElectron',
            index = 1
            )

razorLeptonTrackIsolationMaker                   = razorTrackIsolationMaker.clone()
razorLeptonTrackIsolationMaker.vetoCollections   = cms.VInputTag(
    cms.InputTag("razorTightMuonLead"),
    cms.InputTag("razorTightElectronLead")
    )

###########################
##iso track veto sequence##
###########################
isoTrackVetoSequence = cms.Sequence(
    razorTrackIsolationMaker      +
    razorTightMuonLead            +
    razorTightElectronLead        +
    razorLeptonTrackIsolationMaker
    )
