#! /usr/bin/env python
from optparse import OptionParser

import os.path
import sys, re
from array import *

if __name__ == '__main__':
#    datasetName = sys.argv[1]
    mLSP = sys.argv[1]
 #   mStop = sys.argv[1]
   
    queue = "1nd"
    pwd = os.environ['PWD']
    datasetNames = {
    ##    'SingleEleA':'/SingleElectron/Run2012A-22Jan2013-v1/AOD/V5_B/PAT_CMG_V5_17_0/SUSY/',
    ##    'SingleEleB':'/SingleElectron/Run2012B-22Jan2013-v1/AOD/V5_B/PAT_CMG_V5_17_0/SUSY/',
    ##     'SingleEleC':'/SingleElectron/Run2012C-22Jan2013-v1/AOD/V5_B/PAT_CMG_V5_17_0/SUSY/',
##         'SingleEleD':'/SingleElectron/Run2012D-22Jan2013-v1/AOD/V5_B/PAT_CMG_V5_17_0/SUSY/',
##        'SingleMuA':'/SingleMu/Run2012A-22Jan2013-v1/AOD/PAT_CMG_V5_17_0/SUSY/',
##        'SingleMuB':'/SingleMu/Run2012B-22Jan2013-v1/AOD/PAT_CMG_V5_17_0/SUSY/',
##        'SingleMuC':'/SingleMu/Run2012C-22Jan2013-v1/AOD/PAT_CMG_V5_17_0/SUSY/',
##        'SingleMuD':'/SingleMu/Run2012D-22Jan2013-v1/AOD/PAT_CMG_V5_17_0/SUSY/',
##        'MultiJet1':'/MultiJet1Parked/Run2012C-part1_05Nov2012-v2/AOD/V5_B/PAT_CMG_V5_17_0/SUSY/',
##        'MultiJet2':'/MultiJet1Parked/Run2012C-part2_05Nov2012-v2/AOD/V5_B/PAT_CMG_V5_17_0/SUSY/',
        
      #  'SMS-T2tt_mStop-500to650_mLSP-0to225_8TeV-Pythia6Z':'/SMS-T2tt_mStop-500to650_mLSP-0to225_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY_MERGED/',
      #  'SMS-T2tt_mStop-500to650_mLSP-250to550_8TeV-Pythia6Z':'/SMS-T2tt_mStop-500to650_mLSP-250to550_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY_MERGED/',
        'SMS-T2tt_mStop-675to800_mLSP-0to275_8TeV-Pythia6Z':'/SMS-T2tt_mStop-675to800_mLSP-0to275_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY_MERGED/',
      #  'SMS-T2tt_mStop-675to800_mLSP-300to700_8TeV-Pythia6Z':'/SMS-T2tt_mStop-675to800_mLSP-300to700_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY_MERGED/',
     #  'SMS-T2tt_mStop-150to350_mLSP-0to250_8TeV-Pythia6Z':'/SMS-T2tt_mStop-150to350_mLSP-0to250_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY_MERGED/',
     #   'SMS-T2tt_mStop-375to475_mLSP-0to375_8TeV-Pythia6Z':'/SMS-T2tt_mStop-375to475_mLSP-0to375_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/CMGPF_V5_16_0/SUSY_MERGED/',
#        'TTJets':'/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY_MERGED/',
       ##  'WJets':'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM/V5_B/CMGPF_V5_16_0/SUSY_MERGED/',
##        'QCD1000ToInf':'/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY_MERGED',
##        'QCD100To250' :'/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY_MERGED',
##        'QCD250To500' :'/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY_MERGED',
##        'QCD500To1000':'/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY_MERGED',
##        'DY':'/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY_MERGED'
##       'T_tW':'/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY',
##       'Tbar_tW':'/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/SUSY'
}

    for dataset,datasetName in datasetNames.iteritems() :

        submitDir = pwd+"/submit_"+dataset
        
        resultDir = "/afs/cern.ch/work/l/lucieg/private/RazorMultiJet/%s/%s"%(dataset,mLSP)
        ffDir = "/afs/cern.ch/work/l/lucieg/private/RazorMultiJet/%s/logs_%s"%(dataset,mLSP)
    
        os.system("mkdir -p %s"%(submitDir)) 
        os.system("mkdir -p %s"%(ffDir))
        os.system("mkdir -p %s"%resultDir)
        # prepare the script to run
        for index in range(0,100):
            outputname = submitDir+"/submit_"+dataset+str(index)+".src"
            outputfile = open(outputname,'w')
            outputfile.write('#!/bin/bash\n')
            outputfile.write('cd %s \n'%pwd)
            outputfile.write('echo $PWD \n')
            outputfile.write('eval `scramv1 runtime -sh` \n')
            outputfile.write("python /afs/cern.ch/user/l/lucieg/scratch1/Sep8/CMGTools/CMSSW_5_3_9/src/CMGTools/Susy/macros/MultiJet/razorMJDataset.py datasetName=%s maxFiles=3 index=%i mLSP=%s outputDirectory=%s"%(datasetName,index,mLSP,resultDir))
            outputfile.close
            os.system("echo bsub -q "+queue+" -o "+ffDir+"/log"+str(index)+".log source "+outputname)
            os.system("bsub -q "+queue+" -o "+ffDir+"/log"+str(index)+".log source "+outputname)
