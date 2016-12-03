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
"""   


from ROOT import *
import os
import datetime
import argparse

# Let's have an idea of how much does it take to run this s***t
print "We start now! ", datetime.datetime.now()
print

# Parse the input arguments  
parser = argparse.ArgumentParser()
parser.add_argument("rootName" , help="This is the name of the rootFile where your TTree leaves")
parser.add_argument("ttreeName", help="This is the path/name of your TTree")
parser.add_argument("leaf"     , metavar='N', type=str, nargs='+',
                    help="This is the name of the leaf you want to tabulate. Can be more than 1")
args = parser.parse_args()

# and make sure they are converted to strings  
rootName  = str(args.rootName)
ttreeName = str(args.ttreeName)
leaves = args.leaf


# Make sure the file exists
if not os.path.isfile(rootName):
   exit("Root File Not Found")
fileRoot    = TFile(rootName)
# Make sure the anatree exists
ttree   = fileRoot.Get(ttreeName)
if not ttree:
   exit("AnaTree Not Found")

# Let's give the outputfile a name that rembles the original root file and anatree
wordsInttreeName = ttreeName.split("/")
wordsfileRootName = rootName.split(".")
outPutFileName = wordsfileRootName[0]+wordsInttreeName[len(wordsInttreeName)-1]+"_tree.csv"
target = open(outPutFileName, 'w')

# Print out the header in the csv format, might be useful for R
header = ""
for leaf in leaves:
      header += (leaf+",")
header = header[:-1]
print "Your table will be in the format:"
print header
target.write(header)

### Bulk of the program ###
# leafValue is a dummy variable to store the leafValue in the loop
leafValue = 0
# Run on all the anatree events
for event in ttree :
   # outString is what we're going to write in the csv, one per event 
   outString = ""
   # Take each leaf in each event
   for leaf in leaves:
      # command to get the leaf
      pyCmd = 'leafValue = event.'+leaf
      # but make sure the leaf exists
      try:
         exec(pyCmd)
      except AttributeError: 
         exit("Leaf Not Found")
      # if the leaf is the last one in the sequence, add a return
      if (leaf==leaves[len(leaves)-1]):
         outString += str(leafValue)+"\n"
      # otherwise, add a comma
      else:
         outString += str(leafValue)+","
   # write your string to file
   target.write(outString)

print
print datetime.datetime.now(), ", and this is it!"
# Done

