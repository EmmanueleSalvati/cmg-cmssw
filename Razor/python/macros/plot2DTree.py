#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re
from array import array
from math import sqrt
from optparse import OptionParser

def line(x1, x2, y1, y2):
     print 'in line'
     print x1, x2, y1, y2
     tline = rt.TLine(x1, x2, y1, y2)
     tline.SetLineColor(rt.kBlack)
     tline.SetLineWidth(4)
     return tline

def sidebandLines():

    sidebands = []
    l1 = line(3000.,0.05, 3000., 0.09)
    l2 = line(650.,0.09, 3000., 0.09)
    l3 = line(650.,0.09, 650., 0.2)
    l4 = line(600.,0.2, 650., 0.2)
    l5 = line(600.,0.2, 600., 0.3)
    l6 = line(550.,0.3, 600., 0.3)
    l7 = line(550.,0.3, 550., 0.5)
    l8 = line(0.,0.5, 550., 0.5)
    sidebands.append(l1)
    sidebands.append(l2)
    sidebands.append(l3)
    sidebands.append(l4)
    sidebands.append(l5)
    sidebands.append(l6)
    sidebands.append(l7)
    sidebands.append(l8)

    return sidebands

def mDeltaLine(mD):

     lmDelta = line(mD, 0., mD, 1.)
     return lmDelta

def binnedHisto2D(tree, binsX, binsY, cut = '', label='') :

    histo = rt.TH2F("histo"+label, "histo"+label, len(binsX) -1, binsX, len(binsY) -1, binsY)
    if not(cut == ''):
         cut = " && "+cut
    
    for i_binx in range(0, len(binsX) - 1):
        for i_biny in range(0, len(binsY) - 1):
        
            binx     = binsX[i_binx]
            binx_p1  = binsX[i_binx+1]
            biny     = binsY[i_biny]
            biny_p1  = binsY[i_biny+1]

            numEntries = tree.GetEntries("MR > %s && MR < %s && Rsq > %s && Rsq < %s"%(binx, binx_p1, biny, biny_p1)+cut)
          #  numEntries = tree.GetEntries("mR2011 > %s && mR2011 < %s && Rsq > %s && Rsq < %s"%(binx, binx_p1, biny, biny_p1)+cut)
            histo.Fill(binx, biny, numEntries)

    return histo

if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
    parser = OptionParser()
    
    cut = parser.add_option("-c", "--cut", 
                            dest="cut", 
                            help="cutflow",
                            default='')
    (options,args) = parser.parse_args()

    ########## binning def
   # MRbins  = array('d',[350.0,  450.0, 550.0, 650.0, 790.0, 1000, 1500, 2200, 3000, 4000.0])
   # Rsqbins = array('d',[0.05, 0.07, 0.12, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0])
    MRbins  = array('d',[0., 50., 150., 250., 350.0, 450.0, 600.0, 800.0, 1050.0, 1500.0, 2200.0, 3000.0, 4000.0])
    Rsqbins = array('d',[0., 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
 
    ###### SAMPLES
    #signal
    directory = '/afs/cern.ch/work/l/lucieg/private/MultiJet/'
    mLSP = '25'
    
    files     = {}
    trees     = {}
    mDelta    = {}
    massivemDelta = {}
    
    
    for mStop in range(300, 400, 100):
         #filename = directory+'T2tt_'+str(mStop)+'/MultiJetAnalysis/MultiJetAnalysis_tree.root'
   ##      filename = directory+'TTJets/MultiJetAnalysis/MultiJetAnalysis_tree.root'
##         filename = directory+'QCD100/MultiJetAnalysis/MultiJetAnalysis_tree.root'
##         filename = directory+'QCD250/MultiJetAnalysis/MultiJetAnalysis_tree.root'
##         filename = directory+'QCD500/MultiJetAnalysis/MultiJetAnalysis_tree.root'
         filename = directory+'QCD1000/MultiJetAnalysis/MultiJetAnalysis_tree.root'
         files[filename]   = rt.TFile(filename)
         trees[filename]   = files[filename].Get("MultiJetAnalysis")
         
         ####### 2D plots
        # sidebands = sidebandLines()
         cutString = re.sub(' ','',options.cut)
        # c = rt.TCanvas("plots/RsqMR2D_mStop%s_mLSP%s_"%(mStop, mLSP)+cutString+".png", "RsqMR2D_mStop%s_mLSP%s_"%(mStop, mLSP)+cutString+".png")
      ##   c = rt.TCanvas("plots/TTJets.png", "TTJets"+cutString+".png")
      ##   c = rt.TCanvas("plots/QCD100.png", "QCD100"+cutString+".png")
      ##   c = rt.TCanvas("plots/QCD250.png", "QCD250"+cutString+".png")
      ##   c = rt.TCanvas("plots/QCD500.png", "QCD500"+cutString+".png")
         c = rt.TCanvas("plots/QCD1000.png", "QCD1000"+cutString+".png")
        
         c.cd()
         c.SetLogx()
         c.SetLogy()
        ##  tmp = rt.TH1F( 'tmp','tmp',1000, 0., 4000.)
##          trees[filename].Draw("mDelta>>tmp")
##          mD = tmp.GetMean()
##          l = mDeltaLine(mD)
         histo = binnedHisto2D(trees[filename], MRbins, Rsqbins, options.cut, 'signal') 
        # histo.SetTitle("Rsq vs MR, variables, mStop = %s, mLSP = %s;MR(GeV);Rsq"%(mStop, mLSP))
       ##  histo.SetTitle("Rsq vs MR, variables, TTJets;MR(GeV);Rsq")
       ##  histo.SetTitle("Rsq vs MR, variables, QCD100;MR(GeV);Rsq")
       ##  histo.SetTitle("Rsq vs MR, variables, QCD250;MR(GeV);Rsq")
       ##  histo.SetTitle("Rsq vs MR, variables, QCD500;MR(GeV);Rsq")
         histo.SetTitle("Rsq vs MR, variables, QCD1000;MR(GeV);Rsq")
         histo.Draw("colz")
        # l.Draw("SAME")
         c.SaveAs(c.GetName())
         
   
