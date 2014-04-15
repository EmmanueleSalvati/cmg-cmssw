#! /usr/bin/env python

import ROOT as rt

if __name__ == '__main__':

    rt.gROOT.ProcessLine(".L /afs/cern.ch/user/l/lucieg/scratch1/Ap18/CMGTools/CMSSW_5_3_9/src/CMGTools/Susy/python/Lucie/macros/plotDistrib.C")
    from ROOT import plotDistrib

    boxes = ["Ele", "Mu", "BJetHS", "BJetLS"]
    for box in boxes :

        for mStop in range(150, 825, 25) :
            for mLSP in range(25, 50, 25):#, mStop - 100, 25) :
                plotDistrib( str(float(mStop)), str(float(mLSP)), mStop, mLSP,box)


        #plotDistrib("150.0","25.0","Mu")
