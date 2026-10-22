PSWeights
====

Check if the parton shower weights (PSWeight, ISR and FSR variations) change the normalization of a nanoAOD sample.

For each sample, on all the events, no selections:

    R[i] = sum( genWeight * PSWeight[i] ) / sum( genWeight )

$$
R_i = \frac{\sum_k \mathrm{genWeight}_k \cdot \mathrm{PSWeight}[i]_k}{\sum_k \mathrm{genWeight}_k}
$$

i.e. the yield with the PSWeight[i] variation over the nominal yield (only genWeight), on the same events.
PSWeight is already w_var / w_nominal, so genWeight * PSWeight[i] is the event weight with the parton shower variation.
No other weights are used (cross section, luminosity, scale factors): constant factors per sample cancel in the ratio.

R = 1 means the PSWeight[i] variation is a pure shape variation.

The uncertainty on R is the MC statistical one, from the sum of the squared weights
(A and B of R = A/B are correlated, same events: delta method, var(R) = sum_k [ w_k (PSWeight_k - R) ]^2 / B^2).

$$
\sigma_{R_i}^2 = \frac{\sum_k w_k^2 \left( p_k - R_i \right)^2}{\left( \sum_k w_k \right)^2}, \qquad w_k = \mathrm{genWeight}_k, \quad p_k = \mathrm{PSWeight}[i]_k
$$

NB: PSWeight convention, from the nanoAOD documentation (recent versions):

    [0] is ISR=2   FSR=1
    [1] is ISR=1   FSR=2
    [2] is ISR=0.5 FSR=1
    [3] is ISR=1   FSR=0.5

The script prints the PSWeight branch description from the first file of each sample: check it, the order was different in some old nanoAOD versions.

NB: if nPSWeight is smaller than the index (e.g. dummy PSWeight with only 1 element), PSWeight = 1 is used and a warning with the number of such events is printed.

NB: the sum of genWeight is cross-checked with genEventSumw from the Runs tree.
If PSSumw is available in the Runs tree, it is printed as a cross-check too (assumed normalized as LHEScaleSumw: to be checked).


where:

    lxplus
    /afs/cern.ch/user/a/amassiro/work/UEPS/PSWeights/


First, the grid proxy (needed to query DAS and to read the files via xrootd):

    voms-proxy-init -voms cms -rfc -valid 192:00


Setup:

    ROOT (python3) and dasgoclient, e.g. any recent CMSSW release (cmsenv), or:

    source /cvmfs/sft.cern.ch/lcg/views/LCG_109a/x86_64-el9-gcc13-opt/setup.sh
    export PATH=/cvmfs/cms.cern.ch/common:$PATH

Run:

    python3 checkPSWeights.py  -s  /WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM

Where:

    -s, --samples     dataset names, as in DAS (wildcards allowed, more than one sample allowed)
    -i, --indices     PSWeight indices to check (default: 0 1 2 3)
    -n, --maxFiles    max number of files per dataset, for a quick test (default: -1 = all)
    -r, --redirector  xrootd redirector (default: root://cms-xrd-global.cern.ch/)
    -j, --threads     number of threads (default: 4, 0 = no multithreading)
    -o, --output      text file with the summary (dataset, index, R, error)
    -p, --plotDir     folder for the plots (default: plots)
    -b, --binning     binning of the PSWeight histograms: nbins min max (default: 200 0 4)
    -l, --linear      linear y axis in the plots (default: log)

Plots:

    one TCanvas per dataset, with the distributions of PSWeight[i] for all the requested indices,
    weighted with genWeight (the weighted mean of each histogram is R[i]), only events with nPSWeight > i.
    The legend shows the meaning of each PSWeight[i] (e.g. ISR up (x2)), read from the PSWeight branch description of the file.
    The canvas is not shown on screen, it is only saved as:

    plots/PSWeights_<sample>.png
    plots/PSWeights_<sample>.root

    together with the list of the files used (also printed on screen):

    plots/PSWeights_<sample>_list_files.txt

    where <sample> is the first part of the DAS name, e.g. PSWeights_WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8.png
    (if the same sample appears in more campaigns, the campaign is added, e.g. PSWeights_WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8__Run3Summer22NanoAODv12.png)


Examples:

    # quick test, ISR only, 2 files
    python3 checkPSWeights.py  -s /WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-*/NANOAODSIM  -i 0 2  -n 2

    # more samples, summary in a file
    python3 checkPSWeights.py  -s /WWto2L2Nu*/Run3Summer22NanoAODv12-*/NANOAODSIM  /TTto2L2Nu*/Run3Summer22NanoAODv12-*/NANOAODSIM  -o summary.txt

NB: the dataset names above are just examples, check them in DAS:

    dasgoclient -query="dataset dataset=/WWto2L2Nu*/Run3Summer22NanoAODv12*/NANOAODSIM"

NB: running on the full dataset reads all the events via xrootd: it may take a while. Use -n for a quick test.


Post-processed (latino) trees
====

Same study, with checkPSWeightsLatino.py, on the post-processed (latino) trees, e.g. in /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/...
Same options and same plots, but the input is a folder and the latino sample names, as in nanoLatino_<sample>__part*.root (wildcards allowed).

Run:

    python3 checkPSWeightsLatino.py  -d /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9  -s WWTo2L2Nu  TTTo2L2Nu

    python3 checkPSWeightsLatino.py  -d /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9  -s "WW*"  -n 5

Where:

    -d, --directory   folder with the latino trees
    -s, --samples     latino sample names (wildcards allowed, quote them: "WW*")
    -a, --all         test all the samples in the folder (all the nanoLatino_<sample>__part*.root), instead of -s
    --results         text file with one line per sample: name and the ratios R[i] (default: results.txt)
    -n, --maxFiles    max number of files (parts) per sample (default: -1 = all)
    -r, --redirector  xrootd redirector, if the folder is not visible locally (default: root://eoscms.cern.ch/)
    other options as for checkPSWeights.py

All the samples in a folder:

    python3 checkPSWeightsLatino.py  -d /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9  -a

The list of the samples to test (with the number of files) is printed first, then for each sample:

    running on sample WWTo2L2Nu, 16.7 % of files analyzed

where the percentage is the number of files of the samples already analyzed over the total number of files to analyze
(all the nanoLatino files in the folder with -a; fewer with -n). The progress is updated sample by sample.

At the end (and updated after each sample), results.txt (option --results) has one line per sample, with the name and the ratios R[i]:

    # name  R[0]  R[1]  R[2]  R[3]
    WWTo2L2Nu  1.021300  0.998700  0.979000  1.000500

(nan if the sample could not be analyzed, e.g. no PSWeight branch)

The files are found with glob if the folder is visible (e.g. /eos mounted), otherwise with xrdfs.
The plots are named after the latino sample name:

    plots/PSWeights_latino_NLeptons_<sample>.png
    plots/PSWeights_latino_NLeptons_<sample>.root
    plots/PSWeights_latino_NLeptons_<sample>_list_files.txt   (list of the files used, also printed on screen)

    e.g. plots/PSWeights_latino_NLeptons_WWTo2L2Nu.root

NB: the latino trees are skimmed (e.g. l1loose, l2tight): R is the normalization change of the PSWeight variation inside the skim,
not on the full sample. The ratio

    sum genWeight (Events) / sum genEventSumw (Runs)

is printed too: it is the (weighted) skim efficiency (1 for the full nanoAOD).
For the normalization on the full sample, use checkPSWeights.py on the DAS nanoAOD.


Expected yields
====

calculateYield.py: expected yield of each sample in a folder of post-processed (latino) trees, each sample independently.

$$
N = L \cdot \sum_k \mathrm{XSWeight}_k , \qquad \sigma_N = L \cdot \sqrt{\sum_k \mathrm{XSWeight}_k^2}
$$

    N = lumi * sum( XSWeight ),   uncertainty (MC statistics) = lumi * sqrt( sum( XSWeight^2 ) )

XSWeight = baseW * genWeight, with baseW = xsec [pb] * 1000 / sum( genWeight ) of the full generated sample:
sum( XSWeight ) is the number of expected events for 1/fb, i.e. the cross section in fb, inside the skim.

NB: sum( genWeight ) alone is NOT a yield, genWeight has an arbitrary normalization.

NB: samples post-processed with xsec = 1 (e.g. private samples) need the cross section by hand.

Run:

    # all the samples in the folder
    python3 calculateYield.py  -d /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9

    # only the underlying event variations
    python3 calculateYield.py  -d <folder>  -s "*CP5Up*" "*CP5Down*"

    # all but some samples
    python3 calculateYield.py  -d <folder>  -x "*_PSWeights*" "DYJets*"

Where:

    -d, --directory   folder with the latino trees
    -s, --samples     samples to analyze, wildcards allowed, quote them (default: all)
    -x, --exclude     samples NOT to analyze, wildcards allowed, quote them
    -w, --weight      weight of each event (default: XSWeight)
    -L, --lumi        luminosity in 1/fb (default: 1, i.e. the yield is the cross section in fb)
    -n, --maxFiles    max number of files (parts) per sample (default: -1 = all). NB: the yield is then only of these files
    -r, --redirector  xrootd redirector, if the folder is not visible locally (default: root://eoscms.cern.ch/)
    -j, --threads     number of threads (default: 4)
    -o, --output      results file (default: results_yield.txt)

The sample names are matched exactly (nanoLatino_<sample>__part*.root): -s WWTo2L2Nu does not include WWTo2L2Nu_CP5Up.

Output, results_yield.txt, written again after each sample (not only at the end):

    # folder: ...
    # weight: XSWeight, lumi = 1.0 /fb
    # name  nFiles  nEvents  yield  uncertainty
    TTTo2L2Nu_CP5Down  10  123456  1234.5  6.7

(nan if the sample could not be analyzed, e.g. missing branch)
