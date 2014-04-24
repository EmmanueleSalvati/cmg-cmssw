#!/bin/tcsh

cd /afs/cern.ch/work/s/salvati/CMGTools/CMSSW_5_3_14/src/CMGTools/Common/crab
eval `scramv1 runtime -csh`
cmsRun /afs/cern.ch/work/s/salvati/CMGTools/CMSSW_5_3_14/src/CMGTools/Common/crab/PATCMG_cfg.py
