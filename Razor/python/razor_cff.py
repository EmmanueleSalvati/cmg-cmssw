import FWCore.ParameterSet.Config as cms

###########
##Trigger##
###########
from CMGTools.Razor.objects.razorTrigger_cff import *

####################
##Leptonic objects##
####################

##############
#Muons
from CMGTools.Razor.objects.razorMuon_cff import *

##############
#Electrons
from CMGTools.Razor.objects.razorElectron_cff import *

#################
#Iso Track Veto
from CMGTools.Razor.objects.isoTrackVeto_cff import *

razorLeptonSequence = cms.Sequence(
    razorMuonSequence         +
    razorElectronSequence     +
    isoTrackVetoSequence
    )


####################
##Hadronic objects##
####################

##############
#Jets
from CMGTools.Razor.objects.razorJet_cff import *

##############
#Hemispheres
from CMGTools.Razor.objects.razorHemisphere_cff import *

########################
#Generator information##
########################
#later. Just keep the proper event content

###########
##Filters##
###########
from CMGTools.Razor.skims.filters_cfi import razorJetCleanedCount
from CMGTools.Razor.objects.razorCleaning_cff import razorCleaning

##################
##Final Sequence##
##################



razorObjectSequence = cms.Sequence(
    razorCleaning            +
    razorTriggerSequence     +
    razorLeptonSequence      +
    razorJetSequence         +
    razorJetCleanedCount     +
    razorHemisphereSequence
    )

#razorSkimSequence = cms.Seuqnce
