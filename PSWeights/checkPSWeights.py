#!/usr/bin/env python3

#
# Check if the parton shower weights (PSWeight) change the normalization of a nanoAOD sample:
#
#   R[i] = sum( genWeight * PSWeight[i] ) / sum( genWeight )
#
# on the full sample, no selections.
# Input: CMS dataset names, as in DAS (wildcards allowed)
#

import argparse
import subprocess
import math
import os
import re
import ROOT


# ---- DAS ----

def dasQuery(query):
  result = subprocess.run(["dasgoclient", "-query=" + query], capture_output=True, text=True)
  if result.returncode != 0:
    print ("ERROR: dasgoclient failed for query: ", query)
    print (result.stderr)
    return []
  return [line.strip() for line in result.stdout.split("\n") if line.strip() != ""]


def getDatasets(sample):
  # wildcards: get the list of datasets from DAS
  if "*" in sample:
    return dasQuery("dataset dataset=" + sample)
  return [sample]


def getFiles(dataset, redirector, maxFiles):
  files = dasQuery("file dataset=" + dataset)
  if maxFiles > 0:
    files = files[:maxFiles]
  return [redirector + f for f in files]


# ---- PSWeight description, from the first file ----

def getPSWeightInfo(fileName):
  f = ROOT.TFile.Open(fileName)
  if not f or f.IsZombie():
    return None, None
  events = f.Get("Events")
  branch = events.GetBranch("PSWeight")
  if not branch:
    f.Close()
    return None, None
  title = branch.GetTitle()
  # Runs tree: also PSSumw, if available in this nanoAOD version
  # (assumed to be normalized as LHEScaleSumw, i.e. divided by genEventSumw: to be checked)
  runs = f.Get("Runs")
  hasPSSumw = bool(runs.GetBranch("PSSumw"))
  f.Close()
  return title, hasPSSumw


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

def checkDataset(dataset, redirector, maxFiles, indices, binning, plotDir, logy):
  print ("")
  print ("---- ", dataset)

  files = getFiles(dataset, redirector, maxFiles)
  if len(files) == 0:
    print ("   no files found")
    return None
  print ("   files: ", len(files))
  for fileName in files:
    print ("      ", fileName)

  title, hasPSSumw = getPSWeightInfo(files[0])
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
  dfRuns = ROOT.RDataFrame("Runs", files)
  sumRuns = dfRuns.Sum("genEventSumw")
  if hasPSSumw:
    for i in indices:
      dfRuns = dfRuns.Define(f"pssumw{i}", f"nPSSumw > {i} ? PSSumw[{i}] * genEventSumw : genEventSumw")
      sums[f"runsp{i}"] = dfRuns.Sum(f"pssumw{i}")

  # run the event loop (once, all the booked results together)
  ROOT.RDF.RunGraphs([v for v in sums.values()] + [h for h in histos.values()] + [sumRuns])

  sw  = sums["sw"].GetValue()
  sw2 = sums["sw2"].GetValue()

  print ("   events = ", sums["n"].GetValue())
  print ("   sum genWeight (Events) = ", sw)
  print ("   sum genEventSumw (Runs) = ", sumRuns.GetValue())

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

  drawPSWeights(dataset, files, histos, results, meanings, plotDir, logy)

  return results


# ---- plot of the PSWeight distributions ----

def writeFileList(fileName, files):
  with open(fileName, "w") as fileOut:
    for f in files:
      fileOut.write(f + "\n")
  print ("   list of files written in ", fileName)

usedNames = []

def plotName(dataset):
  # first part of the DAS name, e.g. WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8
  # if already used (same sample, different campaign), add the campaign, e.g. __Run3Summer22NanoAODv12
  parts = dataset.strip("/").split("/")
  name = parts[0]
  if name in usedNames and len(parts) > 1:
    name = name + "__" + parts[1].split("-")[0]
  usedNames.append(name)
  return name

def drawPSWeights(dataset, files, histos, results, meanings, plotDir, logy):
  colors = [ROOT.kGreen+3, ROOT.kRed+1, ROOT.kBlue+1, ROOT.kCyan-4, ROOT.kMagenta+1, ROOT.kOrange+7, ROOT.kGray+2, ROOT.kViolet+1]
  name = plotName(dataset)

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
    h.SetTitle(dataset.split("/")[1])
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
  cc.SaveAs(plotDir + "/PSWeights_" + name + ".png")
  cc.SaveAs(plotDir + "/PSWeights_" + name + ".root")

  # list of the files used
  writeFileList(plotDir + "/PSWeights_" + name + "_list_files.txt", files)


#
# main
#

parser = argparse.ArgumentParser(description="Check the normalization of PSWeight (ISR/FSR) on nanoAOD samples")
parser.add_argument("-s", "--samples",    nargs="+", required=True, help="dataset names, as in DAS (wildcards allowed), e.g. /WW_TuneCP5_13p6TeV_pythia8/Run3Summer22NanoAODv12-*/NANOAODSIM")
parser.add_argument("-i", "--indices",    nargs="+", type=int, default=[0, 1, 2, 3], help="PSWeight indices to check")
parser.add_argument("-n", "--maxFiles",   type=int, default=-1, help="max number of files per dataset (-1 = all)")
parser.add_argument("-r", "--redirector", default="root://cms-xrd-global.cern.ch/", help="xrootd redirector")
parser.add_argument("-j", "--threads",    type=int, default=4, help="number of threads (0 = no multithreading)")
parser.add_argument("-o", "--output",     default="", help="output text file with the summary")
parser.add_argument("-p", "--plotDir",    default="plots", help="folder for the plots of the PSWeight distributions")
parser.add_argument("-b", "--binning",    nargs=3, type=float, default=[200, 0., 4.], help="binning of the PSWeight histograms: nbins min max")
parser.add_argument("-l", "--linear",     action="store_true", help="linear y axis in the plots (default: log)")
args = parser.parse_args()

# no plots on screen, only saved as png and root
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

if args.threads > 0:
  ROOT.EnableImplicitMT(args.threads)

summary = []
for sample in args.samples:
  datasets = getDatasets(sample)
  if len(datasets) == 0:
    print ("No dataset found for ", sample)
  for dataset in datasets:
    results = checkDataset(dataset, args.redirector, args.maxFiles, args.indices, args.binning, args.plotDir, not args.linear)
    if results == None:
      continue
    for i, (R, err) in results.items():
      summary.append(f"{dataset}  {i}  {R:.6f}  {err:.6f}")

if args.output != "":
  with open(args.output, "w") as fileOut:
    fileOut.write("# dataset  index  R  error\n")
    for line in summary:
      fileOut.write(line + "\n")
  print ("")
  print ("Summary written in ", args.output)
