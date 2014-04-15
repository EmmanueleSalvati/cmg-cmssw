#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re
from array import array
from math import sqrt


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
             
    files = {
        'TTJets':'/afs/cern.ch/work/l/lucieg/private/RazorMultiJet/TTJets/0/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10_START53_V7C-v1-SUSY.root',
        'T2tt_25':'/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/SMS-T2tt_mStop-Combo_mLSP_25.0_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY.root',
        'T2tt_125':'/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/SMS-T2tt_mStop-Combo_mLSP_125.0_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY.root',
        'T2tt_225':'/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/SMS-T2tt_mStop-Combo_mLSP_225.0_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY.root',
      #  'T2tt_325':'/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/SMS-T2tt_mStop-Combo_mLSP_325.0_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY.root',
        }

    histos = {}
    trees     = {}
    rtfiles = {}
    
    for sample, filename in files.iteritems():
         print sample
         rtfiles[filename]   = rt.TFile(filename)
         #file = rt.TFile(filename)
         trees[sample]   = rtfiles[filename].Get("RMRTree")
         
         
         ctemp = rt.TCanvas("ctemp")
         ctemp.cd()
         histos[sample] = rt.TH1F('hemi1ThetaH_'+sample, 'hemi1ThetaH_'+sample, 50, -1., 1. )
         histos[sample].SetTitle("hemi1, ThetaH")
         cut = ''
         #if not(sample == 'TTJets') :
         cut = ' nJet >= 6 && metFilter && hadBoxFilter && hadTriggerFilter && nCSVM > 0 && MR >= 350 && RSQ >= 0.03 && nMuonTight == 0 && nElectronTight == 0 && !(isolatedTrack10Filter) && nMuonLoose == 0 && nElectronLoose == 0'
         
         trees[sample].Project('hemi1ThetaH_'+sample,'hemi1ThetaH', cut)
         histos[sample].Scale(1./ histos[sample].Integral() )
         histos[sample].SetLineWidth(3)
         #histos[sample]= histo.Clone('hemi1ThetaH_'+sample)

    print histos
    c = rt.TCanvas("hemi1ThetaH.png")
    c.cd()
    leg = rt.TLegend(0.5,0.1,0.8,0.4)
    n = 0
    for sample, histo in sorted(histos.iteritems()):
         if n == 0:
              histo.SetLineColor(rt.kBlack)
              histo.Draw()
              leg.AddEntry(histo, sample,"lep")
         else :
              histo.SetLineColor(rt.kBlack+n)
              histo.Draw("SAME")
              leg.AddEntry(histo, sample,"lep")
         n+=1
    leg.Draw("SAME")
    c.SaveAs(c.GetName())
         
  
