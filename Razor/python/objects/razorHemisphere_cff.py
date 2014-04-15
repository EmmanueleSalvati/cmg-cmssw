import FWCore.ParameterSet.Config as cms

from CMGTools.Razor.skims.razorJetSkim_cfi      import *
from CMGTools.Razor.objects.razorHemisphere_cfi import *

############
##Hadronic##
############
razorHadHemisphereSequence = cms.Sequence(
    ~razorPFJetSelCount  +
    razorHemiHadBox      +
    razorDiHemiHadBox    +
    razorDiHemiHadBoxSel 
    )



############
##Leptonic##
############
razorLepHemisphereSequence = cms.Sequence(
    ~razorPFJetSelCount  +
    razorHemiLepBox      +
    razorDiHemiLepBox    +
    razorDiHemiLepBoxSel 
    )

############
##Sequence##
############
razorHemisphereSequence = cms.Sequence(
    razorHadHemisphereSequence +
    razorLepHemisphereSequence
    )

