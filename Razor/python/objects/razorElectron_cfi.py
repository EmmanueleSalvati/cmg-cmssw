import FWCore.ParameterSet.Config as cms

from CMGTools.Common.skims.cmgElectronSel_cfi import *

razorLooseElectron = cmgElectronSel.clone(
    src = "cmgElectronSel",
    cut = "(pt() > 5.) \
           && (abs(eta()) < 2.5) \
           && sourcePtr().userFloat('isLooseLeptonSAK')"
    )

razorTightElectron = cmgElectronSel.clone(
    src = "cmgElectronSel",
    cut = "(pt() > 30.) \
           && (abs(eta()) < 2.5) \
           && (abs(sourcePtr().superCluster().eta()) <= 1.4442 || abs(sourcePtr().superCluster().eta()) > 1.566) \
           && getSelection(\"cuts_mediumNoVtx\") \
           && relIso(0.5) < 0.15 \
           && abs(dxy()) < 0.02 \
           && abs(dz()) < 0.1"
    )

razorElectronSequence = cms.Sequence(
    razorLooseElectron +
    razorTightElectron
    )
