#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re
from array import array
from math import sqrt


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)

    file = rt.TFile('/afs/cern.ch/work/l/lucieg/private/RazorMultiJet/SMS-T2tt_mStop-150to350_mLSP-0to250_8TeV-Pythia6Z/0/SMS-T2tt_mStop-150to350_mLSP-0to250_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY_MERGED.root')
    #file = rt.TFile('/afs/cern.ch/work/l/lucieg/private/RazorMultiJet/SMS-T2tt_mStop-675to800_mLSP-0to275_8TeV-Pythia6Z/25/SMS-T2tt_mStop-675to800_mLSP-0to275_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY.root')

    file2 = rt.TFile('/afs/cern.ch/work/l/lucieg/private/RazorMultiJet/TTJets/0/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root')
    histoTTJets = rt.TH1F('hemi2ThetaHTTJets', 'hemi2ThetaHTTJets', 50, -1., 1. )
    tree2       = file2.Get("RMRTree")
    cut = ' nJet >= 6 && metFilter && hadBoxFilter && hadTriggerFilter && nCSVM > 0 && MR >= 350 && RSQ >= 0.03 && nMuonTight == 0 && nElectronTight == 0 && !(isolatedTrack10Filter) && nMuonLoose == 0 && nElectronLoose == 0'
    tree2.Project('hemi2ThetaHTTJets','hemi2ThetaH', cut)

    sample = 'T2tt'
    histoP1 = rt.TH1F('hemi2ThetaHP1_'+sample, 'hemi2ThetaHP1_'+sample, 50, -1., 1. )
    histo = rt.TH1F('hemi2ThetaH_'+sample, 'hemi2ThetaH_'+sample, 50, -1., 1. )
    histoM1 = rt.TH1F('hemi2ThetaHM1_'+sample, 'hemi2ThetaHM1_'+sample, 50, -1., 1. )

    c = rt.TCanvas("c")
    tree       = file.Get("RMRTree")
    tree.Draw(">>elist","","entrylist")

    elist = rt.gDirectory.Get('elist')
    count = 0
    print count
    while True:
        count+=1
        #if count > 50 : break
        print count
        entry = elist.Next()
        if entry == -1: break
        tree.GetEntry(entry)
        # print tree.hemi2ThetaH,tree.polarizationWeightMinus1
        #if True :
        if tree.mStop ==250. and tree.nJet >= 6 and tree.metFilter and tree.hadBoxFilter and tree.hadTriggerFilter and tree.nCSVM > 0 and tree.MR >= 350 and tree.RSQ >= 0.03 and tree.nMuonTight == 0 and tree.nElectronTight == 0 and not tree.isolatedTrack10Filter and tree.nMuonLoose == 0 and tree.nElectronLoose == 0 :
            histoP1.Fill(tree.hemi2ThetaH,tree.polarizationWeightPlus1)
            histo.Fill(tree.hemi2ThetaH)
            histoM1.Fill(tree.hemi2ThetaH,tree.polarizationWeightMinus1)
             
    c.cd()
    leg = rt.TLegend(0.5,0.1,0.8,0.4)
    histoP1.SetLineColor(rt.kRed)
    histoP1.SetLineWidth(3)
    histoP1.Scale(1./histoP1.Integral())
    histoP1.SetTitle("hemi2ThetaH")
    leg.AddEntry(histoP1, "pol +1","lep")
    histoP1.Draw()
    histo.SetLineColor(rt.kBlack)
    histo.SetLineWidth(3)
    histo.Scale(1./histo.Integral())
    leg.AddEntry(histo, "any pol","lep")
    histo.Draw("SAME")
    histoM1.SetLineColor(rt.kBlue)
    histoM1.SetLineWidth(3)
    histoM1.Scale(1./histoM1.Integral())
    leg.AddEntry(histoM1, "pol -1","lep")
    histoM1.Draw("SAME")
    histoTTJets.SetLineColor(rt.kGreen)
    histoTTJets.SetLineWidth(3)
    histoTTJets.Scale(1./histoTTJets.Integral())
    histoTTJets.Draw("SAME")
    leg.AddEntry(histoTTJets, "TTjets","lep")
    leg.Draw("SAME")
    c.SaveAs(histoP1.GetName()+"allHadBoxSel.png")
