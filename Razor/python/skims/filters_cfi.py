import FWCore.ParameterSet.Config as cms

from CMGTools.Common.skims.cmgCandCount_cfi import *

razorJetCleanedCount = cmgCandCount.clone(
    src = 'razorJet',
    minNumber = 1
    ) #filter inverted later
