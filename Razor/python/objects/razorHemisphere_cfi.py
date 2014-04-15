import FWCore.ParameterSet.Config as cms

from CMGTools.Common.factories.cmgHemi_cfi   import cmgHemi
from CMGTools.Common.factories.cmgDiHemi_cfi import cmgDiHemi
from CMGTools.Common.skims.cmgCandSel_cfi    import cmgCandSel

############
##Hadronic##
############
razorHemiHadBox = cmgHemi.clone(
    cfg = cmgHemi.cfg.clone(
    inputCollection = cms.VInputTag(
    cms.InputTag("razorJet")
    ),
    balanceAlgorithm = cms.uint32(1),#use the MassBalance algo
    maxCand = cms.uint32(50),
    minObjectsPerHemi0 = cms.untracked.uint32(3),
    minObjectsPerHemi1 = cms.untracked.uint32(3),
    )
)

razorDiHemiHadBox = cmgDiHemi.clone(
    cfg = cmgDiHemi.cfg.clone(
    leg1Collection = cms.InputTag('razorHemiHadBox'),
    leg2Collection = cms.InputTag('razorHemiHadBox'),
    metCollection = cms.InputTag('cmgPFMET')
    ),
    cuts = cms.PSet(
    razor = cms.PSet(
          mr = cms.string('mR() >= 0'),    #mR is computed in CMGTools/Common/interface/DiObjectFactory.h
          rsq = cms.string('Rsq() >= 0.0')
          )
    )
)

razorDiHemiHadBoxSel = cmgCandSel.clone(
    src = 'razorDiHemiHadBox',
    cut = 'getSelection("cuts_razor")'
    )


############
##Leptonic##
############
razorHemiLepBox = razorHemiHadBox.clone()
razorHemiLepBox.cfg.minObjectsPerHemi0 = cms.untracked.uint32(0)
razorHemiLepBox.cfg.minObjectsPerHemi1 = cms.untracked.uint32(0)

razorDiHemiLepBox = cmgDiHemi.clone(
    cfg = cmgDiHemi.cfg.clone(
    leg1Collection = cms.InputTag('razorHemiLepBox'),
    leg2Collection = cms.InputTag('razorHemiLepBox'),
    metCollection = cms.InputTag('cmgPFMET')
    ),
    cuts = cms.PSet(
    razor = cms.PSet(
          mr = cms.string('mR() >= 0'),
          rsq = cms.string('Rsq() >= 0.0')
          )
    )
)

razorDiHemiLepBoxSel = cmgCandSel.clone(
    src = 'razorDiHemiLepBox',
    cut = 'getSelection("cuts_razor")'
    )


