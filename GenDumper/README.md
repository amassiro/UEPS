GenJets analysis
====


Input

    /tmp/amassiro/WW1Mevents_TUNE_CMS.root
    /tmp/amassiro/WW1Mevents_TUNE_ATLAS.root
    /tmp/amassiro/WW1Mevents_TUNE_NOUE.root
    /tmp/amassiro/WW1Mevents_TUNE_CMS_Herwig.root
    /tmp/amassiro/WW1Mevents_TUNE_CMS_Herwig_UE_bigSample.root


Now stored on eos (space problems: ~ 70 GB each)

    /eos/cms/store/user/amassiro/WW/GEN/

    eos cp /eos/cms/store/user/amassiro/WW/GEN/WW1Mevents_TUNE_CMS.root       /tmp/amassiro/
    eos cp /eos/cms/store/user/amassiro/WW/GEN/WW1Mevents_TUNE_ATLAS.root     /tmp/amassiro/
    eos cp /eos/cms/store/user/amassiro/WW/GEN/WW1Mevents_TUNE_CMS_Z2Lep.root /tmp/amassiro/


do:

    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_CMS.root                       outputFile=/tmp/amassiro/WW1Mevents_TUNE_CMS_dump_tree.root
    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_ATLAS.root                     outputFile=/tmp/amassiro/WW1Mevents_TUNE_ATLAS_dump_tree.root
    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_CMS_Herwig_UE_bigSample.root   outputFile=/tmp/amassiro/WW1Mevents_TUNE_Herwig_UE_dump_tree.root
    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_CMS_Z2Lep.root                 outputFile=/tmp/amassiro/WW1Mevents_TUNE_CMS_Z2Lep_dump_tree.root


others for testing:

    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_NoUE.root       outputFile=/tmp/amassiro/WW1Mevents_TUNE_NoUE_dump_tree.root
    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_CMS_Herwig.root outputFile=/tmp/amassiro/WW1Mevents_TUNE_Herwig_dump_tree.root
    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_CMS_Herwig_2.root outputFile=/tmp/amassiro/WW1Mevents_TUNE_Herwig_dump_tree_2.root

    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_CMS_Herwig_UE.root             outputFile=/tmp/amassiro/WW1Mevents_TUNE_Herwig_UE_dump_tree.root
    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_CMS_Herwig_UE_bigSample.root   outputFile=/tmp/amassiro/WW1Mevents_TUNE_Herwig_UE_dump_tree.root

    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_CMS_Herwig_UE.root             outputFile=/tmp/amassiro/WW1Mevents_TUNE_Herwig_UE_dump_tree_TEST.root

    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_CMS.root             outputFile=/tmp/amassiro/WW1Mevents_TUNE_CMS_dump_tree_TEST.root








