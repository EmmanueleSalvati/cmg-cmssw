#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re

if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
    
    box   = sys.argv[1]
    mStop = sys.argv[2]
    mLSP  = sys.argv[3]

    directory = '/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/Datasets/mLSP' +str(mLSP)+'/'
    if box == 'BJetHS' or box == 'BJetLS':
        label  ='_MR500.0_R0.22360679775_'
    else :
        label  ='_MR350.0_R0.22360679775_'
    filename = directory+'SMS-T2tt_mStop-Combo_mLSP_'+str(mLSP)+'_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY'+label+str(mStop)+'_'+str(mLSP)+'_'+box +'.root'
    file = rt.TFile(filename)
    print filename
    tree = file.Get("RMRTree")
    print tree
    tree.Print("V")
##         histoRsq = tree.createHistogram("MR")
##         histoRsq.Draw()
