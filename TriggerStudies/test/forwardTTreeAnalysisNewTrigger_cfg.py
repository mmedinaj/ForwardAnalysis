import FWCore.ParameterSet.Config as cms

# Settings
class config: pass
config.verbose = True
config.writeEdmOutput = False
config.outputTTreeFile = 'forwardTTreeAnalysis.root'
config.runOnMC = False
config.runPATSequences = False
config.usePAT = False
#config.globalTagNameData = 'GR_R_52_V7::All'
config.globalTagNameData = 'GR_R_42_V23::All' 
#config.globalTagNameData = 'GR_R_42_V19::All' 
#config.instLumiROOTFile='/storage2/eliza/lumibyXing_Cert_160404-176023_7TeV_PromptReco_Collisions11_JSON.root'
config.instLumiROOTFile=''
#config.globalTagNameMC = 'START42_V14A::All'
config.globalTagNameMC = 'START42_V17::All'
config.comEnergy = 7000.0
config.trackAnalyzerName = 'trackHistoAnalyzer'
config.trackTagName = 'analysisTracks'
##PAT INFO does not using Asterisk, yet.

if config.runOnMC:
    #config.l1Paths = ('ALL')
    config.l1Paths = ('L1_ZeroBias','L1_BptxMinus_NotBptxPlus','L1_SingleJet30U')
    config.hltPaths =('HLT_Jet30_v1','HLT_Jet30_v2','HLT_Jet30_v3','HLT_Jet30_v4','HLT_Jet30_v5','HLT_Jet30_v6')
else:
    #config.l1Paths = ('L1_ZeroBias','L1_BptxMinus_NotBptxPlus','L1_SingleJet30U')
    #config.hltPaths = ('HLT_ExclDiJet30U_HFOR_v1','HLT_DiJetAve100U_v1')
    config.l1Paths = ('L1_SingleJet16','L1_SingleJet36','L1_SingleJet36_FwdVeto')
    config.hltPaths = ('HLT_ExclDiJet60_HFOR_v*','HLT_ExclDiJet60_HFAND_v*','HLT_Jet60_v*' )
    #config.hltPaths = ('HLT_PFJet40_v*','HLT_L1SingleJet16_v*','HLT_DiPFJetAve80_v*','HLT_L1SingleJet36_v*','HLT_ExclDiJet80_HFAND_v*','HLT_ExclDiJet35_HFAND_v*','HLT_ExclDiJet35_HFOR_v*')
    #config.hltPaths = ('HLT_ExclDiJet30U_HFAND_v*','HLT_ExclDiJet30U_HFOR_v*','HLT_Jet30U*')

if config.runOnMC:
    config.inputFileName = '/storage2/eliza/samples_test/QCD_Pt-15to30_TuneZ2_7TeV_pythia6AODSIMS_3.root'# MC
else:
    #config.inputFileName = 'rfio:/castor/cern.ch/cms/store/data/Run2012A/Jet/RAW/v1/000/193/336/6CE0FC0F-7995-E111-BC9D-001D09F2B2CF.root'
    config.inputFileName = '/storage1/eliza/Commissioning_RunB2011_Raw_175834.root'
        # '/storage1/eliza/MultiJet_Run2011B178970_RAW.root'
        # 'rfio:/castor/cern.ch/cms/store/data/Run2011B/L1JetHPF/RAW/v1/000/179/828/FE539B1D-2CFF-E011-9C7F-BCAEC5364C6C.root'

        # '/storage1/eliza/MultiJet_Run2011B178970_RAW.root'
        # '/storage1/eliza/MultiJet_v1_RAW.root' 
        # '/storage1/eliza/MultiJet_RECO_PromptReco_v4.root' 
        #'/storage2/antoniov/data1/MultiJet_Run2010B_Apr21ReReco-v1_AOD/MultiJet_Run2010B_Apr21ReReco-v1_AOD_7EA7B611-7371-E011-B164-002354EF3BDB.root' 
        #'rfio:/castor/cern.ch/cms/store/data/Run2012A/Jet/RAW/v1/000/193/686/D80B9D30-5999-E111-8DAF-003048D2BC4C.root',
        #'rfio:/castor/cern.ch/cms/store/data/Run2012A/Jet/RAW/v1/000/193/676/8CF36755-3C99-E111-B084-0025B3203898.root'
#'rfio:/castor/cern.ch/cms/store/data/Run2012A/Jet/RECO/PromptReco-v1/000/190/895/BCF66AEE-2685-E111-8B36-BCAEC518FF62.root'

process = cms.Process("Analysis")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.options = cms.untracked.PSet(
	wantSummary = cms.untracked.bool(True),
	SkipEvent = cms.untracked.vstring('ProductNotFound')
	)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( 'file:%s' % config.inputFileName )
    #duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)


#---------------------------------------------------------------------------------
# Output
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(config.outputTTreeFile))


process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryExtended_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
#process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
if config.runOnMC: process.GlobalTag.globaltag = config.globalTagNameMC
else: process.GlobalTag.globaltag = config.globalTagNameData

#process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
#process.load('RecoJets.Configuration.RecoPFJets_cff')
#process.load('RecoJets.Configuration.RecoJets_cff')
process.load('CommonTools/RecoAlgos/HBHENoiseFilterResultProducer_cfi')
from RecoLuminosity.LumiProducer.lumiProducer_cff import *
process.load('RecoLuminosity.LumiProducer.lumiProducer_cff')
###Fragmento do menu de 2011
process.load('ForwardAnalysis.TriggerStudies.hlt_2011_cff')
# create the jetMET HLT reco path
process.DoHLTJets = cms.Path(
    process.HLTBeginSequence +
    process.HLTRecoJetSequenceAK5Corrected +
    process.HLTRecoJetSequenceAK5L1FastJetCorrected +
    process.HLTRecoMETSequence #+
    #HLTDoLocalHcalWithoutHOSequence +                 
    #OpenHLTHCalNoiseTowerCleanerSequence
)
##############################
if config.runPATSequences:
    from ForwardAnalysis.Skimming.addPATSequences import addPATSequences
    addPATSequences(process,config.runOnMC)

    if config.runOnMC:
	process.patTrigger.addL1Algos = cms.bool( False )
	process.patJets.addTagInfos   = cms.bool( False )
    else:
	process.patTrigger.addL1Algos = cms.bool( True )
	process.patJets.addTagInfos   = cms.bool( True )   

from ForwardAnalysis.Utilities.addCastorRecHitCorrector import addCastorRecHitCorrector
addCastorRecHitCorrector(process)


process.load("ForwardAnalysis.ForwardTTreeAnalysis.commonAnalysisSequences_cff")
#process.load("ForwardAnalysis.ForwardTTreeAnalysis.exclusiveDijetsAnalysisSequences_cff")
#######################################################################################################################
# Analysis modules
#--------------------------------
## from ForwardAnalysis.Utilities.countsAnalyzer_cfi import countsAnalyzer
## if not config.runOnMC:
##     process.load('ForwardAnalysis.Utilities.lumiWeight_cfi')
##     process.lumiWeight.rootFileName = cms.string(config.instLumiROOTFile)

## if not config.runOnMC:
##     process.eventWeightSequence = cms.Sequence(process.lumiWeight) 
##     process.eventWeight_step = cms.Path(process.eventWeightSequence)
############################################################################################################## 
process.pfCandidateNoiseThresholds.src = "pfNoPileUpPFlow"
process.tracksTransverseRegion.JetTag = "selectedPatJetsPFlow"

########################################################################

from ForwardAnalysis.ForwardTTreeAnalysis.DiffractiveAnalysis_cfi import DiffractiveAnalysis
from ForwardAnalysis.ForwardTTreeAnalysis.ExclusiveDijetsAnalysis_cfi import ExclusiveDijetsAnalysis
from ForwardAnalysis.ForwardTTreeAnalysis.PATTriggerInfo_cfi import PATTriggerInfo
from ForwardAnalysis.ForwardTTreeAnalysis.DijetsTriggerAnalysis_cfi import DijetsTriggerAnalysis  
#PATTriggerInfo.L1AlgoBitName =  config.l1Paths 
#PATTriggerInfo.HLTAlgoBitName = config.hltPaths 
PATTriggerInfo.runALLTriggerPath = True

process.dijetsTriggerAnalysisTTree = cms.EDAnalyzer("DijetsTriggerAnalysisTTree",
        DijetsTriggerAnalysis = DijetsTriggerAnalysis,
        #PATTriggerInfo = PATTriggerInfo 
        )

process.patInfoTTree = cms.EDAnalyzer("PATTriggerInfoTTree",
	PATTriggerInfo = PATTriggerInfo
	)
process.diffractiveAnalysisTTree = cms.EDAnalyzer("DiffractiveAnalysisTTree",
	DiffractiveAnalysis = DiffractiveAnalysis
	)
process.diffractiveAnalysisPATTriggerInfoTTree = cms.EDAnalyzer("DiffractiveAnalysisPATTriggerInfoTTree",
	DiffractiveAnalysis = DiffractiveAnalysis,
	PATTriggerInfo = PATTriggerInfo
	)
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree = cms.EDAnalyzer("DiffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree",
	DiffractiveAnalysis = DiffractiveAnalysis,
        ExclusiveDijetsAnalysis = ExclusiveDijetsAnalysis,
	PATTriggerInfo = PATTriggerInfo
	)
process.diffractiveAnalysisTTree.DiffractiveAnalysis.hltPath = ''
process.diffractiveAnalysisPATTriggerInfoTTree.DiffractiveAnalysis.hltPath = ''

#process.exclusiveDijetsHLTFilter.HLTPaths = ['HLT_ExclDiJet80_HFAND_v*','HLT_ExclDiJet35_HFAND_v*','HLT_ExclDiJet35_HFOR_v*','HLT_L1SingleJet16_v*','HLT_DiPFJetAve80_v*','HLT_L1SingleJet36_v*']
#process.exclusiveDijetsHLTFilter.HLTPaths = config.hltPaths 

process.load('HLTrigger/HLTfilters/hltHighLevel_cfi')
process.hltHighLevel.TriggerResultsTag =cms.InputTag("TriggerResults","","HLT")
process.hltHighLevel.HLTPaths = ['HLT_ExclDiJet60_HFAND_v*','HLT_ExclDiJet60_HFOR_v*','HLT_Jet60_v*']
process.hltHighLevel.andOr = True # True = OR, False = AND

process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.DiffractiveAnalysis.hltPath = ''
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.DiffractiveAnalysis.trackTag = 'analysisTracks'
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.DiffractiveAnalysis.vertexTag = "offlinePrimaryVertices"
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.DiffractiveAnalysis.particleFlowTag = "pfCandidateNoiseThresholds"
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.DiffractiveAnalysis.jetTag = "selectedPatJetsPFlow"

process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.ExclusiveDijetsAnalysis.hltPaths = config.hltPaths 
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.ExclusiveDijetsAnalysis.TrackTag = 'analysisTracks'
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.ExclusiveDijetsAnalysis.VertexTag = "offlinePrimaryVertices"
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.ExclusiveDijetsAnalysis.ParticleFlowTag = "pfCandidateNoiseThresholds"
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.ExclusiveDijetsAnalysis.JetTag = "selectedPatJetsPFlow"
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.ExclusiveDijetsAnalysis.JetNonCorrTag = "ak5PFJets"
if config.runOnMC:
     process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.DiffractiveAnalysis.accessMCInfo = True
     process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.ExclusiveDijetsAnalysis.AccessMCInfo = True
else:
     process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.DiffractiveAnalysis.accessMCInfo = False 
     process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.ExclusiveDijetsAnalysis.AccessMCInfo = False 

#########################################################################
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF0 = process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.clone()
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF0.DiffractiveAnalysis.energyThresholdHF = 0.0
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF4 = process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.clone()
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF4.DiffractiveAnalysis.energyThresholdHF = 4.0
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF8 = process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.clone()
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF8.DiffractiveAnalysis.energyThresholdHF = 8.0
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF10 = process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree.clone()
process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF10.DiffractiveAnalysis.energyThresholdHF = 10.0


##########################################################################
if config.runOnMC:
  process.gen_step = cms.Path(process.genChargedParticles+
                              process.genProtonDissociative*process.edmNtupleMxGen+
                              process.genStableParticles*
                              process.etaMaxGen+process.etaMinGen*
                              process.edmNtupleEtaMaxGen+process.edmNtupleEtaMinGen)


process.analysis_reco_step = cms.Path(process.analysisSequences)
process.castor_step = cms.Path(process.castorSequence)

#process.analysis_patInfoTTree_step = cms.Path(process.patInfoTTree)
#process.analysis_diffractiveAnalysisTTree_step = cms.Path(process.diffractiveAnalysisTTree)
#process.analysis_dijetsTriggerAnalysisPATTriggerInfoTTree_step = cms.Path(process.exclusiveDijetsHLTFilter + process.dijetsTriggerAnalysisTTree)
#process.analysis_diffractiveAnalysisPATTriggerInfoTTree_step = cms.Path(process.diffractiveAnalysisPATTriggerInfoTTree)

#process.analysis_diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_step = cms.Path(
#    process.eventSelectionHLT +
#    process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree
#)

process.analysis_dijetsTriggerAnalysisTTree_step = cms.Path(process.lumiProducer + process.hltHighLevel + process.dijetsTriggerAnalysisTTree)
process.schedule = cms.Schedule( process.DoHLTJets, process.analysis_dijetsTriggerAnalysisTTree_step)

#process.analysis_diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_step = cms.Path(
#    process.eventSelectionHLT+
#    process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree+
#    process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF0+
#    process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF1+
#    process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF2+
#    process.diffractiveExclusiveDijetsAnalysisPATTriggerInfoTTree_HF3)
