#!/usr/bin/env python
import re, sys
from array import array

import ROOT as rt


if __name__ == '__main__':

    directory = '/afs/cern.ch/work/l/lucieg/private/RazorMultiJet/'

    var = sys.argv[1]
    data = 'SingleMu'
    
    samples = {
        'A-QCD100To250' :directory+'QCD100To250/0/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root',
        'B-QCD1000ToInf':directory+'QCD1000ToInf/0/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root',
        'C-QCD250To500' :directory+'QCD250To500/0/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root',
        'D-QCD500To1000':directory+'QCD500To1000/0/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root',
        'E-DY':directory+'DY/0/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root',
        'F-WJets':directory+'WJets/0/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball-Summer12_DR53X-PU_S10_START53_V7A-v2-SUSY_MERGED.root',
        'G-T_tW':directory+'T_tW/0/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY.root',
        'H-Tbar_tW':directory+'Tbar_tW/0/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY.root',
        'I-TTJets':directory+'TTJets/0/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root',
        }
    data_samples = {
        'SingleEle':directory+'SingleElectron-Run2012ABCD-22Jan2013-v1-SUSY.root',
        'SingleMu':directory+'SingleMu-Run2012ABCD-22Jan2013-v1-SUSY.root',
#        'MultiJet':
        }
     
    xsections = {
        'DY'          : 2950.,
        'QCD1000ToInf': 204.,
        'QCD100To250' : 1.04e+07,
        'QCD250To500' : 276000.,
        'QCD500To1000': 8426.,
        'TTJets'      : 245.8,
        'T_tW'        : 10.7,
        'Tbar_tW'     : 10.7,
        'WJets'       : 48.01,
        }

    ngen = {
        'DY'          : 30459503.,
        'QCD1000ToInf': 13843863.,
        'QCD100To250' : 50129518.,
        'QCD250To500' : 27062078.,
        'QCD500To1000': 30599292.,
        'TTJets'      : 6923750.,
        'T_tW'        : 497658.,
        'Tbar_tW'     : 493460.,
        'WJets'       : 57709905., 
        }


    files    = {}
    histosVar = {}
    trees    = {}
    colors   = {
        'QCD100To250' : rt.kYellow,
        'QCD1000ToInf': rt.kYellow,
        'QCD250To500' : rt.kYellow,
        'QCD500To1000': rt.kYellow,
        'DY'          : rt.kOrange,
        'WJets'       : rt.kMagenta,
        'T_tW'        : rt.kCyan,
        'Tbar_tW'     : rt.kGreen,
        'TTJets'      : rt.kBlue,
        'SingleEle'   : rt.kBlack,
        'SingleMu'    : rt.kBlack,
        }

    
    cut  = {
        'SingleEle':'eleBoxFilter && nJetNoLeptons > 4  && eleTriggerFilter && nCSVM > 0 && MR >= 300. && RSQ >= 0.08 && nMuonTight == 0 && nElectronTight == 1 && nMuonLoose == 0 && nElectronLoose == 1 && !(isolatedTrack10LeptonFilter)',
        'SingleMu' :'muBoxFilter && nJetNoLeptons >4 && muTriggerFilter && nCSVM > 0 && MR >= 350. && RSQ >= 0.08 && nMuonTight == 1 && nElectronTight == 0 && nMuonLoose == 1 && nElectronLoose == 0 && !(isolatedTrack10LeptonFilter)',
     }
        
    stackVar = rt.THStack("stackVar","Var")
    count = 0
    leg = rt.TLegend(0.7,0.5,0.94,0.94)
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    MRbins = array('d',[400, 450, 550, 700, 900, 1200, 1600, 2000])#2500, 4000])
    Rsqbins = array('d',[0.08, 0.10, 0.15, 0.20,0.30,0.41,0.52,0.64,0.80,1.5])
    if var == 'MR':
        bins = MRbins
    else :
        bins = Rsqbins
    
###stack histo
    for sample, file in sorted(samples.iteritems()) :

        sample = re.sub('[A-Z]-','',sample)
        files[sample]    = rt.TFile(file)
        histosVar[sample] = rt.TH1F("histoVar"+sample, "histoVar"+sample, len(bins) -1 , bins)
        histosVar[sample].SetLineColor(colors[sample])
        histosVar[sample].SetFillColor(colors[sample])
        trees[sample]    = files[sample].Get('RMRTree')
        trees[sample].Project("histoVar"+sample, var, cut[data])
        histosVar[sample].Scale(19300.*xsections[sample]/ngen[sample])
        print sample, histosVar[sample].GetEntries()
        if sample.startswith('QCD') :
            if count == 0 :
                leg.AddEntry(histosVar[sample],'QCD',"f")
                count+=1
        else :
            leg.AddEntry(histosVar[sample],sample,"f")
        stackVar.Add(histosVar[sample])

    files[data]    = rt.TFile(data_samples[data])
    trees[data]    = files[data].Get('RMRTree')
    histosVar[data] = rt.TH1F("histoVar"+data, "histoVar"+data, len(bins) -1 , bins)
    trees[data].Project("histoVar"+data, var, cut[data])
    histosVar[data].Sumw2()
    histosVar[data].SetMarkerStyle(20)
    leg.AddEntry(histosVar[data],data,"lep")

    if var == 'MR' : title = 'MR (GeV)'
    else : title = var
    histosVar[data].GetXaxis().SetTitle(title)
    histosVar[data].GetXaxis().SetLabelOffset(0.08)
    histosVar[data].GetXaxis().SetLabelSize(0.15)
    histosVar[data].GetYaxis().SetLabelSize(0.06)
    histosVar[data].GetXaxis().SetTitleSize(0.22)
    histosVar[data].GetYaxis().SetTitleSize(0.07)
    histosVar[data].GetXaxis().SetTitleOffset(1.0)
    histosVar[data].GetYaxis().SetTitleOffset(0.7)
    histosVar[data].GetXaxis().SetTicks("+-")
    histosVar[data].GetXaxis().SetRange(1,histosVar[data].GetNbinsX())
    histosVar[data].GetYaxis().SetTitle("Events")
  

###ratio
    histoVarDataDivide = histosVar[data].Clone(histosVar[data].GetName()+"Divide")
    histoVarDataDivide.Sumw2()
    histoVarMCDivide = rt.TH1F("histoVar"+sample, "histoVar"+sample, 45 , 200., 2000.)
  
    for i in range(1, histoVarDataDivide.GetNbinsX()+1):

        tmpVal= 0
        for sample, histo in histosVar.iteritems():
            if sample.startswith('Single') :
                continue
            tmpVal+=histo.GetBinContent(i)
            
        if tmpVal != -0.:
            histoVarDataDivide.SetBinContent(i, histoVarDataDivide.GetBinContent(i)/tmpVal)
            histoVarDataDivide.SetBinError(i, histoVarDataDivide.GetBinError(i)/tmpVal)

    histoVarDataDivide.SetMaximum(3.0)
    histoVarDataDivide.SetMinimum(0.)
    histoVarDataDivide.GetYaxis().SetNdivisions(504,rt.kTRUE)
    histoVarDataDivide.GetYaxis().SetTitleOffset(0.2)
    histoVarDataDivide.GetYaxis().SetTitleSize(0.22)
    histoVarDataDivide.GetYaxis().SetTitle("Data/MC")
  

###draw
    c1 = rt.TCanvas("c1","c1", 500, 400)
    pad1 = rt.TPad("pad1","pad1",0,0.25,1,1)
    pad2 = rt.TPad("pad2","pad2",0,0,1,0.25)
    rt.gStyle.SetOptStat(0000)
    rt.gStyle.SetOptTitle(0)
   ##  pad1.Range(-213.4588,-0.3237935,4222.803,5.412602);
##     pad2.Range(-213.4588,-2.206896,4222.803,3.241379);

    pad1.SetLeftMargin(0.15)
    pad2.SetLeftMargin(0.15)
    pad1.SetRightMargin(0.05)
    pad2.SetRightMargin(0.05)
    pad1.SetTopMargin(0.05)
    pad2.SetTopMargin(0.)
    pad1.SetBottomMargin(0.)
    #pad2.SetTopMargin(0.04)
    #pad1.SetBottomMargin(0.004)
    pad2.SetBottomMargin(0.47)
   

    pad1.Draw()
    pad1.cd()
    rt.gPad.SetLogy()

    
    histosVar[data].Draw()
    stackVar.Draw("SAME")
    histosVar[data].Draw("SAME")
    leg.Draw("SAME")

    c1.cd()
    
    pad2.Draw()
    pad2.cd()
    rt.gPad.SetLogy(0)
    histoVarDataDivide.GetYaxis().SetLabelSize(0.15)
    histoVarDataDivide.Draw()

    

    
    c1.SaveAs(var+data+"gt4jets.png")
