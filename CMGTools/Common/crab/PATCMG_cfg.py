import FWCore.ParameterSet.Config as cms

from CMGTools.Common.Tools.cmsswRelease import isNewerThan

sep_line = '-'*67
print sep_line
print 'CMG PAT-tuplizer, contact Colin before any modification'
print sep_line

process = cms.Process("PAT")

print 'querying database for source files'
runOnMC = True
runOnFastSim = True

from CMGTools.Production.datasetToSource import *
## This is used to get the correct global tag below, and to find the files
datasetInfo = ('', '/SMS-MadGraph_Pythia6Zstar_8TeV_T1tttt_2J_mGo-1100to1400_mLSP-525to1000_25GeVX25GeV_Binning/Summer12-START52_V9_FSIM-v2/AODSIM')

process.source = cms.Source(
    "PoolSource",
    noEventSort=cms.untracked.bool(True),
    duplicateCheckMode=cms.untracked.string("noDuplicateCheck"),
    fileNames=cms.untracked.vstring('DUMMY')
    )

# process.source.fileNames = cms.untracked.vstring('root://eoscms//eos/'
#     'cms/store/cmst3/user/lucieg/CMG/fileRun2012Dpart2_17Jan2013-v1.root')
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))

print sep_line
print process.source.fileNames
print sep_line

print 'loading the main CMG sequence'
process.load('CMGTools.Common.PAT.PATCMG_cff')

if runOnMC is False:
    print 'removing MC stuff, as we are running on Data'

    process.patElectrons.addGenMatch = False
    process.makePatElectrons.remove(process.electronMatch)
    process.patMuons.addGenMatch = False
    process.makePatMuons.remove(process.muonMatch)

    process.PATCMGSequence.remove(process.PATCMGGenSequence)
    process.PATCMGJetSequence.remove(process.jetMCSequence)
    process.PATCMGJetSequence.remove(process.patJetFlavourId)
    process.patJets.addGenJetMatch = False
    process.patJets.addGenPartonMatch = False

    process.PATCMGTauSequence.remove(process.tauGenJets)
    process.PATCMGTauSequence.remove(process.tauGenJetsSelectorAllHadrons)
    process.PATCMGTauSequence.remove(process.tauGenJetMatch)
    process.PATCMGTauSequence.remove(process.tauMatch)
    process.patTaus.addGenJetMatch = False
    process.patTaus.addGenMatch = False

    process.patMETs.addGenMET = False
    process.patMETsRaw.addGenMET = False


    process.patJetCorrFactors.levels.append('L2L3Residual')


process.muPFIsoDepositChargedAll.ExtractorPSet.DR_Veto = 1e-3

print 'cloning the jet sequence to build PU chs jets'
from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
process.PATCMGJetCHSSequence = cloneProcessingSnippet(process,\
    process.PATCMGJetSequence, 'CHS')
process.PATCMGJetCHSSequence.insert(0, process.ak5PFJetsCHS)
from CMGTools.Common.Tools.visitorUtils import replaceSrc
replaceSrc(process.PATCMGJetCHSSequence, 'ak5PFJets', 'ak5PFJetsCHS')
replaceSrc(process.PATCMGJetCHSSequence, 'particleFlow', 'pfNoPileUp')
process.PATCMGJetCHSSequence.remove(process.outPFCandCHS)
process.PATCMGJetCHSSequence.remove(process.ak5SoftPFJetsForVbfHbbCHS)
jecPayload = 'AK5PFchs'
process.patJetsWithVarCHS.payload = jecPayload
process.patJetCorrFactorsCHS.payload = jecPayload
process.puJetIdCHS.jec = jecPayload
process.cmgPUJetMvaCHS.jec = jecPayload
process.selectedPatJetsCHS.cut = 'pt()>10'


########################################################
## Path definition
########################################################

process.dump = cms.EDAnalyzer('EventContentAnalyzer')

process.load('CMGTools.Common.PAT.addFilterPaths_cff')
process.p = cms.Path(
    process.prePathCounter +
    process.PATCMGSequence +
    process.PATCMGJetCHSSequence
    )

if 'Prompt' in datasetInfo[1] or runOnMC:
    process.metNoiseCleaning.remove(process.hcalfilter)
if ('Parked' in datasetInfo[1]) or ('22Jan2013' in datasetInfo[1]):
    process.metNoiseCleaning.remove(process.hcallasereventfilter2012)

process.p += process.postPathCounter


########################################################
## CMG output definition
########################################################

process.outpath = cms.EndPath()

from CMGTools.Common.eventContent.patEventContentCMG_cff import everything
process.outcmg = cms.OutputModule(
    "PoolOutputModule",
    fileName=cms.untracked.string('cmgTuple.root'),
    SelectEvents=cms.untracked.PSet(SelectEvents=cms.vstring('p')),
    outputCommands=everything,
    dropMetaData=cms.untracked.string('PRIOR')
    )
process.outpath += process.outcmg

########################################################
## Conditions
########################################################

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")

########################################################
## Below, stuff that you probably don't want to modify
########################################################

## Geometry and Detector Conditions (needed for a few patTuple production steps)

from CMGTools.Common.PAT.patCMGSchedule_cff import getSchedule
process.schedule = getSchedule(process, runOnMC, runOnFastSim)
process.schedule.append(process.outpath)

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10
process.MessageLogger.suppressWarning =\
    cms.untracked.vstring('ecalLaserCorrFilter')
## Options and Output Report
process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(False))

if not runOnMC and isNewerThan('CMSSW_5_2_0'):
    process.pfJetMETcorr.jetCorrLabel = cms.string("ak5PFL1FastL2L3Residual")

print sep_line

print 'Fastjet instances (dominating our processing time...):'
from CMGTools.Common.Tools.visitorUtils import SeqVisitor
v = SeqVisitor('FastjetJetProducer')
process.p.visit(v)

### Set the global tag from the dataset name
from CMGTools.Common.Tools.getGlobalTag import getGlobalTagByDataset
process.GlobalTag.globaltag = getGlobalTagByDataset(runOnMC, datasetInfo[1])
print 'Global tag       : ', process.GlobalTag.globaltag
###

print sep_line

print 'starting CMSSW'
