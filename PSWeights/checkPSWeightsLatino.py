#!/usr/bin/env python3

#
# Same as checkPSWeights.py, but on post-processed (latino) trees, e.g. in /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/...
# Check if the parton shower weights (PSWeight) change the normalization of a sample:
#
#   R[i] = sum( genWeight * PSWeight[i] ) / sum( genWeight )
#
# Input: folder with the latino trees, and sample names as in nanoLatino_<sample>__part*.root (wildcards allowed)
# NB: latino trees are skimmed, R is then the normalization change inside the skim
#

import argparse
import subprocess
import fnmatch
import glob
import math
import os
import re
import ROOT


# ---- post-processed (latino) trees ----

listedDirectories = {}


def listDirectory(directory, redirector):
  # list the files in the folder: glob if visible (e.g. /eos mounted), otherwise xrdfs
  if directory in listedDirectories:
    return listedDirectories[directory]
  if os.path.isdir(directory):
    files = [os.path.join(directory, os.path.basename(f)) for f in glob.glob(directory + "/*.root")]
  else:
    result = subprocess.run(["xrdfs", redirector, "ls", directory], capture_output=True, text=True)
    if result.returncode != 0:
      print ("ERROR: xrdfs failed for ", directory)
      print (result.stderr)
      return []
    files = [redirector + line.strip() for line in result.stdout.split("\n") if line.strip().endswith(".root")]
  listedDirectories[directory] = files
  return files


def getLatinoSamples(directory, sample, redirector, maxFiles):
  # nanoLatino_<sample>__part<N>.root, wildcards allowed in <sample>
  samples = {}
  for fileName in listDirectory(directory, redirector):
    m = re.match(r"nanoLatino_(.+)__part(\d+)\.root$", os.path.basename(fileName))
    if m and fnmatch.fnmatch(m.group(1), sample):
      samples.setdefault(m.group(1), []).append((int(m.group(2)), fileName))
  for name in samples:
    files = [f for part, f in sorted(samples[name])]
    if maxFiles > 0:
      files = files[:maxFiles]
    samples[name] = files
  return samples


# ---- PSWeight description, from the first file ----

def getPSWeightInfo(fileName):
  f = ROOT.TFile.Open(fileName)
  if not f or f.IsZombie():
    return None, None, None
  events = f.Get("Events")
  branch = events.GetBranch("PSWeight")
  if not branch:
    f.Close()
    return None, None, None
  title = branch.GetTitle()
  # Runs tree: also PSSumw, if available in this nanoAOD version
  # (assumed to be normalized as LHEScaleSumw, i.e. divided by genEventSumw: to be checked)
  runs = f.Get("Runs")
  hasRuns = bool(runs)
  hasPSSumw = hasRuns and bool(runs.GetBranch("PSSumw"))
  f.Close()
  return title, hasRuns, hasPSSumw


# ---- meaning of each PSWeight index, from the branch description ----

def describeVariation(name, value):
  if value > 1:
    return f"{name} up (#times{value:g})"
  return f"{name} down (#times{value:g})"


def getPSWeightMeanings(title):
  # e.g. "PS weights (w_var / w_nominal);   [0] is ISR=2 FSR=1; [1] is ISR=1 FSR=2[2] is ISR=0.5 FSR=1; [3] is ISR=1 FSR=0.5;"
  meanings = {}
  for index, isr, fsr in re.findall(r"\[(\d+)\]\s*is\s*ISR\s*=\s*([\d.]+)\s*FSR\s*=\s*([\d.]+)", title):
    isr = float(isr)
    fsr = float(fsr)
    labels = []
    if isr != 1:
      labels.append(describeVariation("ISR", isr))
    if fsr != 1:
      labels.append(describeVariation("FSR", fsr))
    if len(labels) == 0:
      labels.append("nominal")
    meanings[int(index)] = ", ".join(labels)
  return meanings


# ---- the actual check ----

def checkSample(label, name, campaign, files, indices, binning, plotDir, logy):
  print ("")
  print ("---- ", label)

  if len(files) == 0:
    print ("   no files found")
    return None
  print ("   files: ", len(files))
  for fileName in files:
    print ("      ", fileName)

  title, hasRuns, hasPSSumw = getPSWeightInfo(files[0])
  if title == None:
    print ("   PSWeight not found in ", files[0])
    return None
  print ("   PSWeight: ", title)
  meanings = getPSWeightMeanings(title)
  for i in indices:
    if i not in meanings:
      print (f"   WARNING: meaning of PSWeight[{i}] not found in the branch description")

  df = ROOT.RDataFrame("Events", files)

  #
  # w = genWeight, p = PSWeight[i]
  # if nPSWeight <= i (e.g. dummy PSWeight with 1 element) --> p = 1 and the event is counted
  #
  df = df.Define("w2", "genWeight*genWeight")

  sums = {}
  histos = {}
  sums["n"]   = df.Count()
  sums["sw"]  = df.Sum("genWeight")
  sums["sw2"] = df.Sum("w2")
  for i in indices:
    df = df.Define(f"p{i}", f"nPSWeight > {i} ? PSWeight[{i}] : 1.f")
    df = df.Define(f"wp{i}", f"genWeight * p{i}")
    df = df.Define(f"w2p{i}", f"w2 * p{i}")
    df = df.Define(f"w2pp{i}", f"w2 * p{i} * p{i}")
    sums[f"swp{i}"]   = df.Sum(f"wp{i}")
    sums[f"sw2p{i}"]  = df.Sum(f"w2p{i}")
    sums[f"sw2pp{i}"] = df.Sum(f"w2pp{i}")
    sums[f"nmissing{i}"] = df.Filter(f"nPSWeight <= {i}").Count()
    # distribution of PSWeight[i], weighted with genWeight (its weighted mean is R[i])
    # only events where PSWeight[i] exists
    histos[i] = df.Filter(f"nPSWeight > {i}").Histo1D(ROOT.RDF.TH1DModel(f"h_PSWeight_{i}", "", int(binning[0]), binning[1], binning[2]), f"p{i}", "genWeight")

  # cross-check with the Runs tree
  sumRuns = None
  if hasRuns:
    dfRuns = ROOT.RDataFrame("Runs", files)
    sumRuns = dfRuns.Sum("genEventSumw")
    sums["runs"] = sumRuns
  if hasPSSumw:
    for i in indices:
      dfRuns = dfRuns.Define(f"pssumw{i}", f"nPSSumw > {i} ? PSSumw[{i}] * genEventSumw : genEventSumw")
      sums[f"runsp{i}"] = dfRuns.Sum(f"pssumw{i}")

  # run the event loop (once, all the booked results together)
  ROOT.RDF.RunGraphs([v for v in sums.values()] + [h for h in histos.values()])

  sw  = sums["sw"].GetValue()
  sw2 = sums["sw2"].GetValue()

  print ("   events = ", sums["n"].GetValue())
  print ("   sum genWeight (Events) = ", sw)
  if hasRuns:
    print ("   sum genEventSumw (Runs) = ", sumRuns.GetValue())
    # = 1 for the full nanoAOD, < 1 for skimmed (e.g. latino) trees
    print (f"   sum genWeight (Events) / sum genEventSumw (Runs) = {sw / sumRuns.GetValue():.5f}")

  results = {}
  for i in indices:
    swp   = sums[f"swp{i}"].GetValue()
    sw2p  = sums[f"sw2p{i}"].GetValue()
    sw2pp = sums[f"sw2pp{i}"].GetValue()
    R = swp / sw
    #
    # MC statistical uncertainty on R = A/B, with A and B correlated (same events)
    # delta method: var(R) = sum_k [ w_k (p_k - R) ]^2 / B^2
    #
    var = (sw2pp - 2 * R * sw2p + R * R * sw2) / (sw * sw)
    err = math.sqrt(max(var, 0.))
    results[i] = (R, err)
    line = f"   R[{i}] = sum(genWeight*PSWeight[{i}]) / sum(genWeight) = {R:.5f} +/- {err:.5f}   ({(R-1)*100:+.3f} %)"
    if hasPSSumw:
      line += f"   [Runs PSSumw: {sums[f'runsp{i}'].GetValue() / sumRuns.GetValue():.5f}]"
    if i in meanings:
      line += "   " + meanings[i].replace("#times", "x")
    print (line)
    nmissing = sums[f"nmissing{i}"].GetValue()
    if nmissing > 0:
      print (f"      WARNING: {nmissing} events with nPSWeight <= {i}: PSWeight[{i}] = 1 used for them")

  drawPSWeights(name, campaign, files, histos, results, meanings, plotDir, logy)

  return results


# ---- plot of the PSWeight distributions ----

def writeFileList(fileName, files):
  with open(fileName, "w") as fileOut:
    for f in files:
      fileOut.write(f + "\n")
  print ("   list of files written in ", fileName)

usedNames = []

def plotName(name, campaign):
  # latino sample name, e.g. WWTo2L2Nu
  # if already used (same sample, different production), add the production, e.g. __Summer20UL18_106x_nAODv9_Full2018v9
  if name in usedNames:
    name = name + "__" + campaign
  usedNames.append(name)
  return name

def drawPSWeights(sampleName, campaign, files, histos, results, meanings, plotDir, logy):
  colors = [ROOT.kGreen+3, ROOT.kRed+1, ROOT.kBlue+1, ROOT.kCyan-4, ROOT.kMagenta+1, ROOT.kOrange+7, ROOT.kGray+2, ROOT.kViolet+1]
  name = plotName(sampleName, campaign)

  cc = ROOT.TCanvas ("cc_" + name, "", 800, 600)
  if logy:
    cc.SetLogy()

  legend = ROOT.TLegend(0.38, 0.65, 0.89, 0.89)
  legend.SetTextSize(0.03)
  legend.SetBorderSize(0)
  legend.SetFillStyle(0)

  maximum = max([h.GetPtr().GetMaximum() for h in histos.values()])
  first = True
  for iColor, (i, histo) in enumerate(histos.items()):
    h = histo.GetPtr()
    h.SetLineColor(colors[iColor % len(colors)])
    h.SetLineWidth(3)
    h.SetTitle(sampleName + "  " + campaign)
    h.GetXaxis().SetTitle("PSWeight")
    h.GetYaxis().SetTitle("events (weighted with genWeight)")
    h.SetMaximum(maximum * (10. if logy else 1.2))
    h.Draw("hist" if first else "hist same")
    first = False
    R, err = results[i]
    meaning = (" " + meanings[i] + ",") if i in meanings else ","
    legend.AddEntry(h, f"PSWeight[{i}]{meaning} R = {R:.4f} #pm {err:.4f}", "l")
  legend.Draw()

  os.makedirs(plotDir, exist_ok=True)
  # e.g. PSWeights_latino_NLeptons_WWTo2L2Nu.root
  cc.SaveAs(plotDir + "/PSWeights_latino_NLeptons_" + name + ".png")
  cc.SaveAs(plotDir + "/PSWeights_latino_NLeptons_" + name + ".root")

  # list of the files used
  writeFileList(plotDir + "/PSWeights_latino_NLeptons_" + name + "_list_files.txt", files)


#
# main
#

parser = argparse.ArgumentParser(description="Check the normalization of PSWeight (ISR/FSR) on post-processed (latino) trees")
parser.add_argument("-d", "--directory",  required=True, help="folder with post-processed (latino) trees, e.g. /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9")
parser.add_argument("-s", "--samples",    nargs="+", default=[], help="latino sample names, as in nanoLatino_<sample>__part*.root (wildcards allowed), e.g. WWTo2L2Nu")
parser.add_argument("-a", "--all",        action="store_true", help="test all the samples in the folder (all the nanoLatino_<sample>__part*.root)")
parser.add_argument("-i", "--indices",    nargs="+", type=int, default=[0, 1, 2, 3], help="PSWeight indices to check")
parser.add_argument("-n", "--maxFiles",   type=int, default=-1, help="max number of files (parts) per sample (-1 = all)")
parser.add_argument("-r", "--redirector", default="root://eoscms.cern.ch/", help="xrootd redirector, if the folder is not visible locally")
parser.add_argument("-j", "--threads",    type=int, default=4, help="number of threads (0 = no multithreading)")
parser.add_argument("-o", "--output",     default="", help="output text file with the summary")
parser.add_argument("-p", "--plotDir",    default="plots", help="folder for the plots of the PSWeight distributions")
parser.add_argument("-b", "--binning",    nargs=3, type=float, default=[200, 0., 4.], help="binning of the PSWeight histograms: nbins min max")
parser.add_argument("-l", "--linear",     action="store_true", help="linear y axis in the plots (default: log)")
args = parser.parse_args()

if not args.all and len(args.samples) == 0:
  parser.error("give the samples with -s, or use -a to test all the samples in the folder")
if args.all and len(args.samples) > 0:
  print ("WARNING: -a given, -s ignored: all the samples in the folder are tested")

# no plots on screen, only saved as png and root
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

if args.threads > 0:
  ROOT.EnableImplicitMT(args.threads)

#
# list of samples to check: (label, name, campaign, files)
#
toCheck = []
directory = args.directory.rstrip("/")
# campaign: production folder, e.g. Summer20UL18_106x_nAODv9_Full2018v9
campaign = os.path.basename(os.path.dirname(directory))
patterns = ["*"] if args.all else args.samples
for sample in patterns:
  samples = getLatinoSamples(directory, sample, args.redirector, args.maxFiles)
  if len(samples) == 0:
    print ("No latino sample found for ", sample, " in ", directory)
  for name, files in sorted(samples.items()):
    # the same sample only once, also if matched by more than one -s
    if name in [n for l, n, c, fs in toCheck]:
      continue
    toCheck.append((directory + "/nanoLatino_" + name, name, campaign, files))

# list of the samples to test
totalFiles = sum([len(files) for label, name, campaign, files in toCheck])
print ("")
print ("Samples to test in ", directory, ": ", len(toCheck), ", files: ", totalFiles)
for label, name, campaign, files in toCheck:
  print ("   ", name, " (", len(files), " files)")

summary = []
analyzedFiles = 0
for label, name, campaign, files in toCheck:
  # progress, per sample: files of the samples already analyzed over all the files to analyze
  print ("")
  print (f"running on sample {name}, {100. * analyzedFiles / totalFiles:.1f} % of files analyzed")
  results = checkSample(label, name, campaign, files, args.indices, args.binning, args.plotDir, not args.linear)
  analyzedFiles += len(files)
  if results == None:
    continue
  for i, (R, err) in results.items():
    summary.append(f"{label}  {i}  {R:.6f}  {err:.6f}")

if len(toCheck) > 0:
  print ("")
  print (f"done, {100. * analyzedFiles / totalFiles:.1f} % of files analyzed")

if args.output != "":
  with open(args.output, "w") as fileOut:
    fileOut.write("# sample  index  R  error\n")
    for line in summary:
      fileOut.write(line + "\n")
  print ("")
  print ("Summary written in ", args.output)
