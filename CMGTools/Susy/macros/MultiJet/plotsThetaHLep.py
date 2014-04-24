#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re
from array import array
from math import sqrt


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)

    #file = rt.TFile('/afs/cern.ch/work/l/lucieg/private/RazorMultiJet/SMS-T2tt_mStop-150to350_mLSP-0to250_8TeV-Pythia6Z/0/SMS-T2tt_mStop-150to350_mLSP-0to250_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY_MERGED.root')
    file = rt.TFile('/afs/cern.ch/work/l/lucieg/private/RazorMultiJet/SMS-T2tt_mStop-675to800_mLSP-0to275_8TeV-Pythia6Z/0/SMS-T2tt_mStop-675to800_mLSP-0to275_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY_MERGED.root')

    histoP1 = rt.TH1F('hemiLepThetaHP1', 'hemiLepThetaHP1', 100, -1., 1. )
    histo   = rt.TH1F('hemiLepThetaH'  , 'hemiLepThetaH'  , 100, -1., 1. )
    histoM1 = rt.TH1F('hemiLepThetaHM1', 'hemiLepThetaHM1', 100, -1., 1. )

  ##   histoP1 = rt.TH1F('hemiLepThetaHP1', 'hemiLepThetaHP1', 50 , 0., 250. )
##     histo   = rt.TH1F('hemiLepThetaH'  , 'hemiLepThetaH'  , 50 , 0., 250. )
##     histoM1 = rt.TH1F('hemiLepThetaHM1', 'hemiLepThetaHM1', 50 , 0., 250. )
   
    c = rt.TCanvas("c")
    tree       = file.Get("RMRTree")
    tree.Draw(">>elist","","entrylist")

    elist = rt.gDirectory.Get('elist')
    count = 0
    #print count
    while True:
        count+=1
        if (count%1000 == 0):
            print count
        entry = elist.Next()
        if entry == -1: break
        tree.GetEntry(entry)
       #tree.mStop ==225. and  tree.mLSP ==25. and
        if  tree.nJet >= 4 and tree.metFilter  and tree.nCSVM > 0 and tree.MR >= 350 and tree.RSQ >= 0.08 and tree.nMuonTight  == 1 :
         ##    histoP1.Fill(tree.muTight_pt[0],tree.polarizationWeightPlus1)
##             histo.Fill(tree.muTight_pt[0])
##             histoM1.Fill(tree.muTight_pt[0],tree.polarizationWeightMinus1)
            histoP1.Fill(tree.hemiLepThetaH,tree.polarizationWeightPlus1)
            histo.Fill(tree.hemiLepThetaH)
            histoM1.Fill(tree.hemiLepThetaH,tree.polarizationWeightMinus1)
             
    c.cd()
    c.SetLogy()
    leg = rt.TLegend(0.5,0.4,0.8,0.7)
    histoM1.SetLineColor(rt.kRed)
    histoM1.SetLineWidth(3)
    histoM1.Scale(1./histoM1.Integral())
    histoM1.SetTitle("hemiLepThetaH")
    #histoM1.SetTitle("pt muon(GeV)")
    leg.AddEntry(histoM1, "pol +1","lep")
    histoM1.Draw()
    histo.SetLineColor(rt.kBlack)
    histo.SetLineWidth(3)
    histo.Scale(1./histo.Integral())
    leg.AddEntry(histo, "any pol","lep")
    histo.Draw("SAME")
    histoP1.SetLineColor(rt.kBlue)
    histoP1.SetLineWidth(3)
    histoP1.Scale(1./histoP1.Integral())
    leg.AddEntry(histoP1, "pol -1","lep")
    histoP1.Draw("SAME")
    ## histoTTJets.SetLineColor(rt.kGreen)
##     histoTTJets.SetLineWidth(3)
##     histoTTJets.Scale(1./histoTTJets.Integral())
##     histoTTJets.Draw("SAME")
##     leg.AddEntry(histoTTJets, "TTjets","lep")
    leg.Draw("SAME")
    c.SaveAs(histoP1.GetName()+"large.png")
   # c.SaveAs("ptMu.png")
