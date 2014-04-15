import FWCore.ParameterSet.Config as cms

from CMGTools.Common.skims.cmgPFJetSel_cfi import *

############
##Hadronic##
############
razorJet = cmgPFJetSel.clone(
    src = 'cmgPFJetSelCHS',
    cut = 'pt()>=30 \
           && abs(eta)<=2.4'
    )

############
##Leptonic##
############
razorJetNoLepton = cms.EDProducer(
    "DeltaRVetoProducerPFJet",
    inputCollection = cms.InputTag('razorJet'),
    MatchingParams = cms.VPSet(
        cms.PSet(                                     
            vetoCollection=cms.InputTag("razorTightElectron"),
            minDeltaR=cms.double(0.4),
            removeMatchedObject=cms.bool(True)
            ),
        cms.PSet(                                     
            vetoCollection=cms.InputTag("razorTightMuon"),
            minDeltaR=cms.double(0.4),
            removeMatchedObject=cms.bool(True)
            )
        ),
    verbose = cms.untracked.bool(False)
    )

############
##Jet ID  ##
############
razorJetCleaned = cmgPFJetSel.clone(
    src = 'razorJet',
    cut = '(!getSelection("cuts_looseJetId"))'
    )


################
##Jet Sequence##
################
razorJetSequence = cms.Sequence(
    razorJet         +
    razorJetNoLepton +
    razorJetCleaned
    )

