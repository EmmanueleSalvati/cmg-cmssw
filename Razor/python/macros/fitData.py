#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re
from array import array

rt.RooWorkspace.rfimport = getattr(rt.RooWorkspace, 'import')

if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
    
    box   = sys.argv[1]

    ###### SAMPLES
    #data
    directoryData = ''#'/data/wreece/RazorMultijet_2012/220113/'
    filenameData  = directoryData+'SingleElectron-Run2012ABCD-wreece_220113-Combo_MR350.0_R0.22360679775_Ele.root'
    fileData = rt.TFile(filenameData)
    treeData = fileData.Get("RMRTree")

    ##########

    #MRbins  = array('d',[350.0, 400.0, 450.0, 500.0, 550.0, 650.0, 790.0, 1000, 1500, 2200, 3000, 4000.0])
    MRbins  = array('d',[350.0, 450.0, 550.0, 650.0, 750.0, 850.0, 1000, 1500, 2200, 3000, 4000.0])
    Rsqbins = array('d',[0.05, 0.07, 0.12, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0])
 
 
    w = rt.RooWorkspace("w")
    w.rfimport(treeData)
    

    frame = w.var("MR").frame()
    w.data("RMRTree").plotOn(frame)
    frame.Draw()

    h = w.data("RMRTree").createHistogram(w.var("MR"),w.var("Rsq"),50, 50)
    h.Draw()
    #add pdf
    #w.factory("Exponential::f(mr[350.0, 1000.0], -1)")
    w.factory("expr::myxy('(MR-MR0)*(Rsq-Rsq0)',MR, MR0[100.],Rsq, Rsq0[0.5])")
    w.factory("Exponential::f(myxy, -1)")
    w.Print("V")
