from PhysicsTools.PatAlgos.patTemplate_cfg import *
from CMGTools.Production.datasetToSource import *

DATASETINFO = ('', ('/store/user/salvati/Razor/MultiJet2012/'
    'CMSSW_5_3_14/CMGTuples/Run2012D-part2_17Jan2013-v1_8/'),
    'cmgTuple.root')

# DATASETINFO = ('', '/SMS-MadGraph_Pythia6Zstar_8TeV_T1tttt_2J_mGo-1100to1400_mLSP-525to1000_25GeVX25GeV_Binning/Summer12-START52_V9_FSIM-v2/AODSIM',
#     'cmgTuple.root')

FILE_LIST = os.listdir('%s' % DATASETINFO[1].replace('/store', '/mnt/xrootd'))
MY_FILE_LIST = cms.untracked.vstring()
for i in range(0, len(FILE_LIST)):
    MY_FILE_LIST.extend([DATASETINFO[1]+FILE_LIST[i]])

# IN_FILES = open('cmgTuples_Run2012D-part1_10Dec2012-v1_8.txt', 'rU')
# IN_FILES = open('final_input_list.txt', 'rU')
# TMP_IN_FILES_LIST = IN_FILES.read().splitlines()
# IN_FILES_LIST = []
# for cmg_tuple in TMP_IN_FILES_LIST:
#     new_cmg_tuple = cmg_tuple.replace('/mnt/xrootd', '/store')
#     IN_FILES_LIST.append(new_cmg_tuple)

process.source = cms.Source(
    "PoolSource",
    noEventSort=cms.untracked.bool(True),
    duplicateCheckMode=cms.untracked.string("noDuplicateCheck"),
    fileNames=cms.untracked.vstring(MY_FILE_LIST)
    )

# process.source.fileNames = cms.untracked.vstring('/store/user/salvati/'
#     'Razor/MultiJet2012/CMSSW_5_3_14/CMGTuples/T1tttt/mGo-1100to1400_mLSP-525to1000/'
#     'cmgTuple_1734_1_Q9e.root')
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))

process.maxLuminosityBlocks = cms.untracked.PSet(
    input=cms.untracked.int32(-1)
    )

RUN_ON_MC = False
DATASET_FOR_GLOBAL_TAG = ['',
    '/MultiJet1Parked/Run2012D-part2_17Jan2013-v1/AOD']
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
runPAT = False
# Message logger setup.
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(False))

process.setName_('MJSkim')
# ext = ''

print 'processing:'
print process.source.fileNames

# outFileNameExt = ext

process.p = cms.Path()

if runPAT:
    process.load('CMGTools.Common.PAT.PATCMG_cff')

    if not RUN_ON_MC:
        print 'removing MC stuff, as we are running on Data'
        process.PATCMGSequence.remove(process.PATCMGGenSequence)

    print 'cloning the jet sequence to build PU chs jets'

    from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
    process.jetCHSSequence = cloneProcessingSnippet(process, process.jetSequence, 'CHS')
    from CMGTools.Common.Tools.visitorUtils import replaceSrc
    replaceSrc( process.jetCHSSequence, 'selectedPatJets', 'selectedPatJetsCHS')
    replaceSrc( process.jetCHSSequence, 'puJetId', 'puJetIdCHS')

    process.p += process.CMGSequence
    process.p += process.jetCHSSequence

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
if runPAT:
    process.out.outputCommands.extend(cms.untracked.vstring('drop cmg*_*_*_PAT'))
from CMGTools.Common.eventContent.eventCleaning_cff import eventCleaning
process.out.outputCommands.extend(eventCleaning)
process.out.outputCommands += susyEventContent

SelectEvents = cms.vstring('razorMJSkimSequenceHadPath',
    'razorMJSkimSequenceElePath', 'razorMJSkimSequenceMuPath')
if not skimEvents:
    SelectEvents.append('p')

process.out.SelectEvents = cms.untracked.PSet(SelectEvents=SelectEvents)


print 'output file: ', process.out.fileName
