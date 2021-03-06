import FWCore.ParameterSet.Config as cms

analysisVertices = cms.EDFilter("VertexSelector",
   src = cms.InputTag("goodOfflinePrimaryVertices"),
   cut = cms.string("!isFake && ndof > 4 && abs(z) <= 15 && position.Rho <= 2"),
   filter = cms.bool(False),
)
