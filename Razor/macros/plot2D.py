#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re
from array import array
from math import sqrt

def line(x1, x2, y1, y2):
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

def mDeltaLine(mDelta):

     lmDelta = line(mDelta, 0., mDelta, 1.)

     return lmDelta

def binnedHisto2D(tree, binsX, binsY, label='') :

    histo = rt.TH2F("histo"+label, "histo"+label, len(binsX) -1, binsX, len(binsY) -1, binsY)
   
    for i_binx in range(0, len(binsX) - 1):
        for i_biny in range(0, len(binsY) - 1):
        
            binx     = binsX[i_binx]
            binx_p1  = binsX[i_binx+1]
            biny     = binsY[i_biny]
            biny_p1  = binsY[i_biny+1]
            
            numEntries = (tree.reduce("MR > %s && MR < %s && Rsq > %s && Rsq < %s"%(binx, binx_p1, biny, biny_p1)).numEntries())
            histo.Fill(binx, biny, numEntries)

    return histo

def binnedHisto1D(tree, binsX, varName, label='', xsec = None, eff = None) :

    histo = rt.TH1F("histo1D"+varName+label, "histo1D"+varName+label , len(binsX) -1, binsX)
    
    Ngen = 0.
    for i_binx in range(0, len(binsX) - 1):
        
            binx     = binsX[i_binx]
            binx_p1  = binsX[i_binx+1]
                       
            numEntries = (tree.reduce("%s >= %s && %s <= %s"%(varName, binx, varName, binx_p1)).numEntries())
            Ngen+=numEntries
            histo.Fill(binx, numEntries)

    integral = histo.Integral()
    print integral
    histo.Scale(1./integral)
  ##   if not( xsec == None ) :
##         histo.Scale(19300.*xsec*eff / Ngen)
                             
    return histo


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
             
    ######## Get Arguments
    box     = sys.argv[1]
    mLSP    = float(sys.argv[2])
    mStops  = int(sys.argv[3])
    nmStops = int(sys.argv[4])
    drawSideband = False

    ########## binning def
   # MRbins  = array('d',[350.0,  450.0, 550.0, 650.0, 790.0, 1000, 1500, 2200, 3000, 4000.0])
   # Rsqbins = array('d',[0.05, 0.07, 0.12, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0])
    MRbins  = array('d',[350.0, 450.0, 600.0, 800.0, 1050.0, 1500.0, 2200.0, 3000.0, 4000.0])
    Rsqbins = array('d',[0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
 
    ###### SAMPLES
    #signal
    directory = '/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/Datasets/mLSP' +str(mLSP)+'/'
    if box == 'BJetHS' or box == 'BJetLS':
        label  ='_MR500.0_R0.22360679775_'
    else :
        label  ='_MR350.0_R0.22360679775_'

    mStopmin = mStops
    mStopmax = mStops+nmStops*100

    histoRsqs = {}
    histoMRs  = {}
    files     = {}
    trees     = {}
    mDelta    = {}
    massivemDelta = {}
    
    for mStop in range(mStopmin, mStopmax, 100):
         filename = directory+'SMS-T2tt_mStop-Combo_mLSP_'+str(mLSP)+'_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY'+label+str(mStop)+'.0_'+str(mLSP)+'_'+box +'.root'
   # mStop = mStops
   # for mLSP in range(100., 700., 100):
   #      directory = '/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/Datasets/mLSP' +str(mLSP)+'.0/' 
    #     filename = directory+'SMS-T2tt_mStop-Combo_mLSP_'+str(mLSP)+'.0_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY'+label+str(mStop)+'.0_'+str(mLSP)+'.0_'+box +'.root'
         
         files[filename]   = rt.TFile(filename)
         trees[filename]   = files[filename].Get("RMRTree")
         wHisto = files[filename].Get("wHisto")
         eff    = wHisto.Integral()
         print 'eff',eff

         mDelta[mStop]        = (mStop*mStop - mLSP*mLSP) / (1.*mStop)
         massivemDelta[mStop] = 0
         if mStop > mLSP+175.:
              massivemDelta[mStop] = sqrt((mStop*mStop - (mLSP - 176.)*(mLSP - 176.))*(mStop*mStop - (mLSP + 176.)*(mLSP + 176.)))/ (1.*mStop)

         ####### 2D plots
         sidebands = sidebandLines()
    
         c = rt.TCanvas("plots/RsqMR2D_mStop%s_mLSP%s_box%s.png"%(mStop, mLSP, box), "RsqMR2D_mStop%s_mLSP%s_box%s.png"%(mStop, mLSP, box))
        
         c.cd()
         c.SetLogx()
         c.SetLogy()
         histo = binnedHisto2D(trees[filename], MRbins, Rsqbins, 'signal') 
         histo.SetTitle("Rsq vs MR, mStop = %s, mLSP = %s, signal, %s box;MR(GeV);Rsq"%(mStop, mLSP, box))
         histo.Draw("colz")
         if drawSideband :
              for line in sidebands:
                   line.Draw("SAME")
         if mDelta[mStop] > 350.:
              print mStop
              print mDelta[mStop]
              lmDelta = mDeltaLine(mDelta[mStop])
              lmDelta.SetLineColor(rt.kBlue)
         if massivemDelta[mStop] > 350.:
              print massivemDelta[mStop]
              lmassivemDelta = mDeltaLine(massivemDelta[mStop])
              lmDelta.Draw("SAME")
              lmassivemDelta.Draw("SAME")
         
         text = rt.TLatex()
         text.SetTextColor(rt.kBlue)
         text.DrawLatex(1500, 0.8, "m_\Delta="+str(int(mDelta[mStop]))+" GeV")
         text.SetTextColor(rt.kBlack)
         text.DrawLatex(1500, 0.6, "massive m_\Delta="+str(int(massivemDelta[mStop]))+" GeV")
         text.Draw("SAME")
         c.SaveAs(c.GetName())
         
         ####### 1D plots
         leg = rt.TLegend(0.6,0.7,0.9,0.9)
    
         histoRsq = binnedHisto1D(trees[filename], Rsqbins, "Rsq",str(mStop), 10.0,eff) 
         histoRsq.SetTitle("Rsq, %s box mStop : %sGeV, mLSP : %s GeV;Rsq;"%(box, str(mStop), str(mLSP)))
         histoRsq.SetLineColor(rt.kRed)
         histoRsq.SetLineWidth(3)
         histoRsq.SetMaximum(1)
         histoRsqs[mStop]= histoRsq

         histoMR  = binnedHisto1D(trees[filename], MRbins, "MR",'signal', 10.0,eff)
         histoMR.SetTitle("MR, %s box mStop : %sGeV, mLSP : %s GeV;MR(GeV);"%(box, str(mStop), str(mLSP)))
         histoMR.SetLineColor(rt.kRed)
         histoMR.SetLineWidth(3)
         histoMR.SetMaximum(1)
         histoMRs[mStop]=histoMR

    c1D = rt.TCanvas("plots/Rsq_mLSP%s_box%s.png"%(mLSP, box), "Rsq_mLSP%s_box%s.png"%(mLSP, box))
    c1D.cd()
    c1D.SetLogy()
    leg = rt.TLegend(0.6,0.6,0.9,0.9)
    n = 0
    for key, h in sorted(histoRsqs.iteritems()):
         if n == 0:
              h.SetLineColor(rt.kBlack)
              h.Draw()
              leg.AddEntry(h, "mLSP="+str(key)+"GeV","lep")
         else :
              h.SetLineColor(rt.kBlack+n)
              h.Draw("SAME")
              leg.AddEntry(h, "mLSP="+str(key)+"GeV","lep")
         n+=1
    leg.Draw("SAME")
    c1D.SaveAs(c1D.GetName())
         
    c1D1 = rt.TCanvas("plots/MR_mLSP%s_box%s.png"%(mLSP, box), "MR__mLSP%s_box%s.png"%(mLSP, box))
    c1D1.cd()
    c1D1.SetLogy()
    legMR = rt.TLegend(0.4,0.6,0.9,0.9)
    n = 0
    for key, h in sorted(histoMRs.iteritems()):
         if n == 0:
              h.SetLineColor(rt.kBlack)
              h.Draw()
              #text = rt.TLatex(0.,0.,"mLSP="+str(key)+"GeV, m_\Delta="+str(int(mDelta[key]))+" GeV")
              legMR.AddEntry(h, "mLSP="+str(key)+"GeV, mD="+str(int(mDelta[key]))+" GeV","lep")
         else :
              h.SetLineColor(rt.kBlack+n)
              h.Draw("SAME")
              legMR.AddEntry(h, "mLSP="+str(key)+"GeV, mD="+str(int(mDelta[key]))+" GeV","lep")
         n+=1
    legMR.Draw("SAME")
    c1D1.SaveAs(c1D1.GetName())
