import glob
import os, fnmatch
import re

def findFiles(rootPath, pattern):
  """Walk through rootPath and return files matching pattern"""
  filenames = []
  for root,dirs,files in os.walk(rootPath):
    for f in files:
      if fnmatch.fnmatch(f,pattern):
        filenames.append(os.path.join(root, f))
  return filenames

def getCfPVlist(rootPath, pattern):
  """Get list of PVs from CF path"""
  filenames = findFiles(rootPath, pattern)
  pvlist = []
  for fn in filenames:
    pvlist += [line.strip() for line in open(fn)]
  
  return pvlist

def applyRegexToList(list, regex, separator=' ', expandList = None):
  """Apply a list of regex to list and return result"""
  if type(regex) != type(list):
    regex = [regex]

  regexList = [re.compile(r) for r in regex]

  for r in regexList:
    list = [l for l in list if r.match(l)]

  list = [l.split(separator) for l in list]
  list = [i[0] for i in list]
  
  if expandList:
    expandRegexList = [re.compile(r) for r in expandList[0]]
    for r,postfix in zip(expandRegexList, expandList[1]):
      expandMatches = [l for l in list if r.match(l)]
      for e in expandMatches:
        list = list + [(e + p) for p in postfix]
  return list

if __name__ == "__main__":
  list = getCfPVlist('/cf-update', 'xf23ida-ioc1.mc05.dbl')
  for a in applyRegexToList(list, ['^XF:23IDA-BI:1', '.*(?<!_)$'], expandList = [['.*Mtr$'],[['.RBV','.OFF']]]):
    print a

