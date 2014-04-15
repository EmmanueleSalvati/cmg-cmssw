#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re
from array import array

rt.RooWorkspace.rfimport = getattr(rt.RooWorkspace, 'import')

if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
    
    box   = sys.argv[1]
    mLSP = sys.argv[2]
    mStop = sys.argv[3]
    ###### SAMPLES
    #data
    directoryData = ''#'/data/wreece/RazorMultijet_2012/220113/'
    filenameData  = directoryData+'SingleElectron-Run2012ABCD-wreece_220113-Combo_MR350.0_R0.22360679775_Ele.root'
    fileData = rt.TFile(filenameData)
    treeData = fileData.Get("RMRTree")


    #signal
    directory = '/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/Datasets/mLSP' +str(mLSP)+'_origin/'
    if box == 'BJetHS' or box == 'BJetLS':
        label  ='_MR500.0_R0.22360679775_'
    else :
        label  ='_MR350.0_R0.22360679775_'
    filename = directory+'SMS-T2tt_mStop-Combo_mLSP_'+str(mLSP)+'_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY'+label+str(mStop)+'_'+str(mLSP)+'_'+box +'.root'

    file = rt.TFile(filename)
    tree = file.Get("RMRTree")
    wHisto = file.Get("wHisto")
    eff = wHisto.Integral()
    print 'eff',eff

    ##########

    #MRbins  = array('d',[350.0, 400.0, 450.0, 500.0, 550.0, 650.0, 790.0, 1000, 1500, 2200, 3000, 4000.0])
    MRbins  = array('d',[350.0, 450.0, 550.0, 650.0, 750.0, 850.0, 1000, 1500, 2200, 3000, 4000.0])
    Rsqbins = array('d',[0.05, 0.07, 0.12, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0])
 
 
    w = rt.RooWorkspace("w")
    w.rfimport(tree)
    

    frame = w.var("MR").frame()
    w.data("RMRTree").plotOn(frame)
    frame.Draw()

    h = w.data("RMRTree").createHistogram(w.var("MR"),w.var("Rsq"),1000, 1000)
    h.Draw()

    h2 = h.ProjectionY()
    h3 = h2.Rebin(8,"h3",Rsqbins)
    h3.Draw()
    #add pdf
    #w.factory("Exponential::f(mr[350.0, 1000.0], -1)")
    #w.factory("EXPR::mypdf('(MR-MR0)*Exponential(MR-MR0, -1)', MR, MR0[1.])")
    #w.Print("V")
