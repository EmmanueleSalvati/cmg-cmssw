from PhysicsTools.PatAlgos.patTemplate_cfg import *
from CMGTools.Production.datasetToSource import *

DATASETINFO = ('', ('/store/user/salvati/Razor/MultiJet2012/'
    'CMSSW_5_3_14/CMGTuples/T1tttt/mGo-775to1075_mLSP-25to500/'),
    'cmgTuple.root')

FILE_LIST = os.listdir('%s' % DATASETINFO[1].replace('/store', '/mnt/xrootd'))
MY_FILE_LIST = cms.untracked.vstring()

# INDEX_LIST = [10,20,41,42,51,64,67,70]

for i in range(0, len(FILE_LIST)):
    MY_FILE_LIST.extend([DATASETINFO[1]+FILE_LIST[i]])

# # to resubmit some jobs
# EXT_LIST = []
# for i in INDEX_LIST:
#     with open(('step2_T1tttt_mGo-775to1075_mLSP-25to500/Job_%s/'
#                'input_files.txt') % i) as INFILE:
#         for line in INFILE:
#             EXT_LIST.append(line.rstrip('\n'))
# ###############################
# MY_FILE_LIST.extend(EXT_LIST)

# print "My fucking file list is", MY_FILE_LIST

process.source = cms.Source(
    "PoolSource",
    noEventSort=cms.untracked.bool(True),
    duplicateCheckMode=cms.untracked.string("noDuplicateCheck"),
    fileNames=cms.untracked.vstring(MY_FILE_LIST)
    )

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))

process.maxLuminosityBlocks = cms.untracked.PSet(
    input=cms.untracked.int32(-1)
    )

RUN_ON_MC = True
DATASET_FOR_GLOBAL_TAG = ['',
    '/SMS-MadGraph_Pythia6Zstar_8TeV_T1tttt_2J_mGo-775to1075_mLSP-25to500_50GeVX50GeV_Binning/Summer12-START52_V9_FSIM-v3/AODSIM']
# DATASET_FOR_GLOBAL_TAG = DATASETINFO

### Set the global tag from the dataset name
from CMGTools.Common.Tools.getGlobalTag import getGlobalTagByDataset
process.GlobalTag.globaltag = getGlobalTagByDataset(RUN_ON_MC,
    DATASET_FOR_GLOBAL_TAG[1])
print 'Global tag       : ', process.GlobalTag.globaltag
###

##########
from CMGTools.Common.Tools.applyJSON_cff import applyJSON
json = 'goldenJson.txt'
if not RUN_ON_MC:
    applyJSON(process, json )

##########
skimEvents = False
# Message logger setup.
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(False))

process.setName_('MJSkim')

print 'processing:'
print process.source.fileNames

process.p = cms.Path()

process.load('CMGTools.Susy.susy_cff')
process.load('CMGTools.Susy.common.susy_cff')
process.schedule = cms.Schedule(
    process.p,
    process.razorMJSkimSequenceHadPath,
    process.razorMJSkimSequenceElePath,
    process.razorMJSkimSequenceMuPath,
    process.trkVetoLeptonSequencePath,
    process.outpath
    )
if RUN_ON_MC:
    process.p += process.susyGenSequence
else:
    process.p += process.susyDataSequence

#don't know where this comes from, but it screws things up and we don't use it
del process.eIdSequence

from CMGTools.Susy.susyEventContent_cff import susyEventContent
process.out.fileName = cms.untracked.string('susy_tree.root')
process.out.outputCommands = cms.untracked.vstring('drop *')
from CMGTools.Common.eventContent.eventCleaning_cff import eventCleaning
process.out.outputCommands.extend(eventCleaning)
process.out.outputCommands += susyEventContent

SelectEvents = cms.vstring('razorMJSkimSequenceHadPath',
    'razorMJSkimSequenceElePath', 'razorMJSkimSequenceMuPath')
if not skimEvents:
    SelectEvents.append('p')

process.out.SelectEvents = cms.untracked.PSet(SelectEvents=SelectEvents)


print 'output file: ', process.out.fileName
