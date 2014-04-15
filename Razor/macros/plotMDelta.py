#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
    
    h_mDelta     = rt.TH2F("h_mDelta","mDelta;mStop(GeV);mLSP(GeV);mDelta(GeV)", 32, 0., 800., 32, 0., 800. )
    h_mDeltaVsDM = rt.TH2F("h_mDeltaVsDM","mDelta vs mStop - mLSP;mStop - mLSP(GeV);mDelta(GeV)", 32, 0., 800., 32, 0., 800. )

    for mStop in range(200, 825, 25) :
        for mLSP in range(0, mStop - 175, 25):
            mDelta = (mStop*mStop - mLSP*mLSP) / mStop
            h_mDelta.Fill(float(mStop), float(mLSP), mDelta)
            h_mDeltaVsDM.Fill( mStop - mLSP, mDelta)

c = rt.TCanvas("mDelta.png", "mDelta.png", 700, 600)
h_mDelta.SetLabelSize(0.025,"X;Y;Z")
h_mDelta.SetTitleOffset(1.5,"X;Y;Z")
h_mDelta.Draw("LEGO")

c.SaveAs(c.GetName())

c1 = rt.TCanvas("mDeltaVsDM.png","mDeltaVsDM.png",600, 600)
h_mDeltaVsDM.SetMarkerStyle(21)
h_mDeltaVsDM.Draw()#"colz")
c1.SaveAs(c1.GetName())
