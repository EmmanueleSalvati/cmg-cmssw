#!/usr/bin/env python

import ROOT as rt


if __name__ == '__main__':

    directory = '/afs/cern.ch/work/l/lucieg/private/RazorMultiJet/'

    samples = {
        'DY':directory+'DY/0/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root',
        'QCD1000ToInf':directory+'QCD1000ToInf/0/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root',
        'QCD100To250' :directory+'QCD100To250/0/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root',
        'QCD250To500' :directory+'QCD250To500/0/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root',
        'QCD500To1000':directory+'QCD500To1000/0/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY_MERGED.root',
        'TTJets':directory+'TTJets_old/0/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10_START53_V7C-v1-SUSY.root',
        'T_tW':directory+'T_tW/0/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY.root',
        'Tbar_tW':directory+'Tbar_tW/0/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola-Summer12_DR53X-PU_S10_START53_V7A-v1-SUSY.root',
        'WJets':directory+'WJets/0/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball-Summer12_DR53X-PU_S10_START53_V7A-v2-SUSY_MERGED.root',
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
    histosRSQ = {}
    trees    = {}
    colors   = {
        'DY'          : rt.kCyan,
        'QCD1000ToInf': rt.kYellow,
        'QCD100To250' : rt.kYellow,
        'QCD250To500' : rt.kYellow,
        'QCD500To1000': rt.kYellow,
        'TTJets'      : rt.kBlue,
        'T_tW'        : rt.kBlack,
        'Tbar_tW'     : rt.kGreen,
        'WJets'       : rt.kMagenta,
        'SingleEle'   : rt.kBlack,
        'SingleMu'    : rt.kBlack,
        }

    data = 'SingleEle'
    cut  = {
        'SingleEle':'eleBoxFilter && nJetNoLeptons == 4  && eleTriggerFilter && nCSVM > 0 && MR >= 350. && RSQ >= 0.08 && nMuonTight == 0 && nElectronTight == 1 && nMuonLoose == 0 && nElectronLoose == 1 && !(isolatedTrack10LeptonFilter)',
        'SingleMu' :'muBoxFilter && nJetNoLeptons ==4 && muTriggerFilter && nCSVM > 0 && MR >= 350. && RSQ >= 0.08 && nMuonTight == 1 && nElectronTight == 0 && nMuonLoose == 1 && nElectronLoose == 0 && !(isolatedTrack10LeptonFilter)',
     }
        
    stackRSQ = rt.THStack("stackRSQ","RSQ")
    count = 0
    leg = rt.TLegend(0.5,0.5,0.9,0.9)
    for sample, file in samples.iteritems() :
        
        files[sample]    = rt.TFile(file)
        histosRSQ[sample] = rt.TH1F("histoRSQ"+sample, "histoRSQ"+sample, 15 , 0., 1.5)
        histosRSQ[sample].SetLineColor(colors[sample])
        histosRSQ[sample].SetFillColor(colors[sample])
        trees[sample]    = files[sample].Get('RMRTree')
        trees[sample].Project("histoRSQ"+sample, 'RSQ', cut[data])
        histosRSQ[sample].Scale(19300.*xsections[sample]/ngen[sample])
        if sample.startswith('QCD') :
            if count == 0 :
                leg.AddEntry(histosRSQ[sample],'QCD',"f")
                count+=1
        else :
            leg.AddEntry(histosRSQ[sample],sample,"f")
        stackRSQ.Add(histosRSQ[sample])

    files[data]    = rt.TFile(data_samples[data])
    trees[data]    = files[data].Get('RMRTree')
    histosRSQ[data] = rt.TH1F("histoRSQ"+data, "histoRSQ"+data, 15 , 0., 1.5)
    trees[data].Project("histoRSQ"+data, 'RSQ', cut[data])
    histosRSQ[data].Sumw2()
    histosRSQ[data].SetMarkerStyle(20)
    leg.AddEntry(histosRSQ[data],data,"lep")

    c1 = rt.TCanvas("c1","c1", 500, 400)
  ##   pad1 = rt.TPad("pad1","pad1",0,0.25,1,1)
##     pad2 = rt.TPad("pad2","pad2",0,0,1,0.25)
    rt.gStyle.SetOptStat(0000)
    rt.gStyle.SetOptTitle(0)
    #pad1.Range(-213.4588,-0.3237935,4222.803,5.412602);
    #pad2.Range(-213.4588,-2.206896,4222.803,3.241379);

    ## pad1.SetLeftMargin(0.15)
##     pad2.SetLeftMargin(0.15)
##     pad1.SetRightMargin(0.05)
##     pad2.SetRightMargin(0.05)
##     pad1.SetTopMargin(0.05)
##     pad2.SetTopMargin(0.)
##    pad1.SetBottomMargin(0.01)
##     #pad2.SetTopMargin(0.04)
##     #pad1.SetBottomMargin(0.004)
##     pad2.SetBottomMargin(0.47)
    
##     pad1.Draw()
##     pad1.cd()
##    rt.gPad.SetLogy()
    c1.SetLogy()
    stackRSQ.Draw()
    histosRSQ[data].Draw("SAME")
    leg.Draw("SAME")


   ##  pad2.Draw()
##     pad2.cd()
##     rt.gPad.SetLogy(0)
    
  ##   histoRSQDataDivide = histosRSQ[data].Clone(histosRSQ[data].GetName()+"Divide")
##     histoRSQDataDivide.Sumw2()
##     histoRSQMCDivide = histosRSQ[data].Clone(histosRSQ[data].GetName()+"Divide")
##     histoRSQMCDivide.Sumw2()


    
    c1.SaveAs("RSQ"+data+".png")

   ##  for sample, histo in histosRSQ.iteritems() :
        
##         if count == 0 :
##             histo.Draw()
##             count+=1
##         else :
##             histo.Draw("SAME")
