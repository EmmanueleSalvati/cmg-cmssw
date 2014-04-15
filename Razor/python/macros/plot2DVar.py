#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re
from array import array
from math import sqrt
from optparse import OptionParser


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
    parser = OptionParser()
    
    cut = parser.add_option("-c", "--cut", 
                            dest="cut", 
                            help="cutflow",
                            default='')
    (options,args) = parser.parse_args()

  
    ###### SAMPLES
    #signal
    directory = 'MultiJet/'
#    components = {'QCD100':22305.52344, 'QCD250':197.47971, 'QCD500':5.48350, 'QCD1000':0.28559}#, 'TTJets']
    components = {'TTJets':0.44}
    files     = {}
    trees     = {}
    histos = []
    for i in range(0,6):
        index=i+1
        histos.append(rt.TH2F( 'histo'+str(index),'histo'+str(index),15, 0., 150, 10, 0., 1.))
        histos[i].SetTitle("linear radial momentum vs charged multiplicity, TTJets, jet %s;charged multiplicity;lrm"%str(index))

    for comp, weight in components.iteritems() :
        print comp
        filename = directory+comp+'/MultiJetAnalysis/MultiJetAnalysis_tree.root'
        files[filename]   = rt.TFile(filename)
        trees[filename]   = files[filename].Get("MultiJetAnalysis")

        for i in range(0,6):
            tmp= rt.TH2F( 'tmp'+str(i),'tmp'+str(i),15, 0., 150, 10, 0., 1.)
            trees[filename].Draw("lrm%s:chMultiplicity%s>>tmp%s"%(str(i+1),str(i+1),str(i)))
            histos[i].Add(tmp, weight)
            
            
    comp = "TTJets"
    for i in range(0,6):
        c = rt.TCanvas(comp+"_jet%s"%str(i+1)+".png")
        histos[i].DrawNormalized("colz")
        c.SaveAs(c.GetName())
        
