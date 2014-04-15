import FWCore.ParameterSet.Config as cms

from CMGTools.Common.factories.cmgTriggerObject_cfi import *

razorCleaning = cmgTriggerObject.clone()

razorCleaning.cfg.triggerResults = cms.InputTag("TriggerResults","","PAT")
razorCleaning.cfg.processName    = "PAT"
