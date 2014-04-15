import FWCore.ParameterSet.Config as cms

from CMGTools.Common.Tools.cmsswRelease import isNewerThan

sep_line = '-'*67
print sep_line
print 'CMG PAT-tuplizer, contact Colin before any modification'
print sep_line

process = cms.Process("RZR")


print 'querying database for source files'


runOnMC      = True
runOnFastSim = False

from CMGTools.Production.datasetToSource import *
## This is used to get the correct global tag below, and to find the files
## It is *reset* automatically by ProductionTasks, so you can use it after the ProductionTasksHook
datasetInfo = (
   # 'cmgtools',
   # '/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/',
   # '/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/',
   # '/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/',
   # '/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/',
   # '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/',
    'lucieg',
    '/SMS-T2tt_mStop-675to800_mLSP-0to275_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/PAT_CMG_V5_17_0',
   # '/SMS-T2tt_mStop-500to650_mLSP-0to225_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/PAT_CMG_V5_17_0',
#    '/SMS-T2tt_mStop-150to350_mLSP-0to250_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/PAT_CMG_V5_17_0',

#    '/SMS-T2tt_mStop-375to475_mLSP-0to375_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/PAT_CMG_V5_17_0',
    # 'CMS',
    # '/DoubleMu/Run2012A-22Jan2013-v1/AOD',
    '.*root')
process.source = datasetToSource(
    *datasetInfo
    )

#process.source.fileNames = cms.untracked.vstring('file:cmgTuple.root')
#process.source.fileNames = process.source.fileNames[:20]
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

print sep_line
print process.source.fileNames
print sep_line 


print 'loading the main razor sequence'

process.load('CMGTools.Razor.razor_cff')


# setting up JSON file
# json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/DCSOnly/json_DCSONLY.txt'
# print 'using json file: ', json
# from CMGTools.Common.Tools.applyJSON_cff import *
# applyJSON(process, json )


########################################################
## Path definition
########################################################

process.p = cms.Path(
    process.razorObjectSequence
    )



########################################################
## output definition
########################################################

## Output Module Configuration (expects a path 'p')
from CMGTools.Razor.eventContent.razorEventContent_cff import razorEventContent
process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('razorTuple.root'),
                               # save only events passing the full path
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               outputCommands = razorEventContent
                               )

process.outpath = cms.EndPath(
    process.out
    )

process.schedule = cms.Schedule(
    process.p,
    process.outpath
    )


########################################################
## Conditions 
########################################################

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")

########################################################
## Below, stuff that you probably don't want to modify
########################################################




## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10
process.MessageLogger.suppressWarning = cms.untracked.vstring('ecalLaserCorrFilter')
## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


### Set the global tag from the dataset name
from CMGTools.Common.Tools.getGlobalTag import getGlobalTagByDataset
process.GlobalTag.globaltag = getGlobalTagByDataset( runOnMC, datasetInfo[1])
print 'Global tag       : ', process.GlobalTag.globaltag
###

print sep_line

print 'starting CMSSW'


