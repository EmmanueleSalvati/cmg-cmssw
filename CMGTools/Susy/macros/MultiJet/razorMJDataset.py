#!/usr/bin/env python

import ROOT as rt
from ROOT import std
import array, os, sys, math, glob, pickle
from DataFormats.FWLite import Events, Handle
from CMGTools.RootTools import RootFile
from razorMJTopTag import topTag, calcHelicityLep
from histoSMSTree import getBoxGenLevel, getBox

def listDirectory(dir, inputFiles, maxFiles):
    if not os.path.exists(dir):
        raise Exception("The directory '%s' does not exist" % dir)
    files = glob.glob('%s/*.root' % dir)
    if len(files) > maxFiles:
        files = files[:maxFiles]
    inputFiles.extend(files)
    return len(files)

def getFiles(datasets, user, pattern):

    from CMGTools.Production.datasetToSource import datasetToSource

    files = []
    print '-------------------',pattern
    for d in datasets:
        print d
        ds = datasetToSource(
                             'lucieg',
                             #os.environ['USER'],
                             d,
                             pattern
                             )
        files.extend(ds.fileNames)
    print files[:1]
##     return  ['file:../../susy_tree_CMG_0.root']
    return ['root://eoscms//eos/cms%s' % f for f in files]

def deltaR(a,b):
    deta = a.eta() - b.eta()
    dphi = a.phi() - b.phi()
    dr = deta*deta + dphi*dphi
    return math.sqrt(dr)

def mt(j, met):
    result = 2*j.pt()*met.et()*(1-math.cos(j.phi()-met.phi()))
    return math.sqrt(result)

def mct(calc, h1, h2):
    v1 = array.array('d')
    v2 = array.array('d')

    v1.extend([h1.E(),h1.Px(),h1.Py(),h1.Pz()])
    v2.extend([h2.E(),h2.Px(),h2.Py(),h2.Pz()])

    return calc.mct(v1,v2)

if __name__ == '__main__':

    skimEvents = False

    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideAboutPythonConfigFile#VarParsing_Example
    from FWCore.ParameterSet.VarParsing import VarParsing
    options = VarParsing ('python')
    options.outputFile = None
    options.register ('inputDirectory',
                  None, # default value
                  VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.varType.string,          # string, int, or float
                  "A directory to read root files from")
    options.register ('outputDirectory',
                  '.', # default value
                  VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.varType.string,          # string, int, or float
                  "A directory to write root files to")
    options.register ('datasetName',
                  None,
                  VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.varType.string,          # string, int, or float
                  "A directory to read root files from")
    options.register ('maxFiles',
                  -1, # default value
                  VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.varType.int,          # string, int, or float
                  "The maximum number of files to read")
    options.register ('index',
                  -1, # default value
                  VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.varType.int,          # string, int, or float
                  "The file index to run on")
    options.register ('model',
                  None,
                  VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.varType.string,          # string, int, or float
                  "The SMS model to use in the error calculation")
    options.register ('runOnMC',
                  False,
                  VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.varType.bool,          # string, int, or float
                  "Run on MC or data")

    options.register ('mLSP',
                  0,
                  VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.varType.float,          # string, int, or float
                  "LSP mass")
    options.register ('mStop',
                  0,
                  VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.varType.float,          # string, int, or float
                  "stop mass")

    options.parseArguments()
    runOnMC = options.runOnMC
    mLSPskim = float(options.mLSP)
    mStopSkim = float(options.mStop)

    runSMS = True
    if options.datasetName:
        runSMS = 'SMS' in options.datasetName
        runOnMC = 'START' in options.datasetName
    if not options.inputFiles:
        if options.inputDirectory is not None:
            listDirectory(options.inputDirectory, options.inputFiles, options.maxFiles)

        if True:
            names = [f for f in options.datasetName.split('/') if f]
            if runOnMC:
                options.model = names[0].split('-')[1].split('_')[0]
            if options.index < 0:
                name = '%s-%s-%s.root' % (names[0],names[1],names[-1])
            else:
                name = '%s-%s-%s_%d.root' % (names[0],names[1],names[-1],options.index)
            options.outputFile = os.path.join(options.outputDirectory,name)

        files = getFiles(
            [options.datasetName],
            'lucieg',
           # 'susy_tree_CMG_[0-9]+_[0-9]+.root'
            'susy_tree_[0-9]+.root'
            )

       # files=files[:10]
       # files = ['susy_tree_2_.root']
        if options.maxFiles > 0:
            options.inputFiles = files[0:options.maxFiles]
        else:
            options.inputFiles = files
        print 'The number of files to run on is: %d' % len(files)

    if options.index > -1:
        chunks = []
        chunk = []

        for f in sorted(files):
            if len(chunk) <= options.maxFiles:
                chunk.append(f)
            if len(chunk) == options.maxFiles:
                chunks.append(chunk)
                chunk = []
        if chunk:
            chunks.append(chunk)

        options.clearList('inputFiles')
        options.inputFiles = chunks[options.index]
        print 'Created %d chunks of length %s' % (len(chunks),options.maxFiles),options.index,[len(c) for c in chunks],len(chunks[options.index]),len(options.inputFiles)
        print options.inputFiles

    # pickleFile = options.outputFile.replace('.root','.pkl')

    rt.gROOT.ProcessLine("""
struct Variables{\
    Double_t MR;\
    Double_t MR_JES_UP;\
    Double_t MR_JES_DOWN;\
    Double_t RSQ;\
    Double_t RSQ_JES_UP;\
    Double_t RSQ_JES_DOWN;\
    Double_t met;\
    Double_t met_x;\
    Double_t met_y;\
    Double_t met_up;\
    Double_t met_down;\
    Double_t caloMET;\
    Double_t caloMET_x;\
    Double_t caloMET_y;\
    Double_t hemi1Mass;\
    Double_t hemi2Mass;\
    Double_t hemi1TopMass;\
    Double_t hemi1WMass;\
    Double_t hemi1ThetaH;\
    Double_t hemiLepThetaH;\
    Double_t hemi2TopMass;\
    Double_t hemi2WMass;\
    Double_t hemi2ThetaH;\
    Double_t mStop;\
    Double_t mLSP;\
    Double_t diTopPt;\
    Double_t hemi1Pt;\
    Double_t hemi2Pt;\
    Double_t hemi1Eta;\
    Double_t hemi2Eta;\
    Double_t hemi1Phi;\
    Double_t hemi2Phi;\
    Double_t pileUpWeightABCD;\
    Double_t pileUpWeightBCD;\
    Double_t isrWeightUp;\
    Double_t isrWeight;\
    Double_t isrWeightDown;\
    Double_t polarizationWeightPlus1;\
    Double_t polarizationWeightMinus1;\
    Double_t MRT;\
    Double_t MCT;\
    Double_t MEFF;\
};""")

    rt.gROOT.ProcessLine("""
struct Info{\
    Int_t event;\
    Int_t run;\
    Int_t lumi;\
    Int_t nJet;\
    Int_t nJetNoLeptons;\
    Int_t nJet20;\
    Int_t nJetNoLeptons20;\
    Int_t nCSVL;\
    Int_t nCSVL20;\
    Int_t nCSVM;\
    Int_t nCSVT;\
    Int_t NBJET;\
    Int_t nMuonLoose;\
    Int_t nMuonTight;\
    Int_t nElectronLoose;\
    Int_t nElectronTight;\
    Int_t nTauLoose;\
    Int_t nTauTight;\
    Int_t nLepton;\
    Int_t nVertex;\
    Int_t hemisphereBalance;\
    Int_t hemi1Count;\
    Int_t hemi2Count;\
    Int_t genInfo;\
    Int_t BOX_NUM;\
    Int_t BOX_NUM_GEN;\
    Int_t bestHemi;\
};""")

    rt.gROOT.ProcessLine("""
struct Filters{\
    Bool_t hadBoxFilter;\
    Bool_t eleBoxFilter;\
    Bool_t muBoxFilter;\
    Bool_t eleTriggerFilter;\
    Bool_t hadTriggerFilter;\
    Bool_t quadJetTriggerFilter;\
    Bool_t muTriggerFilter;\
    Bool_t metFilter;\
    Bool_t isolatedTrack10Filter;\
    Bool_t isolatedTrack10LeptonFilter;\
};""")


    top_dir = os.path.join(os.environ['CMSSW_BASE'],'src/CMGTools/Susy/macros/MultiJet')
    rt.gROOT.ProcessLine(".L %s/calcVariables.C+" % top_dir)
    rt.gROOT.ProcessLine(".L %s/StopReweight.C+" % top_dir)

    #see http://mctlib.hepforge.org/
    rt.gROOT.ProcessLine(".L %s/mctlib.C+" % top_dir)

    from ROOT import Variables, Info, Filters, SUSYGenParticle#, mR, mRT
    from ROOT import mctlib
    mct_calc = mctlib()

#    output = rt.TFile.Open(options.outputFile,'recreate')
    tree = rt.TTree('RMRTree','Multijet events')
    tree.SetDirectory(0)
    def setAddress(obj, flag):
        for branch in dir(obj):
            if branch.startswith('__'): continue
            tree.Branch(branch,rt.AddressOf(obj,branch),'%s/%s' % (branch,flag) )

    filters = Filters()
    info = Info()
    vars = Variables()

    setAddress(filters,'O')
    setAddress(info,'I')
    setAddress(vars,'D')

    CTEQ66_W = std.vector('double')()
    MRST2006NNLO_W = std.vector('double')()
    tree.Branch('CTEQ66_W',CTEQ66_W)
    tree.Branch('MRST2006NNLO_W',MRST2006NNLO_W)

    jet_pt = std.vector('double')()
    tree.Branch('jet_pt',jet_pt)
    jet_eta = std.vector('double')()
    tree.Branch('jet_eta',jet_eta)
    jet_phi = std.vector('double')()
    tree.Branch('jet_phi',jet_phi)
    jet_csv = std.vector('double')()
    tree.Branch('jet_csv',jet_csv)
    jet_fl = std.vector('double')()
    tree.Branch('jet_fl',jet_fl)
    jet_mult = std.vector('double')()
    tree.Branch('jet_mult',jet_mult)
    jet_had_frac = std.vector('double')()
    tree.Branch('jet_had_frac',jet_had_frac)
    jet_girth = std.vector('double')()
    tree.Branch('jet_girth',jet_girth)
    jet_girth_ch = std.vector('double')()
    tree.Branch('jet_girth_ch',jet_girth_ch)

    pftau_mt = std.vector('double')()
    tree.Branch('pftau_mt',pftau_mt)

    jet_veto = std.vector('int')()
    tree.Branch('jet_veto',jet_veto)

    muLoose_pt = std.vector('double')()
    tree.Branch('muLoose_pt',muLoose_pt)
    muLoose_eta = std.vector('double')()
    tree.Branch('muLoose_eta',muLoose_eta)

    muTight_pt = std.vector('double')()
    tree.Branch('muTight_pt',muTight_pt)
    muTight_eta = std.vector('double')()
    tree.Branch('muTight_eta',muTight_eta)


    eleLoose_pt = std.vector('double')()
    tree.Branch('eleLoose_pt',eleLoose_pt)
    eleLoose_eta = std.vector('double')()
    tree.Branch('eleLoose_eta',eleLoose_eta)

    eleTight_pt = std.vector('double')()
    tree.Branch('eleTight_pt',eleTight_pt)
    eleTight_eta = std.vector('double')()
    tree.Branch('eleTight_eta',eleTight_eta)


    # use Varparsing object
    print 'inputFiles:',options.inputFiles
    events = Events(options)

    #make some handles
    jetSel30H = Handle("std::vector<cmg::PFJet>")
    jetSel20H = Handle("std::vector<cmg::PFJet>")
    jetSelCleanedH = Handle("std::vector<cmg::PFJet>")

    hemiHadH = Handle("std::vector<cmg::DiObject<cmg::Hemisphere, cmg::Hemisphere> >")
    hemiLepH = Handle("std::vector<cmg::DiObject<cmg::Hemisphere, cmg::Hemisphere> >")
    metH = Handle("std::vector<cmg::BaseMET>")
    calometH = Handle("std::vector<reco::CaloMET>")
    lheH = Handle('LHEEventProduct')
    pdfH = Handle('std::vector<double>')
    candH = Handle("std::vector<reco::LeafCandidate>")
    vertexH = Handle("std::vector<reco::Vertex>")
    genH    = Handle("std::vector<reco::GenParticle>")

    electronH = Handle("std::vector<cmg::Electron>")
    muonH = Handle("std::vector<cmg::Muon>")
    tauH = Handle("std::vector<cmg::Tau>")

    triggerH = Handle('std::vector<cmg::TriggerObject>')
    countH = Handle('int')
    filterH = Handle('int')
    pileUpH = Handle('double')
    doubleH = Handle('std::vector<double>')

    pathTriggerH = Handle("edm::TriggerResults")
    lheH = Handle('LHEEventProduct')

    pfcandsptH = Handle('std::vector<float>')
    pfcandstrkisoH = Handle('std::vector<float>')
    pfcandschgH = Handle('std::vector<int>')
    pfcandsfromPVH = Handle('std::vector<bool>')

    store = RootFile.RootFile(options.outputFile)
    store.add(tree)

    count = 0
    #for storing the counts of each model point
    bins = {}

    # loop over events
    nEvents = 0
    countThetaH = 0

    #print 'nevents',events.numEntries()
    for event in events:
        # print 'event', nEvents
        nEvents+=1
        # if nEvents > 2000 :
        #     break

        info.event = event.object().id().event()
        info.lumi = event.object().id().luminosityBlock()
        info.run = event.object().id().run()

        CTEQ66_W.clear()
        MRST2006NNLO_W.clear()

        jet_pt.clear()
        jet_eta.clear()
        jet_phi.clear()
        jet_csv.clear()
        jet_fl.clear()
        jet_mult.clear()
        jet_had_frac.clear()
        jet_girth.clear()
        jet_girth_ch.clear()
        jet_veto.clear()

        pftau_mt.clear()

        muLoose_pt.clear()
        muLoose_eta.clear()
        muTight_pt.clear()
        muTight_eta.clear()

        eleLoose_pt.clear()
        eleLoose_eta.clear()
        eleTight_pt.clear()
        eleTight_eta.clear()


        vars.pileUpWeight = 1.0

        if (count % 1000) == 0:
            print count,'run/lumi/event',info.run,info.lumi,info.event
            tree.AutoSave()
        count += 1

        #get the LHE product info
        vars.mStop = -1
        vars.mLSP = -1
        if runOnMC and runSMS:
            event.getByLabel(('source'),lheH)
            if lheH.isValid():
                lhe = lheH.product()
                for i in xrange(lhe.comments_size()):
                    comment = lhe.getComment(i)
                    if 'model' not in comment: continue
                    comment = comment.replace('\n','')
                    parameters = comment.split(' ')[2]
                    masses = map(float,parameters.split('_')[-2:])
                    vars.mStop = masses[0]
                    vars.mLSP = masses[1]
                if skimEvents and not (vars.mLSP == mLSPskim ) :
                   # print 'failed skim'
                    #TODO: For Moriond, only consider the zero LSP mass strip
                    continue

        #store how many of each model we see
        point = (vars.mStop,vars.mLSP)
        if bins.has_key(point):
            bins[point] = bins[point] + 1
        else:
            bins[point] = 1

        event.getByLabel(('TriggerResults','','MJSkim'),pathTriggerH)
        pathTrigger = pathTriggerH.product()
        pathTriggerNames = event.object().triggerNames(pathTrigger)

        #start by vetoing events that didn't pass the offline selection
        filters.hadBoxFilter = pathTrigger.accept(pathTriggerNames.triggerIndex('razorMJSkimSequenceHadPath'))
        filters.eleBoxFilter = pathTrigger.accept(pathTriggerNames.triggerIndex('razorMJSkimSequenceElePath'))
        filters.muBoxFilter = pathTrigger.accept(pathTriggerNames.triggerIndex('razorMJSkimSequenceMuPath'))
        path = filters.hadBoxFilter or filters.muBoxFilter or filters.eleBoxFilter
        if skimEvents and not path:
            print 'continue - skimEvents and not path'
            continue

        #also get the MET filter
        event.getByLabel(('TriggerResults','','PAT'),pathTriggerH)
        pathTrigger = pathTriggerH.product()
        pathTriggerNames = event.object().triggerNames(pathTrigger)
        if runOnMC:
            filters.metFilter = pathTrigger.accept(pathTriggerNames.triggerIndex('metNoiseCleaningPath'))
        else:
            filters.metFilter = pathTrigger.accept(pathTriggerNames.triggerIndex('metNoiseCleaningPath')) and pathTrigger.accept(pathTriggerNames.triggerIndex('trkPOGFiltersPath'))

        event.getByLabel(('razorMJDiHemiHadBoxUp'),hemiHadH)
        if hemiHadH.isValid() and len(hemiHadH.product()):
            hemi = hemiHadH.product()[0]
            vars.RSQ_JES_UP = hemi.Rsq()
            vars.MR_JES_UP = hemi.mR()

        event.getByLabel(('razorMJDiHemiHadBoxDown'),hemiHadH)
        if hemiHadH.isValid() and len(hemiHadH.product()):
            hemi = hemiHadH.product()[0]
            vars.RSQ_JES_DOWN = hemi.Rsq()
            vars.MR_JES_DOWN = hemi.mR()

        #the number of lepton cleaned jets
        jet_param_veto = []
        event.getByLabel(('razorMJJetCleanedLoose'),jetSelCleanedH)
        if jetSelCleanedH.isValid():
            info.nJetNoLeptons = len([j for j in jetSelCleanedH.product() if j.pt() >= 30.])
            info.nJetNoLeptons20 = len(jetSelCleanedH.product())
            jet_param_veto = [ (j.pt(), j.eta()) for j in jetSelCleanedH.product()]

        event.getByLabel(('razorMJPFJetSel30'),jetSel30H)
        if not jetSel30H.isValid():
            print 'not jetSel30H.isValid()'
            continue
        jets = jetSel30H.product()
        info.nJet30 = len(jets)
        info.nJet = len([j for j in jetSel30H.product() if j.pt() >= 30.])


        #all PFCands

        vars.MEFF = 0.0
        for jet in jets:
            jet_pt.push_back(jet.pt())
            jet_eta.push_back(jet.eta())
            jet_phi.push_back(jet.phi())
            jet_csv.push_back(jet.btag(6))
            jet_fl.push_back(jet.partonFlavour())
            #charged multiplicity
            jet_mult.push_back(jet.component(1).number() + jet.component(2).number() + jet.component(3).number() )
            #hadronic (neutral + charged) fraction
            jet_had_frac.push_back(jet.component(1).fraction()+jet.component(5).fraction())
            #girth
            jet_girth.push_back(jet.girth())
            jet_girth_ch.push_back(jet.girth_charged())
            #store whether or not this was removed from the lepton veto jets
            jet_veto.push_back( int( (jet.pt(), jet.eta() ) in jet_param_veto) )
            vars.MEFF += jet.pt()

        #store the number of btags at each working point
        csv = sorted([j.btag(6) for j in jets if j.pt() >= 30.], reverse=True)
        info.nCSVL = len([c for c in csv if c >= 0.244])
        info.nCSVM = len([c for c in csv if c >= 0.679])
        info.nCSVT = len([c for c in csv if c >= 0.898])
        csv_20 = sorted([j.btag(6) for j in jets if j.pt() >= 20.], reverse=True)
        info.nCSVL20 = len([c for c in csv_20 if c >= 0.244])

        event.getByLabel(('cmgPFMET'),metH)
        met = metH.product()[0]
        vars.met = met.et()
        vars.met_x = met.px()
        vars.met_y = met.py()
        vars.MEFF += met.et()



        #set the number of btags
        if info.nCSVL == 0:
            info.NBJET = 0 #bjet veto
        else:
            info.NBJET = info.nCSVM #minimum is one medium

        #loose lepton ID
        event.getByLabel(('razorMJElectronLoose'),electronH)
        event.getByLabel(('razorMJMuonLoose'),muonH)
        event.getByLabel(('razorMJTauLoose'),tauH)
        #
        info.nElectronLoose = len(electronH.product())
        info.nMuonLoose = len(muonH.product())
        info.nTauLoose = len(tauH.product())

        #get leading and subleading leptons pt/eta for data/MC scaling
        if len(muonH.product()):
            for mu in muonH.product()[:2]:
                muLoose_pt.push_back(mu.pt())
                muLoose_eta.push_back(mu.eta())
        if len(electronH.product()):
            for ele in electronH.product()[:2]:
                eleLoose_pt.push_back(ele.pt())
                eleLoose_eta.push_back(ele.eta())

        #loop over loose PF taus
        for t in tauH.product():
            pftau_mt.push_back(mt(t,met))

        #tight lepton ID
        event.getByLabel(('razorMJElectronTight'),electronH)
        event.getByLabel(('razorMJMuonTight'),muonH)
        event.getByLabel(('razorMJTauTight'),tauH)

        #get leading and subleading leptons pt/eta for data/MC scaling
        if len(muonH.product()):
            for mu in muonH.product():
                muTight_pt.push_back(mu.pt())
                muTight_eta.push_back(mu.eta())
        if len(electronH.product()):
            for ele in electronH.product():
                eleTight_pt.push_back(ele.pt())
                eleTight_eta.push_back(ele.eta())

        #
        info.nElectronTight = len(electronH.product())
        info.nMuonTight = len(muonH.product())
        info.nTauTight = len(tauH.product())
        info.nLepton = info.nElectronTight + info.nMuonTight
        #if not (info.nLepton == 1 ): continue
        #store the leptons for future use
        leptons = [l for l in electronH.product()]
        leptons.extend([l for l in muonH.product()])
        #leptons.extend([l for l in tauH.product()])

        #this is for the isolated track veto
        event.getByLabel(('razorMJTrackIsolationMaker','pfcandspt'),pfcandsptH)
        event.getByLabel(('razorMJTrackIsolationMaker','pfcandstrkiso'),pfcandstrkisoH)
        event.getByLabel(('razorMJTrackIsolationMaker','pfcandschg'),pfcandschgH)
        event.getByLabel(('razorMJTrackIsolationMaker','pfcandsfromPV'),pfcandsfromPVH)

        filters.isolatedTrack10Filter = False
        if pfcandsptH.isValid():
            pfcandspt = pfcandsptH.product()
            pfcandstrkiso = pfcandstrkisoH.product()
            pfcandschg = pfcandschgH.product()
            pfcandsfromPV = pfcandsfromPVH.product()

            veto10 = False
            for i in xrange(len(pfcandspt)):
                if not(pfcandsfromPV.at(i)): continue
                if pfcandspt.at(i) >= 10. and pfcandschg.at(i) > 0:
                    reliso = pfcandstrkiso.at(i)/pfcandspt.at(i)
                    if reliso < 0.1:
                        veto10 = True
                if veto10:
                    break
            filters.isolatedTrack10Filter = veto10

        #this is for the isolated track veto, for leptonic boxes
        event.getByLabel(('razorMJLeptonTrackIsolationMaker','pfcandspt'),pfcandsptH)
        event.getByLabel(('razorMJLeptonTrackIsolationMaker','pfcandstrkiso'),pfcandstrkisoH)
        event.getByLabel(('razorMJLeptonTrackIsolationMaker','pfcandschg'),pfcandschgH)
        event.getByLabel(('razorMJLeptonTrackIsolationMaker','pfcandsfromPV'),pfcandsfromPVH)

        filters.isolatedTrack10LeptonFilter = False
        if pfcandsptH.isValid():
            pfcandspt = pfcandsptH.product()
            pfcandstrkiso = pfcandstrkisoH.product()
            pfcandschg = pfcandschgH.product()
            pfcandsfromPV = pfcandsfromPVH.product()

            veto10 = False
            for i in xrange(len(pfcandspt)):
                if not(pfcandsfromPV.at(i)): continue
                if len(electronH.product()) :
                    if pfcandschg.at(i) * electronH.product()[0].charge() > 0:
                        continue
                elif len(muonH.product()) :
                    if pfcandschg.at(i) * muonH.product()[0].charge() > 0:
                        continue
                if pfcandspt.at(i) >= 10. and pfcandschg.at(i) > 0:
                    reliso = pfcandstrkiso.at(i)/pfcandspt.at(i)
                    if reliso < 0.1:
                        veto10 = True
                if veto10:
                    break
            filters.isolatedTrack10LeptonFilter = veto10


        info.BOX_NUM = getBox(info.NBJET,info.nElectronTight,info.nMuonTight,info.nTauTight)

        if info.nLepton == 1 and info.nJetNoLeptons20 >= 4:
            #if we have 4 jets above 30, we use them, otherwise take the 20 GeV jets
            if info.nJetNoLeptons >= 4:
                event.getByLabel(('razorMJDiHemiLepBox'),hemiLepH)
            else:
                event.getByLabel(('razorMJDiHemiLepBox20'),hemiLepH)

            if hemiLepH.isValid() and len( hemiLepH.product())>0.:

                hemi = hemiLepH.product()[0]

                vars.RSQ = hemi.Rsq()
                vars.MR = hemi.mR()
                vars.hemi1Mass = hemi.leg1().mass()
                vars.hemi2Mass = hemi.leg2().mass()
                info.hemisphereBalance = (10*hemi.leg1().numConstituents()) + hemi.leg2().numConstituents()

                vars.hemi1Pt = hemi.leg1().pt()
                vars.hemi1Eta = hemi.leg1().eta()
                vars.hemi1Phi = hemi.leg1().phi()
                vars.hemi2Pt = hemi.leg2().pt()
                vars.hemi2Eta = hemi.leg2().eta()
                vars.hemi2Phi = hemi.leg2().phi()

                #MCT etc
                vars.MCT = mct(mct_calc,hemi.leg1().p4(),hemi.leg2().p4())
                vars.MRT = hemi.mRT()

                #now need to take care of the systematics...
                #UP
                event.getByLabel(('razorMJDiHemiLepBoxUp'),hemiLepH)
                if hemiLepH.isValid() and len(hemiLepH.product())>0:
                    hemi = hemiLepH.product()[0]
                    vars.RSQ_JES_UP = hemi.Rsq()
                    vars.MR_JES_UP = hemi.mR()


                #DOWN
                event.getByLabel(('razorMJDiHemiLepBoxDown'),hemiLepH)
                if hemiLepH.isValid() and len( hemiLepH.product())>0.:
                    hemi = hemiLepH.product()[0]
                    vars.RSQ_JES_DOWN = hemi.Rsq()
                    vars.MR_JES_DOWN = hemi.mR()

                #helicity for leptonic case
                subjets = hemi.leg1().sourcePtrs()
                dR1 = 100000.
                for j in subjets :
                    dR1 = min(dR1, deltaR ( leptons[0], j))

                subjets = hemi.leg2().sourcePtrs()
                dR2 = 100000.
                for j in subjets :
                    dR2 = min(dR2, deltaR ( leptons[0], j))

                if dR1 < dR2 : subjets = hemi.leg1().sourcePtrs()
                jets = []
                dR = 100000.
                for j in subjets :
                    dR = min(dR, deltaR ( leptons[0], j))
                    if dR > min(dR1,dR2):
                        jets.append(j)
                if len(jets) > 0. :
                    csv = sorted([(j.btag(6),j) for j in jets], reverse=True)
                    tag = csv[0][1]

                    thetaH = calcHelicityLep(leptons[0], met, tag )
                    vars.hemiLepThetaH = thetaH
                    if thetaH == -2 :
                        countThetaH +=1
                        print countThetaH

        else:
            #take the 20Gev jet control sample if relevant
            if info.nJet20 >= 6 and info.nJet < 6:
                event.getByLabel(('razorMJDiHemiHadBox20'),hemiHadH)
            else:
                event.getByLabel(('razorMJDiHemiHadBox'),hemiHadH)

            if hemiHadH.isValid() and len(hemiHadH.product()):
                hemi = hemiHadH.product()[0]
                vars.RSQ = hemi.Rsq()
                vars.MR = hemi.mR()
                vars.hemi1Mass = hemi.leg1().mass()
                vars.hemi2Mass = hemi.leg2().mass()
                info.hemisphereBalance = (10*hemi.leg1().numConstituents()) + hemi.leg2().numConstituents()

                #run the hadronic top tagger
                info.hemi1Count, vars.hemi1TopMass, vars.hemi1WMass, vars.hemi1ThetaH = topTag( hemi.leg1() )
                info.hemi2Count, vars.hemi2TopMass, vars.hemi2WMass, vars.hemi2ThetaH = topTag( hemi.leg2() )

                #calculate a chi2
                chi1 = (abs(vars.hemi1TopMass-173.5)/57.)+(abs(vars.hemi1WMass-80.385)/44.)
                chi2 = (abs(vars.hemi2TopMass-173.5)/57.)+(abs(vars.hemi2WMass-80.385)/44.)
                if chi1 <= chi2:
                    info.bestHemi = 1
                else:
                    info.bestHemi = 2

                vars.hemi1Pt = hemi.leg1().pt()
                vars.hemi1Eta = hemi.leg1().eta()
                vars.hemi1Phi = hemi.leg1().phi()
                vars.hemi2Pt = hemi.leg2().pt()
                vars.hemi2Eta = hemi.leg2().eta()
                vars.hemi2Phi = hemi.leg2().phi()

                #MCT etc
                vars.MCT = mct(mct_calc,hemi.leg1().p4(),hemi.leg2().p4())
                vars.MRT = hemi.mRT()


        event.getByLabel(('razorMJMetUp'),metH)
        met = metH.product()[0]
        vars.met_up = met.et()

        event.getByLabel(('razorMJMetDown'),metH)
        met = metH.product()[0]
        vars.met_down = met.et()

        event.getByLabel(('goodOfflinePrimaryVertices'),vertexH)
        info.nVertex = len(vertexH.product())

        if runOnMC:
            #dump the PDF weights
            event.getByLabel(('dumpPdfWeights','cteq66'),pdfH)
            if pdfH.isValid():
                for w in pdfH.product():
                    CTEQ66_W.push_back(w)
            event.getByLabel(('dumpPdfWeights','NNPDF20'),pdfH)
            if pdfH.isValid():
                for w in pdfH.product():
                    MRST2006NNLO_W.push_back(w)

        event.getByLabel(('razorMJAllTriggerSel'),triggerH)
        if len(triggerH.product()):
            trigger = triggerH.product()[0]
            filters.hadTriggerFilter =  trigger.getSelectionRegExp("^HLT_DiJet[0-9]+_DiJet[0-9]+_DiJet[0-9]+.*_v[0-9]+$") or\
                trigger.getSelectionRegExp("^HLT_QuadJet[0-9]+_DiJet[0-9]+.*_v[0-9]+$") or\
                trigger.getSelectionRegExp("^HLT_QuadJet[0-9]+_v[0-9]+$") or\
                trigger.getSelectionRegExp("^HLT_QuadJet[0-9]+_L1FastJet_v[0-9]+$") or \
                trigger.getSelectionRegExp("^HLT_SixJet[0-9]+.*_v[0-9]+$")
            filters.quadJetTriggerFilter =   trigger.getSelectionRegExp("^HLT_QuadJet[0-9]+_v[0-9]+$")
            filters.eleTriggerFilter = trigger.getSelectionRegExp("^HLT_Ele[0-9]+_WP80_v[0-9]+$")
            filters.muTriggerFilter = trigger.getSelectionRegExp("^HLT_Mu[0-9]+_eta2p1_v[0-9]+$") or \
                trigger.getSelectionRegExp("^HLT_IsoMu[0-9]+_eta2p1_v[0-9]+$") or \
                trigger.getSelectionRegExp("^HLT_Mu[0-9]+_v[0-9]+$") or \
                trigger.getSelectionRegExp("^HLT_IsoMu[0-9]+_v[0-9]+$")
            del trigger
        else:
            filters.hadTriggerFilter = False
            filters.quadJetTriggerFilter = False
            filters.muTriggerFilter = False
            filters.eleTriggerFilter = False

        #recoCaloMETs_corMetGlobalMuons__RECO
        event.getByLabel(('corMetGlobalMuons'),calometH)
        calomet = calometH.product()[0]
        vars.caloMET = calomet.et()
        vars.caloMET_x = calomet.px()
        vars.caloMET_y = calomet.py()


        if runOnMC:
            event.getByLabel(('topGenInfo'),candH)
            if options.model is not None and candH.isValid() and len(candH.product()):
                if 'T2' in options.model:
                    diTop = candH.product()[1]
                elif 'T1' in options.model:
                    diTop = candH.product()[2]
                else:
                    diTop = candH.product()[0]
                vars.diTopPt = diTop.pt()


            event.getByLabel(('genParticlesStatus3'), genH)
            genParticles  = std.vector('SUSYGenParticle')()
            thetaMixingTargetPlus1  = -0.437
            thetaMixingTargetMinus1 = -1.134
            thetaMixingReference = 0.785
            from ROOT import Reweight_Stop_to_TopChi0_with_SUSYmodel
            polarizationWeightPlus1  = -100
            polarizationWeightMinus1 = -100
            if genH.isValid():
                for gen in genH.product():
                    genPart = SUSYGenParticle()
                    genPart.pdgId  = gen.pdgId()
                    genPart.energy = gen.energy()
                    genPart.pt     = gen.pt()
                    genPart.eta    = gen.eta()
                    genPart.phi    = gen.phi()
                    idx = 0
                    if gen.numberOfMothers() > 0:
                        for genP in genH.product() :
                            if  gen.mother() == genP :
                                genPart.firstMother = idx
                                break
                            idx+=1
                    else :
                        genPart.firstMother = -1
                    genParticles.push_back(genPart)
            polarizationWeightPlus1  = Reweight_Stop_to_TopChi0_with_SUSYmodel (genParticles, thetaMixingTargetPlus1)
            polarizationWeightMinus1 = Reweight_Stop_to_TopChi0_with_SUSYmodel (genParticles, thetaMixingTargetMinus1)
            vars.polarizationWeightPlus1  = polarizationWeightPlus1
            vars.polarizationWeightMinus1 = polarizationWeightMinus1

            event.getByLabel(('simpleGenInfo'),filterH)
            if filterH.isValid():
                info.genInfo = filterH.product()[0]
                info.BOX_NUM_GEN = getBoxGenLevel(info.genInfo)

            #store weights for both ABCD (StreamA) and BCD (Parking)
            event.getByLabel(('vertexWeightSummer12MC53X2012ABCDData'),pileUpH)
            vars.pileUpWeightABCD = pileUpH.product()[0]
            event.getByLabel(('vertexWeightSummer12MC53X2012BCDData'),pileUpH)
            vars.pileUpWeightBCD = pileUpH.product()[0]

            event.getByLabel(('isrWeight'),doubleH)
            vars.isrWeightUp   = doubleH.product()[0]
            vars.isrWeight     = doubleH.product()[1]
            vars.isrWeightDown = doubleH.product()[2]

   ##      #TODO: Place some cut here
        if skimEvents and (vars.RSQ < 0.05 or vars.MR < 350.):
            print 'skimming'
            continue
        if nEvents % 500 == 0:
            print 'event', nEvents
        tree.Fill()

    store.write()

    # sample_counts = file(options.outputFile.replace('.root','.pkl'),'wb')
    # pickle.dump(bins,sample_counts)
    # sample_counts.close()

