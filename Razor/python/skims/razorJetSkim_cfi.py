import FWCore.ParameterSet.Config as cms

from CMGTools.Common.skims.cmgCandCount_cfi import *

#protection
razorPFJetSelCount = cmgCandCount.clone(
    src = 'cmgPFJetSelCHS',
    minNumber = 20
    )

############
##Hadronic##
############
razorJetCount =  cmgCandCount.clone(
    src = 'razorJet',
    minNumber = 6
    )

############
##Leptonic##
############
razorJetNoLeptonCount =  cmgCandCount.clone(
    src = 'razorJetNoLepton',
    minNumber = 4
    )



