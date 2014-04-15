#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re
from array import array

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

def binnedHisto2D(tree, binsX, binsY, label='') :

    histo = rt.TH2F("histo"+label, "histo"+label, 10, binsX, 8, binsY)

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
            
    if not( xsec == None ) :
        histo.Scale(19300.*xsec*eff / Ngen)
        print 19300.*xsec*eff / Ngen
        print Ngen
                      
    return histo


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)

    ######## Get Arguments
    box     = sys.argv[1]
    mLSP    = sys.argv[2]
    mStops  = sys.argv[3]
    nmStops = sys.argv[4]
    drawSideband = sys.argv[5]

    ########## binning def
    MRbins  = array('d',[350.0, 400.0, 450.0, 500.0, 550.0, 650.0, 790.0, 1000, 1500, 2200, 3000, 4000.0])
    Rsqbins = array('d',[0.05, 0.07, 0.12, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0])
 
    ###### SAMPLES
    #data
    directoryData = ''#'/data/wreece/RazorMultijet_2012/220113/'
    filenameData  = directoryData+'SingleElectron-Run2012ABCD-wreece_220113-Combo_MR350.0_R0.22360679775_'+box+'.root'
    fileData = rt.TFile(filenameData)
    treeData = fileData.Get("RMRTree")
    
    #signal
    directory = '/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/Datasets/mLSP' +str(mLSP)+'/'
    if box == 'BJetHS' or box == 'BJetLS':
        label  ='_MR500.0_R0.22360679775_'
    else :
        label  ='_MR350.0_R0.22360679775_'

    mStopmin = int(mStops)
    mStopmax = int(mStops)+int(nmStops)*25
    for mStop in range(mStopmin, mStopmax, 25):
         filename = directory+'SMS-T2tt_mStop-Combo_mLSP_'+str(mLSP)+'_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY'+label+str(mStop)+'.0_'+str(mLSP)+'_'+box +'.root'
         
         file = rt.TFile(filename)
         tree = file.Get("RMRTree")
         wHisto = file.Get("wHisto")
         eff = wHisto.Integral()
         print 'eff',eff
    
    
         ####### 2D plots
         sidebands = sidebandLines()
    
         c = rt.TCanvas("RsqMR2D_mStop%s_mLSP%s_box%s.png"%(mStop, mLSP, box), "RsqMR2D_mStop%s_mLSP%s_box%s.png"%(mStop, mLSP, box), 1160, 393)
         c.Divide(2,1)

         c.cd(1)
         c.GetPad(1).SetLogx()
         c.GetPad(1).SetLogy()
         histo = binnedHisto2D(tree, MRbins, Rsqbins, 'signal') 
         histo.SetTitle("Rsq vs MR, mStop = %s, mLSP = %s, signal, %s box;MR(GeV);Rsq"%(mStop, mLSP, box))
         histo.Draw("colz")
         if drawSideband :
              for line in sidebands:
                   line.Draw("SAME")
         c.cd(2)
         c.GetPad(2).SetLogx()
         c.GetPad(2).SetLogy()
         histoData = binnedHisto2D(treeData, MRbins, Rsqbins, 'data') 
         histoData.SetTitle("Rsq vs MR, data, %s box;MR(GeV);Rsq"%box)
         histoData.Draw("colz")
         if drawSideband :
              for line in sidebands:
                   line.Draw("SAME")
         c.SaveAs(c.GetName())


         ####### 1D plots
         leg = rt.TLegend(0.6,0.7,0.9,0.9)
    
         c1D = rt.TCanvas("RsqMR_mStop%s_mLSP%s_box%s.png"%(mStop, mLSP, box), "RsqMR_mStop%s_mLSP%s_box%s.png"%(mStop, mLSP, box), 1160, 393)
         c1D.Divide(2,1)
         c1D.cd(1)
         c1D.GetPad(1).SetLogy()
         histoRsq = binnedHisto1D(tree, Rsqbins, "Rsq",'signal', 10.0,eff) 
         histoRsq.SetTitle("Rsq, %s box;Rsq;"%(box))
         histoRsq.SetLineColor(rt.kRed)
         histoRsq.SetLineWidth(3)
         histoRsqData = binnedHisto1D(treeData, Rsqbins, "Rsq",'data') 
         histoRsqData.SetTitle("Rsq, %s box;Rsq;"%box)
         histoRsqData.SetLineColor(rt.kBlack)
         histoRsqData.SetLineWidth(3)
         histoRsqData.SetMarkerStyle(22)
         histoRsqData.Draw()
         histoRsq.Draw("SAMES")
         histoRsqSum = histoRsqData.Clone("histoRsqSum")
         histoRsqSum.Add(histoRsq)
         histoRsqSum.SetLineColor(rt.kBlue)
         histoRsqSum.SetLineWidth(3)
         histoRsqSum.SetMarkerStyle(1)
         histoRsqSum.Draw("SAMES")
         #histoRsqData.Draw("E, SAMES")
         leg.AddEntry(histoRsqData, "data", "lep")
         leg.AddEntry(histoRsq, "signal", "lep")
         leg.AddEntry(histoRsqSum, "data+signal", "lep")
         leg.Draw("SAMES")
         
         c1D.cd(2)
         c1D.GetPad(2).SetLogy()
         histoMR  = binnedHisto1D(tree, MRbins, "MR",'signal', 10.0,eff)
         histoMR.SetTitle("MR, %s box;MR(GeV);"%(box))
         histoMR.SetLineColor(rt.kRed)
         histoMR.SetLineWidth(3)
         histoMRData = binnedHisto1D(treeData, MRbins, "MR",'data') 
         histoMRData.SetTitle("MR,%s box;MR;"%box)
         histoMRData.SetLineColor(rt.kBlack)
         histoMRData.SetLineWidth(3)
         histoMRData.SetMarkerStyle(22)
         histoMRData.Draw()
         histoMR.Draw("SAMES")
         histoMRSum = histoMRData.Clone("histoMRSum")
         histoMRSum.Add(histoMR)
         histoMRSum.SetLineColor(rt.kBlue)
         histoMRSum.SetLineWidth(3)
         histoMRSum.Draw("SAMES")
         #histoMRData.Draw("E, SAMES")
         leg.Draw("SAMES")
         c1D.SaveAs(c1D.GetName())
