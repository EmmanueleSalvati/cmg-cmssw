#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
    
    box            = sys.argv[1]
    directory      = sys.argv[2]
    
    efficiencyMap = rt.TH2F("effMap","efficiency map for "+box, 32, 0., 800., 32, 0., 800. )

    for mLSP in range(25, 725, 25):
        dir = directory+'/mLSP'+str(mLSP)+'.0/'
        
        for filename in os.listdir(dir) :
            print filename
            box_result = re.search(str(box),str(filename))
       
            if box_result :
                file = rt.TFile.Open(dir+'/'+filename)
                massPoint = re.findall("[0-9]+.0_[0-9]+.0",filename)
                mStop, mLSP = re.split("_", massPoint[0])
                wHisto = file.Get("wHisto")
                eff = wHisto.Integral()
                efficiencyMap.Fill(float(mStop), float(mLSP), eff)

c = rt.TCanvas("efficiencyMap"+str(box)+".png")
efficiencyMap.Draw("colz")
c.SaveAs(c.GetName())
