import FWCore.ParameterSet.Config as cms

from CMGTools.Common.skims.cmgMuonSel_cfi import *

razorLooseMuon = cmgMuonSel.clone(
    src = "cmgMuonSel",
    cut = "(pt() > 5.) \
           && (abs(eta()) < 2.4) \
           && sourcePtr().userFloat('isLooseLeptonSAK')"#hard-coded SAK...CMGTools.Common.interface, src & plugins
    )

razorTightMuon = cmgMuonSel.clone(
    src = "cmgMuonSel",
    cut = "(pt() > 25.) \
           && (abs(eta()) < 2.4) \
           && relIso(0.5) < 0.15 \
           && getSelection('cuts_tightmuonNoVtx') \
           && abs(dxy()) < 0.02 \
           && abs(dz()) < 0.5"
    )
#relIso : AnalysisDataFormats.CMGTools.interface.Lepton.h : DBeta correction factor
# tightmuponNoVtx : CMGTools.Common.selections.muonsIDs_cfi : Global, PF, numberOf ..., chi2 
# dxy, dz : wrt PV : CMGTools.Common.factories.cmgLepton_cfi CMGTools.Common.interface.LeptonSettingTool.h
 
razorMuonSequence = cms.Sequence(
    razorLooseMuon +
    razorTightMuon
    )
