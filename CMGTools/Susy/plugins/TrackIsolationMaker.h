// -*- C++ -*-
//
// Package:    NtupleMaker
// Class:      NtupleMaker
// 
/**\class NtupleMaker NtupleMaker.cc CMS2/NtupleMaker/src/NtupleMaker.cc

   Description: <one line class summary>

   Implementation:
   <Notes on implementation>
*/
#ifndef NTUPLEMAKER_TRACKISOLATIONMAKER_H
#define NTUPLEMAKER_TRACKISOLATIONMAKER_H

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/ParticleFlow/interface/PFPileUpAlgo.h"
#include "Math/VectorUtil.h"

//
// class decleration
//

class TrackIsolationMakerSUS : public edm::EDProducer {
public:
     explicit TrackIsolationMakerSUS (const edm::ParameterSet&);
     ~TrackIsolationMakerSUS();

private:
  //  virtual void beginJob() ;
  virtual void beginJob() ;
  virtual void beginRun(edm::Run&, const edm::EventSetup&) ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  float getFixGridRho(std::vector<float>& etabins,std::vector<float>& phibins);
  
  // ----------member data ---------------------------
  double dR_;
  double minPt_;

  edm::InputTag cmgCandidatesTag_;
  edm::InputTag vertexInputTag_;
  std::vector<edm::InputTag> vetoCollectionTags_;

  typedef std::vector< cmg::Candidate > cmgCandidateCollection;
  //typedef std::vector< reco::PFCandidate > cmgCandidateCollection;
  const cmgCandidateCollection *cmgCandidates;

};

#endif

