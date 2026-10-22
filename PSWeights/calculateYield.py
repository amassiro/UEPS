#!/usr/bin/env python3

#
# Expected yield of each sample in a folder of post-processed (latino) trees:
#
#   N = lumi * sum( XSWeight ),   uncertainty (MC statistics): lumi * sqrt( sum( XSWeight^2 ) )
#
# XSWeight = baseW * genWeight, with baseW = xsec [pb] * 1000 / sum( genWeight ) of the full generated sample,
# so sum( XSWeight ) is the number of expected events for 1/fb, i.e. the cross section in fb, inside the skim.
# NB: sum( genWeight ) alone is NOT a yield: genWeight has an arbitrary normalization.
#
# Each sample is done independently, and the results file is updated after each sample.
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


def getLatinoSamples(directory, redirector, maxFiles):
  # all the nanoLatino_<sample>__part<N>.root in the folder, grouped by sample
  samples = {}
  for fileName in listDirectory(directory, redirector):
    m = re.match(r"nanoLatino_(.+)__part(\d+)\.root$", os.path.basename(fileName))
    if m:
      samples.setdefault(m.group(1), []).append((int(m.group(2)), fileName))
  for name in samples:
    files = [f for part, f in sorted(samples[name])]
    if maxFiles > 0:
      files = files[:maxFiles]
    samples[name] = files
  return samples


def matchAny(name, patterns):
  return any([fnmatch.fnmatch(name, pattern) for pattern in patterns])


# ---- the yield of one sample ----

def calculateYield(name, files, weight, lumi):
  print ("")
  print ("---- ", name)
  print ("   files: ", len(files))
  for fileName in files:
    print ("      ", fileName)

  try:
    df = ROOT.RDataFrame("Events", files)
    df = df.Define("w_yield", f"double({weight})")
    df = df.Define("w2_yield", "w_yield * w_yield")
    n   = df.Count()
    sw  = df.Sum("w_yield")
    sw2 = df.Sum("w2_yield")
    ROOT.RDF.RunGraphs([n, sw, sw2])
  except Exception as e:
    print ("   ERROR: ", e)
    return None

  nEvents = n.GetValue()
  yieldValue = lumi * sw.GetValue()
  yieldError = lumi * math.sqrt(sw2.GetValue())
  print (f"   events = {nEvents}")
  print (f"   yield = {yieldValue:.6g} +/- {yieldError:.6g}   (weight: {weight}, lumi = {lumi} /fb)")
  return nEvents, yieldValue, yieldError


#
# main
#

parser = argparse.ArgumentParser(description="Expected yield of each sample in a folder of post-processed (latino) trees")
parser.add_argument("-d", "--directory",  required=True, help="folder with post-processed (latino) trees, e.g. /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9")
parser.add_argument("-s", "--samples",    nargs="+", default=["*"], help="samples to analyze, wildcards allowed, e.g. \"*CP5Up*\" \"*CP5Down*\" (default: all)")
parser.add_argument("-x", "--exclude",    nargs="+", default=[], help="samples NOT to analyze, wildcards allowed, e.g. \"*_PSWeights*\"")
parser.add_argument("-w", "--weight",     default="XSWeight", help="weight of each event (default: XSWeight)")
parser.add_argument("-L", "--lumi",       type=float, default=1., help="luminosity in 1/fb (default: 1, i.e. the yield is the cross section in fb)")
parser.add_argument("-n", "--maxFiles",   type=int, default=-1, help="max number of files (parts) per sample (-1 = all). NB: the yield is then only of these files")
parser.add_argument("-r", "--redirector", default="root://eoscms.cern.ch/", help="xrootd redirector, if the folder is not visible locally")
parser.add_argument("-j", "--threads",    type=int, default=4, help="number of threads (0 = no multithreading)")
parser.add_argument("-o", "--output",     default="results_yield.txt", help="output text file: name, number of files, events, yield, uncertainty")
args = parser.parse_args()

if args.threads > 0:
  ROOT.EnableImplicitMT(args.threads)

directory = args.directory.rstrip("/")

#
# list of samples: those matching -s, but not -x
#
allSamples = getLatinoSamples(directory, args.redirector, args.maxFiles)
toAnalyze = []
for name in sorted(allSamples.keys()):
  if matchAny(name, args.samples) and not matchAny(name, args.exclude):
    toAnalyze.append((name, allSamples[name]))

totalFiles = sum([len(files) for name, files in toAnalyze])
print ("")
print ("Samples in ", directory, ": ", len(allSamples), ", to analyze: ", len(toAnalyze), ", files: ", totalFiles)
for name, files in toAnalyze:
  print ("   ", name, " (", len(files), " files)")
if len(toAnalyze) == 0:
  print ("Nothing to analyze")

#
# results: written again after each sample, not to lose them if the job stops
#
resultLines = []

def writeResults():
  with open(args.output, "w") as fileOut:
    fileOut.write(f"# folder: {directory}\n")
    fileOut.write(f"# weight: {args.weight}, lumi = {args.lumi} /fb\n")
    fileOut.write("# name  nFiles  nEvents  yield  uncertainty\n")
    for line in resultLines:
      fileOut.write(line + "\n")

analyzedFiles = 0
for name, files in toAnalyze:
  # progress, per sample: files of the samples already analyzed over all the files to analyze
  print ("")
  print (f"running on sample {name}, {100. * analyzedFiles / totalFiles:.1f} % of files analyzed")
  result = calculateYield(name, files, args.weight, args.lumi)
  analyzedFiles += len(files)
  if result == None:
    resultLines.append(f"{name}  {len(files)}  nan  nan  nan")
  else:
    nEvents, yieldValue, yieldError = result
    resultLines.append(f"{name}  {len(files)}  {nEvents}  {yieldValue:.6g}  {yieldError:.6g}")
  writeResults()

if len(toAnalyze) > 0:
  print ("")
  print (f"done, {100. * analyzedFiles / totalFiles:.1f} % of files analyzed")
  print ("Results written in ", args.output)
