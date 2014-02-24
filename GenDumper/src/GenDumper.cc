// -*- C++ -*-
//
// Package:    GenDumper
// Class:      GenDumper
// 
/**\class GenDumper GenDumper.cc UEPS/GenDumper/src/GenDumper.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Andrea Massironi,42 2-027,+41227662346,
//         Created:  lun feb 10 17:03:36 CET 2014
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"


//---- for auto-tree
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"



//---- for GenParticles
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
// #include "DataFormats/Candidate/interface/Candidate.h"

//---- for GenJets
#include "DataFormats/JetReco/interface/GenJet.h" 

//---- for DeltaR
#include "Math/VectorUtil.h"
//---- for DeltaPhi
#include "DataFormats/Math/interface/deltaPhi.h"

//---- for LHE information
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

//
// class declaration
//

class GenDumper : public edm::EDAnalyzer {
   public:
      explicit GenDumper(const edm::ParameterSet&);
      ~GenDumper();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      bool ifJetALepton(float phi, float eta, edm::Handle<reco::GenParticleCollection> genParticles);

      // ----------member data ---------------------------
      // ----------member data ---------------------------
      edm::InputTag GenJetCollection_;
      edm::InputTag GenParticlesCollection_;
      edm::InputTag mcLHEEventInfoTag_;

      TTree* myTree_;
      int njet_;
      float jetpt_[10];
      float jeteta_[10];
      float lhejetpt_[10];
      float lhejeteta_[10];

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
GenDumper::GenDumper(const edm::ParameterSet& iConfig)

{
 //now do what ever initialization is needed
 GenJetCollection_       = iConfig.getParameter<edm::InputTag>("GenJetCollection");
 GenParticlesCollection_ = iConfig.getParameter<edm::InputTag>("GenParticlesCollection");
 mcLHEEventInfoTag_      = iConfig.getParameter<edm::InputTag>("mcLHEEventInfoTag");

 edm::Service<TFileService> fs ;
 myTree_ = fs -> make <TTree>("myTree","myTree");

 myTree_ -> Branch("njet", &njet_, "njet/I");
 myTree_ -> Branch("jetpt1", &jetpt_[0], "jetpt1/F");
 myTree_ -> Branch("jetpt2", &jetpt_[1], "jetpt2/F");
 myTree_ -> Branch("jetpt3", &jetpt_[2], "jetpt3/F");
 myTree_ -> Branch("jetpt4", &jetpt_[3], "jetpt4/F");
 myTree_ -> Branch("jeteta1", &jeteta_[0], "jeteta1/F");
 myTree_ -> Branch("jeteta2", &jeteta_[1], "jeteta2/F");
 myTree_ -> Branch("jeteta3", &jeteta_[2], "jeteta3/F");
 myTree_ -> Branch("jeteta4", &jeteta_[3], "jeteta4/F");

 myTree_ -> Branch("lhejetpt1", &lhejetpt_[0], "lhejetpt1/F");
 myTree_ -> Branch("lhejetpt2", &lhejetpt_[1], "lhejetpt2/F");
 myTree_ -> Branch("lhejetpt3", &lhejetpt_[2], "lhejetpt3/F");
 myTree_ -> Branch("lhejetpt4", &lhejetpt_[3], "lhejetpt4/F");
 myTree_ -> Branch("lhejeteta1", &lhejeteta_[0], "lhejeteta1/F");
 myTree_ -> Branch("lhejeteta2", &lhejeteta_[1], "lhejeteta2/F");
 myTree_ -> Branch("lhejeteta3", &lhejeteta_[2], "lhejeteta3/F");
 myTree_ -> Branch("lhejeteta4", &lhejeteta_[3], "lhejeteta4/F");
}


GenDumper::~GenDumper()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void GenDumper::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

 edm::Handle<reco::GenParticleCollection> genParticles;
 iEvent.getByLabel(GenParticlesCollection_,genParticles);

 edm::Handle<reco::GenJetCollection> genJet;
 iEvent.getByLabel(GenJetCollection_,genJet);

//  njet_ = (*genJet).size();
 for (int i=0; i<4; i++) {
  jetpt_[i]  = 0;
  jeteta_[i] = -99;
 }

 njet_ = 0;
 int itcount = 0;
 for (reco::GenJetCollection::const_iterator genJetIter=genJet->begin(); genJetIter!=genJet->end(); genJetIter++){
  float phi = genJetIter->phi();
  float pt  = genJetIter->pt();
  float eta = genJetIter->eta();

  bool isLepton = ifJetALepton(phi,eta,genParticles);

  if (isLepton == false) {

   if (itcount < 4) {
    jetpt_[itcount]  = pt;
    jeteta_[itcount] = eta;
   }
   if (pt > 30) njet_++;
  }
  itcount++;
 }

 //---- LHE information ----
 edm::Handle<LHEEventProduct> productLHEHandle;
 iEvent.getByLabel(mcLHEEventInfoTag_, productLHEHandle);

 lhef::HEPEUP LHEhepeup = (*(productLHEHandle.product())).hepeup();

 for (int i=0; i<4; i++) {
  lhejetpt_[i]  = 0;
  lhejeteta_[i] = -99;
 }

 itcount = 0;
 // loop over particles in the event
 for (unsigned int iPart = 0 ; iPart < LHEhepeup.IDUP.size (); ++iPart) {
  if (LHEhepeup.ISTUP.at (iPart) != 1) continue ;
  int type = abs (LHEhepeup.IDUP.at (iPart)) ;
  if ((type < 9 && type > 0) || type == 21) {
   float pt = (
     sqrt (LHEhepeup.PUP.at (iPart) [0] * LHEhepeup.PUP.at (iPart) [0] + // px
     LHEhepeup.PUP.at (iPart) [1] * LHEhepeup.PUP.at (iPart) [1]) // py
                          );
   if (itcount < 4) {
    lhejetpt_[itcount]  = pt;
   }
   itcount++;
  }
 }

 myTree_->Fill();
}


bool GenDumper::ifJetALepton(float phi, float eta, edm::Handle<reco::GenParticleCollection> genParticles) {
 bool isIt = false;
 for (reco::GenParticleCollection::const_iterator genPart = genParticles->begin(); genPart != genParticles->end(); genPart++){
  int id = abs(genPart->pdgId());
  if (id == 11 || id == 13 || id == 15) { //---- e/mu/tau

   float phig = genPart->phi();
   float etag = genPart->eta();

   float deltaR = sqrt(reco::deltaPhi(phig,phi)*reco::deltaPhi(phig,phi) + (etag-eta)*(etag-eta));
   if (deltaR < 0.001) {
    isIt = true;
   }
  }
 }
 return isIt;
}



// ------------ method called once each job just before starting event loop  ------------
void 
GenDumper::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
GenDumper::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
GenDumper::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
GenDumper::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
GenDumper::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
GenDumper::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
GenDumper::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(GenDumper);
