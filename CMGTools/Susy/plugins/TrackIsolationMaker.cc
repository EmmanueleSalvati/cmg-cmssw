//-----------------------------------------------------------------------------------------
//
// Computation of the trackIsolation, for use with the isolated track veto 
// used for the stop quark search in the single lepton channel
// Author: Ben Hooberman
//
// For each PFCandidate above threshold minPt_PFCandidate store 4 quantities:
// pT of PFCandidate
// charge of PFCandidate
// fromPV of PFCandidate
// the trackIsolation value
//
// In the analysis, we veto any event containing IN ADDITION TO the selected lepton a charged PFCandidate with:
// pT > 10 GeV, from PV, and trackIso/pT < 0.1
//
//-----------------------------------------------------------------------------------------

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "RecoParticleFlow/PFProducer/interface/PFMuonAlgo.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlock.h"
#include "DataFormats/Common/interface/ValueMap.h"

#include "AnalysisDataFormats/CMGTools/interface/Lepton.h"
#include "AnalysisDataFormats/CMGTools/interface/Candidate.h"

#include "CMGTools/Susy/plugins/TrackIsolationMaker.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "TMath.h"

#include <utility>

typedef math::XYZTLorentzVectorF LorentzVector;
typedef math::XYZPoint Point;
using namespace reco;
using namespace edm;
using namespace std;

//
// class decleration
//

//
// constructors and destructor
//

TrackIsolationMakerSUS::TrackIsolationMakerSUS(const edm::ParameterSet& iConfig) {

  cmgCandidatesTag_		= iConfig.getParameter<InputTag>	("cmgCandidatesTag");
  vertexInputTag_               = iConfig.getParameter<InputTag>        ("vertexInputTag");
  
  dR_               = iConfig.getParameter<double>          ("dR_ConeSize");       // dR value used to define the isolation cone                (default 0.3 )
  minPt_            = iConfig.getParameter<double>          ("minPt_cmgCandidate"); // store cmgCandidates with pt above this cut                 (default 0   )

  vetoCollectionTags_ =  iConfig.getParameter< std::vector<edm::InputTag> >("vetoCollections");  

  produces<vector<float> >("pfcandstrkiso").setBranchAlias("pfcands_trkiso");
  produces<vector<bool>  >("pfcandsfromPV").setBranchAlias("pfcands_fromPV");
  produces<vector<float> >("pfcandspt"    ).setBranchAlias("pfcands_pt");
  produces<vector<int>   >("pfcandschg"   ).setBranchAlias("pfcands_chg");
    
}

TrackIsolationMakerSUS::~TrackIsolationMakerSUS() 
{

}

void  TrackIsolationMakerSUS::beginRun(edm::Run&, const edm::EventSetup& es) {}
void  TrackIsolationMakerSUS::beginJob() {}
void  TrackIsolationMakerSUS::endJob()   {}

// ------------ method called to produce the data  ------------

void TrackIsolationMakerSUS::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  auto_ptr<vector<float> >  pfcands_trkiso(new vector<float>);
  auto_ptr<vector<bool> >   pfcands_fromPV(new vector<bool>);
  auto_ptr<vector<float> >  pfcands_pt    (new vector<float>);
  auto_ptr<vector<int>   >  pfcands_chg   (new vector<int>  );

  //---------------------------------
  // get cmgCandidate collection
  //---------------------------------
  
  Handle<cmgCandidateCollection> cmgCandidatesHandle;
  iEvent.getByLabel(cmgCandidatesTag_, cmgCandidatesHandle);
  cmgCandidates  = cmgCandidatesHandle.product();

  //---------------------------------
  // get Vertex Collection
  //---------------------------------
  
  Handle<reco::VertexCollection> vertex_h;
  iEvent.getByLabel(vertexInputTag_, vertex_h);
  const reco::VertexCollection *vertices = vertex_h.product();

  //-----------------------------------
  // Find 1st good vertex
  //-----------------------------------

  VertexCollection::const_iterator firstGoodVertex = vertices->end();

  int firstGoodVertexIdx = 0;

  for (VertexCollection::const_iterator vtx = vertices->begin(); vtx != vertices->end(); ++vtx, ++firstGoodVertexIdx) {
    if (  !vtx->isFake() && vtx->ndof()>=4. && vtx->position().Rho()<=2.0 && fabs(vtx->position().Z())<=24.0) {
      firstGoodVertex = vtx;
      break;
    }
  }

  //-----------------------------------
  // get veto collections' candidates
  //----------------------------------
  std::vector< std::pair < double, double > > vetoesEtaPhi;

  for ( std::vector<edm::InputTag>::const_iterator tag = vetoCollectionTags_.begin() ; tag != vetoCollectionTags_.end() ; tag++  ){
    Handle<edm::View<reco::Candidate> > vetos;
    iEvent.getByLabel(*tag, vetos);
    for ( edm::View<reco::Candidate>::const_iterator jt = vetos->begin(); jt != vetos->end(); ++jt){
      vetoesEtaPhi.push_back( std::make_pair( jt -> eta(), jt -> phi()));
    }
  }
 

  //-------------------------------------------------------------------------------------------------
  // loop over cmgCandidates and calculate the trackIsolation and from PV for each one
  // for neutral cmgCandidates, store trkiso = 999 and fromPV = 1
  //-------------------------------------------------------------------------------------------------
  for( cmgCandidateCollection::const_iterator pf_it = cmgCandidates->begin(); pf_it != cmgCandidates->end(); pf_it++ ) {
    //-------------------------------------------------------------------------------------
    // only store cmgCandidate values if pt > minPt
    //-------------------------------------------------------------------------------------

    // if( pf_it->pt() < minPt_ ) continue;

    //-------------------------------------------------------------------------------------
    // skip candidate if it matches a veto object
    //-------------------------------------------------------------------------------------
    double dR = 1000.;
    for ( std::vector< std::pair < double, double > >::const_iterator v_it = vetoesEtaPhi.begin();
	  v_it != vetoesEtaPhi.end();
	  v_it++){
      
      dR = min(dR, reco::deltaR( pf_it -> eta(), pf_it -> phi(), v_it -> first, v_it -> second  ));
    }
    if (dR < 0.02)
      continue;
    //-------------------------------------------------------------------------------------
    // store pt and charge of cmgCandidate
    //-------------------------------------------------------------------------------------

    pfcands_pt->push_back(pf_it->pt());
    pfcands_chg->push_back(pf_it->charge());

    //-------------------------------------------------------------------------------------
    // if there's no good vertex in the event, we can't calculate anything so store 999999
    //-------------------------------------------------------------------------------------
    
    if ( firstGoodVertex==vertices->end() ) {
      pfcands_trkiso->push_back(999);
      pfcands_fromPV->push_back(1);
      continue;
    }

    //-------------------------------------------------------
    // require cmgCandidate is charged, otherwise store 999 
    //-------------------------------------------------------

    if( pf_it->charge() != 0 ){

      //----------------------------------------------------------------------------
      // now loop over other cmgCandidates in the event to calculate trackIsolation
      //----------------------------------------------------------------------------

      float trkiso = 0.0;

      for( cmgCandidateCollection::const_iterator pf_other = cmgCandidates->begin(); pf_other != cmgCandidates->end(); pf_other++ ) {

	// don't count the cmgCandidate in its own isolation sum
	if( pf_it == pf_other       ) continue;

	// require the cmgCandidate to be charged
	if( pf_other->charge() == 0 ) continue;

        // cut on dR between the cmgCandidates
        float dR = deltaR(pf_it->eta(), pf_it->phi(), pf_other->eta(), pf_other->phi());
        if( dR > dR_ ) continue;

	// check that the PFCandidate comes from the PV (we want to use only PV particles in the iso sum)
	//if( not( pf_other->fromPV()) ) continue;

	trkiso += pf_other->pt();
      }

      // store trkiso and fromPV values
      pfcands_trkiso->push_back(trkiso);
      pfcands_fromPV->push_back(1);//pf_it -> fromPV());

    }else{
      //neutral particle, set trkiso and fromPV to 9999, true
      pfcands_trkiso->push_back(9999);
      pfcands_fromPV->push_back(1);
    }

  }
  
            
  // put trkiso and from PV values back into event
  iEvent.put(pfcands_trkiso,"pfcandstrkiso");
  iEvent.put(pfcands_fromPV,"pfcandsfromPV"  );
  iEvent.put(pfcands_pt    ,"pfcandspt"    );
  iEvent.put(pfcands_chg   ,"pfcandschg"   );
 
}

//define this as a plug-in
DEFINE_FWK_MODULE(TrackIsolationMakerSUS);

