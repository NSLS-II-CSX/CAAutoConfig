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

def applyRegexToList(list, regex):
  """Apply a list of regex to list and return result"""
  print type(regex), type(regex) == list
  if type(regex) != type(list):
    regex = [regex]

  print regex

  regexList = [re.compile(r) for r in regex]

  for r in regexList:
    list = [l for l in list if r.match(l)]

  return list
   

if __name__ == "__main__":
  list = getCfPVlist('/cf-update', 'xf23id*.dbl')
  print applyRegexToList(list, ['^XF:23ID(A|1|2)-VA', '.*(?<!_)$'])

