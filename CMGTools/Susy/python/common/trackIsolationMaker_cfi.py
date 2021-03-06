import FWCore.ParameterSet.Config as cms

trackIsolationMaker = cms.EDProducer("TrackIsolationMakerSUS",
                                     pfCandidatesTag     = cms.InputTag("pfNoPileUp"),
                                     vertexInputTag      = cms.InputTag("offlinePrimaryVertices"),
                                     dR_ConeSize         = cms.double(0.3),
                                     dz_CutValue         = cms.double(0.05),
                                     minPt_PFCandidate   = cms.double(0.0)
)
