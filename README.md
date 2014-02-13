UEPS
====

Underlying event and parton shower


where:

    cmsneu
    /home/amassiro/Generation/UEPS/CMSSW_5_3_14_patch2/src/UEPS/


Perform GEN step only with CMSSW.

Where:

    /home/amassiro/Generation/UEPS/CMSSW_5_3_14_patch2/src


Transform in edm format:

    cp /home/amassiro/Generation/MINLO/POWHEG-BOX/WW/testAM_1M_events/pwgevents-rwgt.lhe /tmp/amassiro/WW1Mevents.lhe
    cmsDriver.py MCDBtoEDM --conditions START53_V7C::All -s NONE --eventcontent RAWSIM --datatier GEN --filein file:/tmp/amassiro/WW1Mevents.lhe --fileout /tmp/amassiro/WW1Mevents.root -n -1

    cmsDriver.py MCDBtoEDM --conditions START53_V7C::All -s NONE --eventcontent RAWSIM --datatier GEN --filein file:/tmp/amassiro/WW1Mevents_lvlv_emutau.lhe --fileout /tmp/amassiro/WW1Mevents_lvlv_emutau.root -n -1


Prepare standard GEN:

    cmsDriver.py   BLA.py  --step GEN        --beamspot Realistic8TeVCollision    --pileup NoPileUp         --datamix NODATAMIXER        --eventcontent RAWSIM     --datatier GEN-SIM         --conditions auto:mc         --filein file:/tmp/amassiro/WW1Mevents.root         --fileout /tmp/amassiro/WW1Mevents_TUNE.root   --no_exec


Modify the file to plug in different tunes:

As a reference:

    https://amassiro.web.cern.ch/amassiro/HWW/Plot/CFG/UE/POWHEG_PYTHIA6_Tauola_H_WW_lnulnu_withTau_8TeV_NOUE_cff.py
    /afs/cern.ch/user/a/amassiro/public/4Javi/PythiaATLAStune/PythiaAUEt2BSettings_cfi.py

To obtain:

    ATLAS_py_GEN.py
    NoUE_py_GEN.py
    CMS_py_GEN.py  -> just as a reference with nominal tune
    CMS_Herwig_py_GEN.py


to Run:

    cmsRun ATLAS_py_GEN.py
    cmsRun CMS_py_GEN.py
    cmsRun NoUE_py_GEN.py
    cmsRun CMS_Herwig_py_GEN.py




====
# GenJets analysis dumper

See GenDumper folder and readme

====
# Draw

do:

    r00t Draw.cxx









