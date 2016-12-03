#! /usr/bin/env python
# Copyright (C) 2016-2016 Elena Gramellini <elena.gramellini@yale.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You can read copy of the GNU General Public License here:
# <http://www.gnu.org/licenses/>.

"""@package docstring
Scope of this python script: convert ROOT TTree leaves to csv
Author: Elena Gramellini
Creation Date: 2016-12-03 
Version 0 
-----------------------------------------------------------------------

Input: name of the root file, name of the ttree, name of the leaves
Output: a csv file with tabulated values of the leaves
TO DO:
[   ] get input attributes
"""   


from ROOT import *
import os
import datetime
import argparse

print datetime.datetime.now()
######################## This is temporary ###############################
rootName  = "anaTree_postMassFilter.root"
ttreeName = "anatree/anatree"
leaves = ["cTOF[0]","wcPx[0]","wcPy[0]","wcPz[0]"]
######################## This is temporary ###############################

  
#parser = argparse.ArgumentParser()
#parser.add_argument("rootName" , help="This is the name of the rootFile where your TTree leaves")
#parser.add_argument("ttreeName", help="This is the path/name of your TTree")
#parser.add_argument("leaf"     , help="This is the name of the leaf you want to tabulate. Can be more than 1")
#args = parser.parse_args()
  
#rootName  = str(args.rootName)
#ttreeName = str(args.ttreeName)
#leaves = [str(args.leaf)]

#print rootName, ttreeName, leaves[0]



if not os.path.isfile(rootName):
   exit("Root File Not Found")

fileRoot    = TFile(rootName)
ttree   = fileRoot.Get(ttreeName)
if not ttree:
   exit("AnaTree Not Found")

wordsInttreeName = ttreeName.split("/")
wordsfileRootName = rootName.split(".")
outPutFileName = wordsfileRootName[0]+wordsInttreeName[len(wordsInttreeName)-1]+"_tree.csv"

target = open(outPutFileName, 'w')

leafValue = 0
for event in ttree :
   outString = ""
   for leaf in leaves:
      pyCmd = 'leafValue = event.'+leaf
      try:
         exec(pyCmd)
      except AttributeError: 
         exit("Leaf Not Found")
      if (leaf==leaves[len(leaves)-1]):
         outString += str(leafValue)+"\n"
      else:
         outString += str(leafValue)+","
   target.write(outString)



print datetime.datetime.now()

