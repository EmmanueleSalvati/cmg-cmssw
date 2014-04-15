import operator, pickle, pprint, math, re

from CMGTools.RootTools.analyzers.TreeAnalyzerNumpy  import TreeAnalyzerNumpy
from CMGTools.RootTools.fwlite.AutoHandle            import AutoHandle
from CMGTools.Razor.physicsobjects.PhysicsObjects    import *
from CMGTools.Razor.analyzers.ntuple        import *
from math                                            import sqrt



class MultiJetAnalysis( TreeAnalyzerNumpy):
    '''Makes analysis tree.'''

    ##############################################
    ##############################################
    ##############################################
          #INITIALIZATION FUNCTIONs#
    ##############################################
    ##############################################
    ##############################################

    def __init__( self, cfg_ana, cfg_comp, looperName ):
        self.mStop = cfg_comp.mStop
        super(MultiJetAnalysis,self).__init__( cfg_ana, cfg_comp, looperName )
        
    def declareVariables(self):
        tr = self.tree
        #counting
        var( tr, 'nJets'              , float )
        var( tr, 'nBtagJets'          , float )
        var( tr, 'nJetsNoLeptons'     , float )
        var( tr, 'nBtagJetsNoLeptons' , float )
        var( tr, 'nTightMuons'        , float )
        var( tr, 'nLooseMuons'        , float )
        var( tr, 'nTightElectrons'    , float )
        var( tr, 'nLooseElectrons'    , float )
        var( tr, 'itv_had'            , float )
        var( tr, 'itv_lep'            , float )
        #razor
        var( tr, 'MR'                 , float )
        var( tr, 'Rsq'                , float )
        var( tr, 'betaR2011'          , float )
        var( tr, 'gammaR2011'         , float )
        var( tr, 'mR2011'             , float )
        var( tr, 'mRT'                , float )
        var( tr, 'betaRStar'          , float )
        var( tr, 'gammaRStar'         , float )
        var( tr, 'RStar'              , float )
        var( tr, 'mRStar'             , float )
        #top tagging
        var( tr, 'mtH1'               , float )
        var( tr, 'mWH1'               , float )
        var( tr, 'thetaWH1'           , float )
        var( tr, 'mtH2'               , float )
        var( tr, 'mWH2'               , float )
        var( tr, 'thetaWH2'           , float )
        #Q/G discrimination
        var( tr, 'lrm1'               , float )
        var( tr, 'lrm2'               , float )
        var( tr, 'lrm3'               , float )
        var( tr, 'lrm4'               , float )
        var( tr, 'lrm5'               , float )
        var( tr, 'lrm6'               , float )
        var( tr, 'chMultiplicity1'    , float )
        var( tr, 'chMultiplicity2'    , float )
        var( tr, 'chMultiplicity3'    , float )
        var( tr, 'chMultiplicity4'    , float )
        var( tr, 'chMultiplicity5'    , float )
        var( tr, 'chMultiplicity6'    , float )
        #cleaning & selection -not sure that's wanted
        var( tr, 'cleaning'           , int   )
        var( tr, 'bjetHSbox'          , int   )
        var( tr, 'bjetLSbox'          , int   )
        var( tr, 'elebox'             , int   )
        var( tr, 'mubox'              , int   )
        #gen
        var( tr, 'mStop'              , float )
        var( tr, 'mLSP'               , float )
        var( tr, 'mDelta'             , float )
        var( tr, 'massiveJetsmDelta'  , float )
        
    ##############################################
    ##############################################
    ##############################################
          #CORE FUNCTION#
    ##############################################
    ##############################################
    ##############################################
          
    def process(self, iEvent, event):

        tr = self.tree
        tr.reset()
     
        ##############################################
        ###setting the scene                       ###
        ##############################################
       
        ###inherit whatever's TreeAnalyzerNumpy
        super(MultiJetAnalysis,self).process(iEvent, event)
        
        ###"get handles"
        #self.readCollections( iEvent )
        event.razorJets            = self.buildJets     ( self.handles['razorJets'].product()          , event )
        event.razorJetsCleaned     = self.buildJets     ( self.handles['razorJetsCleaned'].product()   , event )
        event.razorJetsNoLeptons   = self.buildJets     ( self.handles['razorJetsNoLeptons'].product() , event )
        event.razorTightMuons      = self.buildMuons    ( self.handles['razorTightMuons'].product()    , event )
        event.razorLooseMuons      = self.buildMuons    ( self.handles['razorLooseMuons'].product()    , event )
        event.razorTightElectrons  = self.buildElectrons( self.handles['razorTightElectrons'].product(), event )
        event.razorLooseElectrons  = self.buildElectrons( self.handles['razorLooseElectrons'].product(), event )
        event.razorHadDiHemi       = self.buildDiHemis  ( self.handles['razorHadDiHemi'].product()     , event )
        event.razorHadHemi         = self.buildHemis  ( self.handles['razorHadHemi'].product()     , event )
        event.razorLepDiHemi       = self.buildDiHemis  ( self.handles['razorLepDiHemi'].product()     , event )
        #for ITV had : need relIso, pt
        event.itvhad_pfcandspt     = self.handles['had_pfcandspt'].product()
        event.itvhad_pfcandsiso    = self.handles['had_pfcandsiso'].product()
        #for ITV lep : need relIso, pt, charge
        event.itvlep_pfcandspt     = self.handles['lep_pfcandspt'].product() 
        event.itvlep_pfcandsiso    = self.handles['lep_pfcandsiso'].product()
        event.itvlep_pfcandschg    = self.handles['lep_pfcandschg'].product()
        #cleaning
        event.cleaning             = self.handles['cleaning'].product()
        #trigger
        event.triggerObjectEle     = self.handles['EleTrigger'].product()
        event.triggerObjectMu      = self.handles['MuTrigger'].product()
        event.triggerObjectHad     = self.handles['HadronicTrigger'].product()
        #gen
        event.lheInfo              = self.handles['lhe'].product()
        
        ##############################################
        ###now, begin the real work : fill the tree###
        ##############################################
        #gen
        mStop, mLSP = self.getMassPoint(event.lheInfo)
        skipEvent   = True if (self.mStop > 0. and not( mStop == self.mStop )) else False
        if skipEvent :
            return True
        mDelta, massiveJetsmDelta = self.getMDeltas( mStop, mLSP )

        fill( tr, 'mStop'              ,   mStop             )
        fill( tr, 'mLSP'               ,   mLSP              )
        fill( tr, 'mDelta'             ,   mDelta            )
        fill( tr, 'massiveJetsmDelta'  ,   massiveJetsmDelta )
        
        #objects counting
        nJets = 0
        nBtagJets = 0
        index=0
        for jet in event.razorJets :
            if jet.pt() > 30. :
                nJets+=1
                index+=1
                #btag
                if jet.btag(6) >= 0.679 :
                    nBtagJets+=1
                #Q/G
                if index < 7 :
                    fill( tr, 'lrm'+str(index)           , jet.girth()              )
                    fill( tr, 'chMultiplicity'+str(index), self.chargedMultiplicity(jet) )

        fill( tr, 'nJets'              ,  nJets    ) 
        fill( tr, 'nBtagJets'          , nBtagJets )

        nJetsNoLeptons     = 0
        nBtagJetsNoLeptons = 0
        for jet in event.razorJetsNoLeptons :
            if jet.pt >=30. :
                nJetsNoLeptons+=1
                if jet.btag(6) >= 0.679 :
                    nBtagJetsNoLeptons+=1
                    
        fill( tr, 'nJetsNoLeptons'     , nJetsNoLeptons     )        
        fill( tr, 'nBtagJetsNoLeptons' , nBtagJetsNoLeptons )

        nTightMuons = len(event.razorTightMuons)
        fill( tr, 'nTightMuons'        , len(event.razorTightMuons) )
        nLooseMuons = len(event.razorLooseMuons)
        fill( tr, 'nLooseMuons'        , len(event.razorLooseMuons) )
        nTightElectrons = len(event.razorTightElectrons)
        fill( tr, 'nTightElectrons'    , len(event.razorTightElectrons) )
        nLooseElectrons = len(event.razorLooseElectrons)
        fill( tr, 'nLooseElectrons'    , len(event.razorLooseElectrons) )
            
        #ITV : hadronic
        itv_had = self.itv_had(event.itvhad_pfcandspt, event.itvhad_pfcandsiso)
        fill( tr, 'itv_had'            ,  itv_had )

        #ITV : leptonic
        chgLeadLep = 0
        if len( event.razorTightMuons ) > 0 :     
            chgLeadLep = event.razorTightMuons[0].charge()
        elif len( event.razorTightElectrons ) > 0 :
            chgLeadLep = event.razorTightElectrons[0].charge()
        itv_lep = self.itv(event.itvhad_pfcandspt, event.itvhad_pfcandsiso, event.itvlep_pfcandschg)
        fill( tr, 'itv_lep'            ,  itv_lep )
     
        #playing with hemispheres
        hemiValid = False
        had = False
        #kinematic variables - we need to make a choice (or duplicate razor variables)
        if len(event.razorHadDiHemi) > 0 and len( event.razorLooseMuons + event.razorLooseElectrons ) < 1 and not(itv_had) :
            hemi = event.razorHadDiHemi[0]
            hemiValid = True
            had = True
        elif len(event.razorLepDiHemi) > 0:
            hemi = event.razorLepDiHemi[0]
            hemiValid = True
        
        if hemiValid :
            fill(tr, 'MR' , hemi.mR())
            fill(tr, 'Rsq', hemi.Rsq())
            #alternative definitions of mr
            mRT        = sqrt(hemi.Rsq())*hemi.mR()
            betaR2011, gammaR2011, mR2011, mRStar, gammaRStar, RStar = self.getAltRazorVar(hemi.leg1(), hemi.leg2(), mRT)
            
       
            fill(tr, 'betaR2011'  , betaR2011  )
            fill(tr, 'gammaR2011' , gammaR2011 )
            fill(tr, 'mR2011'     , mR2011     )
            fill(tr, 'mRT'        , mRT        )
            fill(tr, 'mRStar'     , mRStar     )
            fill(tr, 'gammaRStar' , gammaRStar )
            fill(tr, 'RStar'      , RStar      )

            #top tagging
            index = 0
            for leg in (hemi.leg1(), hemi.leg2()):
                index+=1
                mWInv, mtInv, thetaWH = self.getTopTagVariables(leg)
                fill(tr, 'mtH'+str(index)     , mtInv )
                fill(tr, 'mWH'+str(index)     , mWInv )
                fill(tr, 'thetaWH'+str(index) , thetaWH)

        #cleaning
        cleaning = event.cleaning[0].getSelection('metNoiseCleaningPath')
        if len(event.razorJetsCleaned)> 0:
            cleaning = 0
        fill( tr, 'cleaning'           ,   cleaning)
     
        #trigger
        triggerHad = 1 if len(event.triggerObjectHad) else 0
        triggerEle = 1 if len(event.triggerObjectEle) else 0
        triggerMu  = 1 if len(event.triggerObjectMu)  else 0
        
        #boxes
        hadBox = (nJets >= 6) \
                 and (nBtagJets>=1) \
                 and (nLooseMuons==0) \
                 and (nLooseElectrons==0)\
                 and not(itv_had) \
                 and cleaning     \
                 and triggerHad   \

        lepBox = (nJetsNoLeptons >= 4) \
                 and (nBtagJetsNoLeptons>=1) \
                 and not(itv_lep) \
                 and cleaning     \
     
        eleBox = lepBox \
                 and (nLooseMuons+nTightMuons==0) \
                 and triggerEle

        muBox  = lepBox \
                 and (nLooseElectrons+nTightElectrons==0) \
                 and triggerMu
            
        fill( tr, 'bjetHSbox'          ,   hadBox )
        fill( tr, 'bjetLSbox'          ,   hadBox )
        fill( tr, 'elebox'             ,   eleBox )
        fill( tr, 'mubox'              ,   muBox  )
            
        #Filling
        self.tree.tree.Fill()

        return True

    ##############################################
    ###writing something to file               ###
    ##############################################
    def write(self):
        super(MultiJetAnalysis,self).write()
         
    
    ##############################################
    ##############################################
    ##############################################
        #COOKING#
    ##############################################
    ##############################################
    ##############################################
    def getMassPoint(self, lheInfo):
        if not (self.mStop > 0.):
            return 0.,0.
        comment    = lheInfo.getComment(1)
        model      = comment.split(' ')[-4]
        parameters = model.split('_')[1:3]
        mStop, mLSP = float(parameters[0]), float(parameters[1])
        return mStop, mLSP

    def getMDeltas( self, mStop, mLSP ):
        
        if mStop > 0. :
            mDelta = (mStop*mStop - mLSP*mLSP) / mStop
            massiveJetsmDelta = (mStop*mStop - (mLSP - 176.)*(mLSP - 176.))*(mStop*mStop - (mLSP + 176.)*(mLSP + 176.)) 
            massiveJetsmDelta = sqrt(max( massiveJetsmDelta, 0)) / (2*mStop)
        else :
            mDelta            = 0
            massiveJetsmDelta = 0
        return mDelta, massiveJetsmDelta

    def chargedMultiplicity(self, jet):
        return jet.component(1).number()+jet.component(2).number()+jet.component(3).number()

    def itv_had(self, pts, isos):
        itv_had = False
        for pt, iso in zip( pts, isos ) :
            if pt < 10.: continue
            else :
                if iso < 0.1 :
                    itv_had = True
                    break
        return itv_had

    def itv(self, pts, isos, charges = [], chargeLead = 0):
        itv    = False
       
        for pt, iso, chg in zip(pts, isos, charges ) :
            if pt < 10.: continue
            if chargeLead * chg > 0 : continue
            else :
                if iso < 0.1 :
                    itv = True
        return itv

    def getAltRazorVar(self, leg1, leg2, mRT):
         q1  = leg1.p()
         q2  = leg2.p()
         q1t = leg1.pt()
         q2t = leg2.pt()
         mod2= (leg1.px()+leg2.px())*(leg1.px()+leg2.px()) + (leg1.py()+leg2.py())*(leg1.py()+leg2.py())  
         q1z = leg1.pz()
         q2z = leg2.pz()
         
         betaR2011  = (q1 - q2) / (q1z - q2z)
         gammaR2011 = 1./sqrt(max (0.000000001, 1. - betaR2011*betaR2011))
         mR2011     = (q1*q2z-q2*q1z)*(q1*q2z-q2*q1z)  /  ((q1z-q2z)*(q1z-q2z) - (q1-q2)*(q1-q2))
         mR2011     = 2*sqrt( max(mR2011, 0.))
         mRStar     = sqrt( max(0., (q1+q2)*(q1+q2) - (q1z+q2z)*(q1z+q2z) - (q1t*q1t - q2t*q2t)*(q1t*q1t - q2t*q2t) / mod2 ))
         if mRStar > 0 :
             gammaRStar =  sqrt(max(0,(q1+q2)*(q1+q2) - (q1z+q2z)*(q1z+q2z))) / mRStar
             RStar      = mRT / mRStar
         else :
             gammaRStar = 0
             RStar      = 0

         return betaR2011, gammaR2011, mR2011, mRStar, gammaRStar, RStar

    def getTopTagVariables(self, leg):
        jets = {}
        for i in range(0, leg.numConstituents()) :
            jet = leg.sourcePtr(i)
            jets[i]=jet.btag(6)
            
        btagOrderedKeys = sorted(jets, key=jets.get, reverse=True)
        btagKey         = btagOrderedKeys[0]
        jets            = btagOrderedKeys[1:]
        
        mWInv = -1
        mtInv = -1

        wJets = []
        for i in jets :
            for j in jets :
                if i == j : continue
                else :
                    jeti = leg.sourcePtr(i)
                    jetj = leg.sourcePtr(j)
                    tmp  = (jeti.p4()+ jetj.p4()).mass()
                    if (abs(tmp - 80.385) < abs(mWInv-80.385)):
                        mtInv = (leg.sourcePtr(btagKey).p4()+jeti.p4()+jetj.p4()).mass()
                        wJets = [jeti, jetj]
                        mWInv =  tmp

        thetaWH = -1
        if len(wJets) < 2 :
            thetaWH = -1
        else :
            wCand=wJets[0].p4()+wJets[1].p4()
            boost = [wCand.px()/wCand.energy(), wCand.py()/wCand.energy(), wCand.pz()/wCand.energy()]
            gamma = 1 - boost[0]*boost[0] - boost[1]*boost[1] - boost[2]*boost[2]
            gamma = 1./sqrt(gamma)
            soft = 0
            if wJets[0].pt() > wJets[1].pt():
                soft = 1
                            
            jSoftx = gamma*(-boost[0]* (wJets[soft]).energy()  + (wJets[soft]).px() )
            jSofty = gamma*(-boost[1]* (wJets[soft]).energy()  + (wJets[soft]).py() )
            jSoftz = gamma*(-boost[2]* (wJets[soft]).energy()  + (wJets[soft]).pz() )
            btagx = gamma*(-boost[0]* leg.sourcePtr(btagKey).energy()  + leg.sourcePtr(btagKey).px() )
            btagy = gamma*(-boost[1]* leg.sourcePtr(btagKey).energy()  + leg.sourcePtr(btagKey).py() )
            btagz = gamma*(-boost[2]* leg.sourcePtr(btagKey).energy()  + leg.sourcePtr(btagKey).pz() )
            #actually cos thetaH
            thetaWH = (jSoftx*btagx + jSofty*btagy + jSoftz*btagz) / (sqrt(jSoftx**2+jSofty**2+jSoftz**2)*sqrt(btagx**2+btagy**2+btagz**2))
       
        return mWInv, mtInv, thetaWH 
                 

      

    ##############################################
    ###building objects functions              ###
    ##############################################
    def buildJets(self, cmgPFJet, event):
        '''Creates python genJets from the recoJets read from the disk.
        to be overloaded if needed.'''
        return map( Jet, cmgPFJet )

    def buildDiHemis(self, cmgDiHemis, event):
        '''Creates python genJets from the recoJets read from the disk.
        to be overloaded if needed.'''
        return map( DiHemisphere, cmgDiHemis )

    def buildHemis(self, cmgHemis, event):
        '''Creates python genJets from the recoJets read from the disk.
        to be overloaded if needed.'''
        return map( Hemisphere, cmgHemis )

    def buildMuons(self, cmgMuon, event):
        '''Creates python genJets from the recoJets read from the disk.
        to be overloaded if needed.'''
        return map( Muon, cmgMuon )
    
    def buildElectrons(self, cmgElectron, event):
        '''Creates python genJets from the recoJets read from the disk.
        to be overloaded if needed.'''
        return map( Electron, cmgElectron )

    def buildFloats(self, floats, event):
        '''Creates python genJets from the recoJets read from the disk.
        to be overloaded if needed.'''
        return map( Float, floats )

    ###
    def declareHandles(self):
        super(MultiJetAnalysis,self).declareHandles()
        self.handles['razorJets'] =  AutoHandle(
            'razorJet',
            'std::vector<cmg::PFJet>'
            )   
        self.handles['razorJetsCleaned'] =  AutoHandle(
            'razorJetCleaned',
            'std::vector<cmg::PFJet>'
            )   
        self.handles['razorJetsNoLeptons']  =  AutoHandle(
            'razorJetNoLepton',
            'std::vector<cmg::PFJet>'
            )   
        self.handles['razorTightMuons']     =  AutoHandle(
            'razorTightMuon',
            'std::vector<cmg::Muon>'
            )   
        self.handles['razorLooseMuons']     =  AutoHandle(
            'razorLooseMuon',
            'std::vector<cmg::Muon>'
            )   
        self.handles['razorTightElectrons'] =  AutoHandle(
            'razorTightElectron',
            'std::vector<cmg::Electron>'
            )   
        self.handles['razorLooseElectrons'] =  AutoHandle(
            'razorLooseElectron',
            'std::vector<cmg::Electron>'
            )   
        self.handles['razorHadDiHemi']      =  AutoHandle(
            'razorDiHemiHadBox',
            'std::vector<cmg::DiObject<cmg::Hemisphere,cmg::Hemisphere> >',
            )   
        self.handles['razorHadHemi']      =  AutoHandle(
            'razorHemiHadBox',
            'std::vector<cmg::Hemisphere>',
            )   
        self.handles['razorLepDiHemi']      =  AutoHandle(
            'razorDiHemiLepBox',
            'std::vector<cmg::DiObject<cmg::Hemisphere,cmg::Hemisphere> >',
            )   
        self.handles['had_pfcandspt']      =  AutoHandle(
            ('razorLeptonTrackIsolationMaker','pfcandspt','RZR'),
            'std::vector<float>',
            )   
        self.handles['had_pfcandsiso']      =  AutoHandle(
            ('razorLeptonTrackIsolationMaker','pfcandstrkiso','RZR'),
            'std::vector<float>',
            )   
        self.handles['lep_pfcandspt']      =  AutoHandle(
            ('razorLeptonTrackIsolationMaker','pfcandspt','RZR'),
            'std::vector<float>',
            )   
        self.handles['lep_pfcandsiso']      =  AutoHandle(
            ('razorLeptonTrackIsolationMaker','pfcandstrkiso','RZR'),
            'std::vector<float>',
            )   
        self.handles['lep_pfcandschg']      =  AutoHandle(
            ('razorLeptonTrackIsolationMaker','pfcandschg','RZR'),
            'std::vector<int>',
            )   
        self.handles['cleaning']      =  AutoHandle(
            'razorCleaning',
            'std::vector<cmg::TriggerObject>',
            )   
        self.handles['EleTrigger'] =  AutoHandle(
            'razorEleTrigger',
            'std::vector<cmg::TriggerObject>'
            )
        self.handles['MuTrigger'] =  AutoHandle(
            'razorMuTrigger',
            'std::vector<cmg::TriggerObject>'
            )
        self.handles['HadronicTrigger'] =  AutoHandle(
            'razorHadronicTrigger',
            'std::vector<cmg::TriggerObject>'
            )
        self.handles['lhe'] =  AutoHandle(
            'source',
            'LHEEventProduct'
            )
       
       
       
       

    
