import FWCore.ParameterSet.Config as cms

process = cms.Process("COPY")

from CMGTools.Production.datasetToSource import *
#datasetInfo = ('lucieg', '/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY','susy_tree_2__[0-9]+.root')
#datasetInfo = ('lucieg', '/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY','susy_tree_2__[0-9]+.root')
#datasetInfo = ('lucieg', '/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY/','susy_tree_2__[0-9]+.root')
## datasetInfo = ('lucieg', '/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY','susy_tree_2__[0-9]+.root')
#datasetInfo = ('lucieg', '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM/V5_B/CMGPF_V5_16_0/SUSY','susy_tree_2__[0-9]+.root')
#datasetInfo = ('lucieg', '/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY','susy_tree_2__[0-9]+.root')
#datasetInfo = ('lucieg', '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY','susy_tree_2__[0-9]+.root')
#datasetInfo = ('lucieg', '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY','susy_tree_2__[0-9]+.root')
#datasetInfo = ('lucieg', '/SMS-T2tt_mStop-150to350_mLSP-0to250_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY','susy_tree_2__[0-9]+.root')
##datasetInfo = ('lucieg', '/SMS-T2tt_mStop-375to475_mLSP-0to375_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY','susy_tree_2__[0-9]+.root')
#datasetInfo = ('lucieg', '/SMS-T2tt_mStop-675to800_mLSP-0to275_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY','susy_tree_2__[0-9]+\\.root')

#datasetInfo = ('lucieg', '/SMS-T2tt_mStop-500to650_mLSP-0to225_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY','susy_tree_2__[0-9]+\\.root')

#datasetInfo = ('lucieg', '/SMS-T2tt_mStop-500to650_mLSP-250to550_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY','susy_tree_2__[0-9]+\\.root')

#datasetInfo = ('lucieg', '/SMS-T2tt_mStop-675to800_mLSP-300to700_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY','susy_tree_2__[0-9]+\\.root')

datasetInfo = ('lucieg', '/SMS-T2tt_mStop-925to1000_mLSP-1_and_mLSP-25to900_8TeV-Pythia6Zstar/Summer12-START52_V9_FSIM-v3/AODSIM/V5_B/CMGPF_V5_16_0/SUSY/', 'susy_tree_2__[0-9]+\\.root')

process.source = datasetToSource(
    *datasetInfo
    )



print process.source.fileNames

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load("Configuration.EventContent.EventContent_cff")
outFile = 'susy_tree.root'
process.out = cms.OutputModule(
    "PoolOutputModule",
    # process.AODSIMEventContent,
    outputCommands =  cms.untracked.vstring(
      'keep *'
      ),
    fileName = cms.untracked.string( outFile ),
    )

process.endpath = cms.EndPath(
    process.out
    )

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

## outpyFile = open("tmpConfig.py","w")
## outpyFile.write("import FWCore.ParameterSet.Config as cms\n")
## outpyFile.write(process.dumpPython())
## outpyFile.close()

## print process.source.fileNames
## print 'will be merged into ', outFile

#if not options.negate:
#os.system("cmsRun tmpConfig.py")

