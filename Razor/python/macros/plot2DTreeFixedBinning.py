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


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
    parser = OptionParser()
    
    cut = parser.add_option("-c", "--cut", 
                            dest="cut", 
                            help="cutflow",
                            default='')
    (options,args) = parser.parse_args()

 
    ###### SAMPLES
    
    directory = '/afs/cern.ch/work/l/lucieg/private/MultiJet/'

    samples = {
         'TTJets' :directory+'TTJets/MultiJetAnalysis/MultiJetAnalysis_tree.root' ,
        ##  'QCD100' :directory+'QCD100/MultiJetAnalysis/MultiJetAnalysis_tree.root',
##          'QCD250' :directory+'QCD250/MultiJetAnalysis/MultiJetAnalysis_tree.root',
##          'QCD500' :directory+'QCD500/MultiJetAnalysis/MultiJetAnalysis_tree.root',
##          'QCD1000':directory+'QCD1000/MultiJetAnalysis/MultiJetAnalysis_tree.root',
          }
    for mStop in range(300, 700, 100):
         samples['T2tt_'+str(mStop)] = directory+'T2tt_'+str(mStop)+'/MultiJetAnalysis/MultiJetAnalysis_tree.root'
    
    mLSP = '25'
    
    mDelta    = {}
    massivemDelta = {}
    
    
    for sample, filename in samples.iteritems() :
         file   = rt.TFile(filename)
         tree   = file.Get("MultiJetAnalysis")
         
         ####### 2D plots
         cutString = re.sub(' ','',options.cut)
         if sample.startswith('T2tt'):
              title = 'plots/'+sample+'_mLSP'+mLSP+'_'+cutString+'.png'
         else :
              title = 'plots/'+sample+'_'+cutString+'.png'
         c = rt.TCanvas(title, title)
        
         c.cd()
       ##   c.SetLogx()
##          c.SetLogy()
         if sample.startswith('T2tt'):
              tmp = rt.TH1F( 'tmp','tmp',1000, 0., 4000.)
              tree.Draw("mDelta>>tmp")
              mD = tmp.GetMean()
              l = mDeltaLine(mD)
        # RsqMR=rt.TH2D('RsqMR','RsqMR',50, 0., 4000., 25, 0., 1.)
         RsqMR=rt.TH2D('RsqMR','RsqMR',25, 0., 2000., 25, 0., 1.)
         tree.Draw("Rsq:MR>>RsqMR", str(options.cut))
        ##  RsqMR.Scale (1./RsqMR.GetMaximum())
##          RsqMR.SetMaximum(RsqMR.GetMaximum())
         RsqMR.SetTitle('Rsq vs MR, '+sample+';MR(GeV);Rsq')
         RsqMR.Draw("colz")
         if sample.startswith('T2tt'):
              l.Draw("SAME")
         c.SaveAs(c.GetName())
         #raw_input()
   
