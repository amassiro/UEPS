UEPS
====

Underlying event and parton shower


where:

    cmsneu
    /home/amassiro/Generation/UEPS


Perform GEN step only with CMSSW.

Transform in edm format:

    cp /home/amassiro/Generation/MINLO/POWHEG-BOX/WW/testAM_1M_events/pwgevents-rwgt.lhe /tmp/amassiro/WW1Mevents.lhe
    cmsDriver.py MCDBtoEDM --conditions START53_V7C::All -s NONE --eventcontent RAWSIM --datatier GEN --filein file:/tmp/amassiro/WW1Mevents.lhe --fileout /tmp/amassiro/WW1Mevents.root -n -1


Prepare standard GEN:

    cmsDriver.py     --step GEN        --beamspot Realistic8TeVCollision    --pileup NoPileUp         --datamix NODATAMIXER        --eventcontent RAWSIM     --datatier GEN-SIM         --conditions auto:mc         --filein file:/tmp/amassiro/WW1Mevents.root         --fileout /tmp/amassiro/WW1Mevents_TUNE.root


Modify the file to plug in different tunes:




