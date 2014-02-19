import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('analysis')

# add a list of strings for events to process
options.parseArguments()


process = cms.Process("SimpleGenDumper")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring (options.inputFiles),
    #fileNames = cms.untracked.vstring('file:/tmp/amassiro/WW1Mevents_TUNE_NoUE_2.root')
)

process.TFileService = cms.Service("TFileService",
      #fileName = cms.string("/tmp/amassiro/WW1Mevents_TUNE_NoUE_2_dump_tree.root"),
      fileName = cms.string (options.outputFile),
      closeFileFast = cms.untracked.bool(True)
)

process.Analyzer = cms.EDAnalyzer('GenDumper',
     GenJetCollection       = cms.InputTag("ak5GenJets"),
     GenParticlesCollection = cms.InputTag("genParticles")
)


process.p = cms.Path(process.Analyzer)
