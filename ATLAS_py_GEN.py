# Auto generated configuration file
# using: 
# Revision: 1.381.2.28 
# Source: /local/reps/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: BLA.py --step GEN --beamspot Realistic8TeVCollision --pileup NoPileUp --datamix NODATAMIXER --eventcontent RAWSIM --datatier GEN-SIM --conditions auto:mc --filein file:/tmp/amassiro/WW1Mevents.root --fileout /tmp/amassiro/WW1Mevents_TUNE.root --no_exec
import FWCore.ParameterSet.Config as cms

process = cms.Process('GEN')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring('file:/tmp/amassiro/WW1Mevents.root')
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.381.2.28 $'),
    annotation = cms.untracked.string('BLA.py nevts:1'),
    name = cms.untracked.string('PyReleaseValidation')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string('/tmp/amassiro/WW1Mevents_TUNE_ATLAS.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V7C::All', '')


process.generator = cms.EDFilter(
    "Pythia6HadronizerFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(8000.0),
    maxEventsToPrint = cms.untracked.int32(0),
    ExternalDecays = cms.PSet(
        Tauola = cms.untracked.PSet(
            UseTauolaPolarization = cms.bool(True),
            InputCards = cms.PSet(
                mdtau = cms.int32(0),
                pjak2 = cms.int32(0),
                pjak1 = cms.int32(0)
            )
        ),
        parameterSets = cms.vstring('Tauola')
    ),
    PythiaParameters = cms.PSet(
        pythiaUESettings = cms.vstring(
            'MSTU(21)=1     ! Check on possible errors during program execution', 
            'MSTJ(11)=5     ! Decay those unstable particles', 
            'MSTJ(22)=2     ! Decay those unstable particles',
            'PARJ(1)=0.073  !',
            'PARJ(2)=0.202  !',
            'PARJ(3)=0.950  !',
            'PARJ(4)=0.033  !',
            'PARJ(11)=0.309 !',
            'PARJ(12)=0.402 !',
            'PARJ(13)=0.544 !',
            'PARJ(21)=0.30  !',
            'PARJ(25)=0.628 !',
            'PARJ(26)=0.129 !',
            'PARJ(41)=0.368 !',
            'PARJ(42)=1.004 !',
            'PARJ(47)=0.873 !',
            'PARJ(71)=10    ! for which ctau  10 mm',
            'PARJ(81)=0.256 !',
            'PARJ(82)=0.830 !',
            'PARU(112)=0.192!',
            'MSTP(2)=1      ! which order running alphaS',
            'MSTP(3)=1      ! ',
            'MSTP(33)=0     ! no K factors in hard cross sections', 
            'MSTP(51)=10042 ! structure function chosen (external PDF CTEQ6L1)',
            'MSTP(52)=2     ! work with LHAPDF',
            'MSTP(64)=2     !',
            'MSTP(70)=0     !',
            'MSTP(72)=2     !',
            'MSTP(81)=21    ! multiple parton interactions 1 is Pythia default', 
            'MSTP(82)=4     ! Defines the multi-parton model',
            'MSTP(91)=1     !', 
            'MSTP(95)=6     !',
            'PARP(1)=0.192  !',
            'PARP(61)=0.192 !',
            'PARP(62)=1.13   ! ', 
            'PARP(64)=0.68   ! ', 
            'PARP(67)=1.0    ! amount of initial-state radiation',
            'PARP(72)=0.527  ! amount of initial-state radiation', 
            'PARP(77)=0.491 !',
            'PARP(78)=0.311 !',
            'PARP(80)=0.1   !',
            'PARP(82)=2.26   ! pt cutoff for multiparton interactions', 
            'PARP(83)=0.356  ! Multiple interactions: matter distrbn parameter', 
            'PARP(84)=0.443  ! Multiple interactions: matter distribution parameter', 
            'PARP(89)=1960. ! sqrts for which PARP82 is set', 
            'PARP(90)=0.249  ! Multiple interactions: rescaling power', 
            'PARP(91)=2.0    ! kt distribution', 
            'PARP(93)=10.0   ! '
            ),

        processParameters = cms.vstring(
            'MSEL=0 ! User defined processes',
            'PMAS(5,1)=4.75 ! b quark mass',
            'PMAS(6,1)=172.5 ! t quark mass',

            'MDME(190,1)=0 ! W decay into dbar u',
            'MDME(191,1)=0 ! W decay into dbar c',
            'MDME(192,1)=0 ! W decay into dbar t',
            'MDME(194,1)=0 ! W decay into sbar u',
            'MDME(195,1)=0 ! W decay into sbar c',
            'MDME(196,1)=0 ! W decay into sbar t',
            'MDME(198,1)=0 ! W decay into bbar u',
            'MDME(199,1)=0 ! W decay into bbar c',
            'MDME(200,1)=0 ! W decay into bbar t',
            'MDME(206,1)=1 ! W decay into e+ nu_e',
            'MDME(207,1)=1 ! W decay into mu+ nu_mu',
            'MDME(208,1)=0 ! W decay into tau+ nu_tau'
            ),
        parameterSets = cms.vstring(
            'pythiaUESettings',
            'processParameters'
            )
        )
    )


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RAWSIMoutput_step)

# filter all path with the production filter sequence
for path in process.paths:
    getattr(process,path)._seq = process.generator * getattr(process,path)._seq 


