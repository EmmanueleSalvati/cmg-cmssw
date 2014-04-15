import CMGTools.RootTools.fwlite.Config as cfg

from   CMGTools.H2TauTau.proto.samples.getFiles import getFiles

ana = cfg.Analyzer(
    'MultiJetAnalysis',
    verbose = False,
    )

filesT2tt    = getFiles('/SMS-T2tt_mStop-375to475_mLSP-0to375_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/RZR/', 'lucieg', 'razorTuple_*.*root')
filesT2tt.extend(getFiles('/SMS-T2tt_mStop-675to800_mLSP-0to275_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/RZR/', 'lucieg', 'razorTuple_*.*root'))
filesT2tt.extend(getFiles('/SMS-T2tt_mStop-500to650_mLSP-0to225_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/RZR/', 'lucieg', 'razorTuple_*.*root'))
filesT2tt.extend(getFiles('/SMS-T2tt_mStop-150to350_mLSP-0to250_8TeV-Pythia6Z/Summer12-START52_V9_FSIM-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/RZR/', 'lucieg', 'razorTuple_*.*root'))


filesTTJets  = getFiles('/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/RZR/', 'lucieg', 'razorTuple_*.*root')
filesQCD100  = getFiles('/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/RZR/', 'lucieg', 'razorTuple_*.*root')
filesQCD250  = getFiles('/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/RZR/', 'lucieg', 'razorTuple_*.*root')
filesQCD500  = getFiles('/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/RZR/', 'lucieg', 'razorTuple_*.*root')
filesQCD1000 = getFiles('/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/V5_B/PAT_CMG_V5_17_0/RZR/', 'lucieg', 'razorTuple_*.*root')

T2tt={}

nGenEvents = {200:92564., 300:95031.,400:121987.,500:228109.,600:227383., 700:108186., 800:118669.}
xSections = {200:18.5245, 300:1.99608,400:0.35683,500:0.0855847,600:0.0248009, 700:0.0081141, 800:0.00289588}
#xSections = {200:18.5245, 300:1.99608,400:0.35683,500:0.0855847,600:10}

for ms in range(200, 900, 100):
    T2tt["T2tt_"+str(ms)] = cfg.MCComponent(
        name          = 'T2tt_'+str(ms),
        files         = filesT2tt,
        xSection      = xSections[ms], 
        nGenEvents    = nGenEvents[ms],
        intLumi       = 19300.,
        triggers      = [],
        effCorrFactor = 1,
        mStop         = float(ms)
        )
    T2tt["T2tt_"+str(ms)].splitFactor = 20


TTJets = cfg.MCComponent(
    name          = 'TTJets',
    files         = filesTTJets,
    xSection      = 157.5, #225.5,#
    nGenEvents    = 6885720,
    triggers      = [],
    effCorrFactor = 1,
    intLumi       = 19300.,
    mStop         = 0.0)
TTJets.splitFactor = 35

QCD100 = cfg.MCComponent(
    name          = 'QCD100',
    files         = filesQCD100,
    xSection      = 1.04e+07, #45 438 419
    nGenEvents    = 8998668,
    triggers      = [],
    effCorrFactor = 1,
    intLumi       = 19300,
    mStop         = 0.0)
QCD100.splitFactor = 100

QCD250 = cfg.MCComponent(
    name          = 'QCD250',
    files         = filesQCD250,
    xSection      = 276000., 
    nGenEvents    = 2.697391e+07,
    triggers      = [],
    effCorrFactor = 1,
    intLumi       = 19300,
    mStop         = 0.0)
QCD250.splitFactor = 100

QCD500 = cfg.MCComponent(
    name          = 'QCD500',
    files         = filesQCD500,
    xSection      = 8426., 
    nGenEvents    = 2.965658e+07,
    triggers      = [],
    effCorrFactor = 1,
    intLumi       = 19300,
    mStop         = 0.0)
QCD500.splitFactor = 100

QCD1000 = cfg.MCComponent(
    name          = 'QCD1000',
    files         = filesQCD1000,
    xSection      = 204., 
    nGenEvents    = 1.378617e+07,#13623774
    triggers      = [],
    effCorrFactor = 1,
    intLumi       = 19300,
    mStop         = 0.0)
QCD1000.splitFactor = 100

selectedComponents= [T2tt[key] for key in T2tt.keys()]
#selectedComponents=[T2tt['T2tt_400']]
## selectedComponents.append(TTJets)
## selectedComponents.append(QCD100)
## selectedComponents.append(QCD250)
## selectedComponents.append(QCD500)
## selectedComponents.append(QCD1000)


print selectedComponents

sequence = cfg.Sequence( [
    ana
    ] )

config = cfg.Config( components = selectedComponents,
                     sequence = sequence )





