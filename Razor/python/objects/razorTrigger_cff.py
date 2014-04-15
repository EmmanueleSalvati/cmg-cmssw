import FWCore.ParameterSet.Config as cms

from CMGTools.Common.skims.cmgTriggerObjectSel_cfi import *

############
##Hadronic##
############
razorHadronicTrigger = cmgTriggerObjectSel.clone(
    src = 'cmgTriggerObjectSel',
    cut = 'getSelectionRegExp("^HLT_DiJet[0-9]+_DiJet[0-9]+_DiJet[0-9]+.*_v[0-9]+$") ||'\
    '  getSelectionRegExp("^HLT_QuadJet[0-9]+_DiJet[0-9]+.*_v[0-9]+$") ||'\
    '  getSelectionRegExp("^HLT_QuadJet[0-9]+_v[0-9]+$") ||'\
    '  getSelectionRegExp("^HLT_QuadJet[0-9]+_L1FastJet_v[0-9]+$") ||'\
    '  getSelectionRegExp("^HLT_SixJet[0-9]+.*_v[0-9]+$")'
    )


############
##Mu      ##
############
razorMuTrigger = cmgTriggerObjectSel.clone(
    src = 'cmgTriggerObjectSel',
    cut = 'getSelectionRegExp("^HLT_Mu[0-9]+_eta2p1_v[0-9]+$") ||'\
    'getSelectionRegExp("^HLT_Mu[0-9]+_v[0-9]+$") ||'\
    'getSelectionRegExp("^HLT_IsoMu[0-9]+_v[0-9]+$") ||'\
    'getSelectionRegExp("^HLT_IsoMu[0-9]+_eta2p1_v[0-9]+$")'
    )


#############
##Electrons##
#############
razorEleTrigger = cmgTriggerObjectSel.clone(
    src = 'cmgTriggerObjectSel',
    cut = 'getSelectionRegExp("^HLT_Ele[0-9]+_WP80_v[0-9]+$")'
    )

#############
##Sequence ##
#############
razorTriggerSequence = cms.Sequence(
    razorHadronicTrigger +
    razorMuTrigger       +
    razorEleTrigger
    ) 
