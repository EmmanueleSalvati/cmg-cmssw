#! /usr/bin/env python

import ROOT as rt
import sys, pickle, pprint
from array import array

def GetXSecT2tt(mStop):

    Xsecs = {
        '200.0' : 18.5,
        '225.0' : 9.90,
        '250.0' : 5.57,
        '275.0' : 3.27,
        '300.0' : 2.00,
        '325.0' : 1.25,
        '350.0' : 0.81,
        '375.0' : 0.53,
        '400.0' : 0.36,
        '425.0' : 0.24,
        '450.0' : 0.17,
        '475.0' : 0.12,
        '500.0' : 0.086,
        '525.0' : 0.062,
        '550.0' : 0.045,
        '575.0' : 0.033,
        '600.0' : 0.025,
        '625.0' : 0.019,
        '650.0' : 0.014,
        '675.0' : 0.011,
        '700.0' : 0.0081,
        '725.0' : 0.0062,
        '750.0' : 0.0048,
        '775.0' : 0.0037,
        '800.0' : 0.0029
        }
    return Xsecs[mStop]

def GetNEvents(mStop, mLSP):

    if mLSP == '25.0' :
        pklFileName = '/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/SMS-T2tt_mStop-Combo.0_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY.pkl'
    else :
        pklFileName = '/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/SMS-T2tt_mStop-Combo_mLSP_'+str(mLSP)+'_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY.pkl'
    pklFile = open(pklFileName, 'rb')
    data    = pickle.load(pklFile)
    Nevents = data[(float(mStop), float(mLSP))]
    
    return Nevents

def GetScale(label, box, mStop = 0, mLSP = 0):

    CrossSections = {
        'TTjets': 225.2
        }
 
    Nevents = {
        'TTjets': 6923750.
        }

    if label == 'T2tt':
        CrossSections['T2tt']  =   GetXSecT2tt(mStop)
        Nevents['T2tt']        =   GetNEvents(mStop, mLSP)

    Br = {
        'Ele': 0.16,
        'Mu' : 0.16,
        'BJetHS' : 0.46,
        'BJetLS' : 0.46
        }

    return CrossSections[label]*Br[box]/Nevents[label]

def GetRatio(histos, histosRatio):
    
    histosRatio['TTjets'] = histos['rebinnedT2tt'].Clone("T2ttForRatio")
    histosRatio['TTjets'].Divide(histos['rebinnedTTjets'])
    print histos['rebinnedT2tt'].GetXaxis().GetXmin(), histos['rebinnedT2tt'].GetXaxis().GetXmax(), histos['rebinnedT2tt'].GetXaxis().GetNbins() 
    print histos['rebinnedTTjets'].GetXaxis().GetXmin(), histos['rebinnedTTjets'].GetXaxis().GetXmax(), histos['rebinnedTTjets'].GetXaxis().GetNbins() 
     
def SetStyle1D(histosRebinned, histo, lineColor, max, title, label, scale, var = "RSQ" ):

    histo.SetLineColor(lineColor)
    histo.SetTitle(title)
    histo.Scale(float(scale))
    histo.SetMinimum(0.00001)
   # histo.SetMaximum(max)
    
    #MRbins = array('d',[450.0, 500.0, 550.0, 650.0, 790.0, 1000.0, 1500.0, 2200.0, 3000.0, 4000.0])
    #histo.GetXaxis().Set(8, MRbins)
    ## if var == "MR":
##         histo.GetXaxis().Set(10, 450., 4000.)
##     else :
##         histo.GetXaxis().Set(10, 0.05, 1.)
   
    #histos['rebinned'+label] =  histo.Rebin(9,"rebinned"+label,MRbins)
    #histosRebinned['rebinned'+label] =  histo.Rebin(5,"rebinned"+label )
    histosRebinned['rebinned'+label] = histo

def mDelta(mStop, mLSP):
    mS = float(mStop)
    mX = float(mLSP)
    mDelta = (mS*mS - mX*mX)/mS

    return int(mDelta)

def massviemDelta(mStop, mLSP):
    mS = float(mStop)
    mX = float(mLSP)
    mDelta = (mS*mS - mX*mX)/mS

    return int(mDelta)

if __name__ == '__main__':

    box   = sys.argv[1]
    mLSP  = sys.argv[2]
    mStop = sys.argv[3]
    if box == 'Ele' or box == 'Mu':
        label = 'MR350.0_R0.22360679775'
    else :
        label = 'MR500.0_R0.22360679775'

    filenames = {
        'TTjets': '/data/wreece/RazorMultijet_2012/231112/Datasets/MC/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10_START53_V7A-v1-wreece_231112-Combo_MR450.0_R0.173205080757_Ele.root',
        'T2tt':'/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/Datasets/mLSP'+str(mLSP)+'/SMS-T2tt_mStop-Combo_mLSP_'+str(mLSP)+'_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY_'+label+'_'+str(mStop)+'_'+str(mLSP)+'_'+box+'.root'
        }

    rt.gROOT.ProcessLine(".L /afs/cern.ch/user/l/lucieg/scratch1/Ap18/CMGTools/CMSSW_5_3_9/src/CMGTools/Susy/python/Lucie/macros/GetHisto.C")
    from ROOT import GetHisto

    scale = GetScale('TTjets', box, 0, 0) /  GetScale('T2tt', box, mStop, mLSP)
   
    #MR
    histosMR = {}
    histosMRRebinned = {}
    histosMRRatio    = {}
    histosMR['TTjets']  = GetHisto(filenames['TTjets'], "MR", "TTjets", "MR > 450.")
    SetStyle1D(histosMRRebinned,histosMR['TTjets'], rt.kBlack, 10000, "MR;MR(GeV);", 'TTjets', scale, "MR")
    
    histosMR['T2tt']    = GetHisto(filenames['T2tt'], "MR", "T2tt", "MR > 450.")
    SetStyle1D(histosMRRebinned,histosMR['T2tt'], rt.kRed, 10000, "MR;MR(GeV);", 'T2tt', 1., "MR")

    #GetRatio(histosMRRebinned, histosMRRatio)
   

    #RSQ
    histosRSQ = {}
    histosRSQRebinned = {}
    histosRSQRatio    = {}
    
    histosRSQ['TTjets']  = GetHisto(filenames['TTjets'], "Rsq", "TTjets", "MR > 450.")
    SetStyle1D(histosRSQRebinned,histosRSQ['TTjets'], rt.kBlack, 10000, "RSQ;RSQ;", 'TTjets', scale)
  
    histosRSQ['T2tt']    = GetHisto(filenames['T2tt'], "Rsq", "T2tt", "MR > 450.")
    SetStyle1D(histosRSQRebinned,histosRSQ['T2tt'], rt.kRed, 10000, "RSQ;RSQ;", 'T2tt', 1.)

    #GetRatio(histosRSQRebinned, histosRSQRatio)
    
    #plot
    rt.gStyle.SetOptStat(0)
    c = rt.TCanvas("c"+'_'+box+'_'+mStop+'_'+mLSP,box+" mStop :"+mStop+" GeV, mLSP "+mLSP)
    c.Divide(2,1)
    leg = rt.TLegend(0.4,0.8,0.9,0.9)
    for key, h in histosMR.iteritems():
        leg.AddEntry(h, key, "lep")

    c.cd(1)
    c.GetPad(1).SetLogy()
    histosRSQRebinned['rebinnedTTjets'].Draw()
    histosRSQRebinned['rebinnedT2tt'].Draw("SAME")
    leg.Draw("SAME")

    c.cd(2)
    c.GetPad(2).SetLogy()
    histosMRRebinned['rebinnedTTjets'].Draw()
    histosMRRebinned['rebinnedT2tt'].Draw("SAME")
    mD = mDelta(mStop, mLSP)
    if mD > 500.:
        line = rt.TLine(mD,0.,mD,10000)
        line.SetLineWidth(2)
        line.SetLineColor(rt.kBlue)
        line.Draw("SAME")
        legMR = leg.Clone("legMR")
        legMR.AddEntry(line, "mDelta", 'l')
        legMR.Draw("SAME")
    else :
        text = rt.TLatex(0.45,0.7,"m\Delta = "+str(mD)+" GeV")
        text.SetNDC()
        text.Draw("SAME")
        leg.Draw("SAME")

    ## c.cd(3)
##     histosRSQRatio['TTjets'].Draw()

##     c.cd(4)
##     histosMRRatio['TTjets'].Draw()
   
    c.SaveAs("plots/"+c.GetName()+".png")
