GenJets analysis
====


Input

    /tmp/amassiro/WW1Mevents_TUNE_CMS.root
    /tmp/amassiro/WW1Mevents_TUNE_ATLAS.root
    /tmp/amassiro/WW1Mevents_TUNE_NOUE_2.root


do:

    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_CMS.root       outputFile=/tmp/amassiro/WW1Mevents_TUNE_CMS_dump_tree.root
    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_ATLAS.root     outputFile=/tmp/amassiro/WW1Mevents_TUNE_ATLAS_dump_tree.root
    cmsRun gendumper_cfg.py   inputFiles=file:/tmp/amassiro/WW1Mevents_TUNE_NoUE.root      outputFile=/tmp/amassiro/WW1Mevents_TUNE_NoUE_dump_tree.root






