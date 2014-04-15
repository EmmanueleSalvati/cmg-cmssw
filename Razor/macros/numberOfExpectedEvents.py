#! /usr/bin/env python

import ROOT as rt
import os.path
import sys, glob, re, pickle, pprint
from array import array

def getXsec() :

    xsec = {
        125:[197.122,    15.7303],
        150:[80.268,     15.7303],
        175:[36.7994,    15.1749],
        200:[18.5245,    14.9147],
        225:[9.90959,    14.9662],
        250:[5.57596,    14.7529],
        275:[3.2781,     14.7341],
        300:[1.99608,    14.6905],
        325:[1.25277,    14.2875],
        350:[0.807323,   14.3597],
        375:[0.531443,   14.266],
        400:[0.35683,    14.2848],
        425:[0.243755,   14.0504],
        450:[0.169668,   14.2368],
        475:[0.119275,   14.6664],
        500:[0.0855847,  14.9611],
        525:[0.0618641,  15.4135],
        550:[0.0452067,  15.8177],
        575:[0.0333988,  16.2132],
        600:[0.0248009,  16.6406],
        625:[0.0185257,  17.0835],
        650:[0.0139566,  17.56],
        675:[0.0106123,  17.9891],
        700:[0.0081141,  18.4146],
        725:[0.00623244, 18.8796],
        750:[0.00480639, 19.4088],
        775:[0.00372717, 19.9097],
        800:[0.00289588, 20.516]
        }

    return xsec


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
   
    mStop    = array('d',range(125, 825, 25))
    mStoperr = array('d',[0., 0., 0., 0., 0., 0., 0., 0.])
    xsecs    = getXsec()
    xsec     = [ v[0] for key, v in sorted(xsecs.iteritems()) ]
    xsecerr  = [ v[0]*v[1]/100. for key, v in sorted(xsecs.iteritems()) ]
    
    nevents    =  array('d',[20000*x for x in xsec])
    neventserr = array('d',[20000*x for x in xsecerr])

    g = rt.TGraphErrors(28, mStop, nevents, mStoperr, neventserr)
    g.SetTitle("number of expected events with 20fb-1 at 8TeV;mStop(GeV)")
    c = rt.TCanvas("numberOfExpectedEvents.png")
    c.SetLogy()
    g.Draw("AP")
    c.SaveAs(c.GetName())
