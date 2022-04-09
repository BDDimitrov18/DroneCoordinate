#math.sin(math.radians(30))

from exif import Image
from pathlib import Path
import os
import wx
from wx.core import Size
from datetime import datetime
import math
"""
class MatchedFileClass():
      def __init__(self):
          self.B=.0
          self.L=.0
          self.H=.0
          self.name=""
          self.s=.0
      def printCoords(self):
            print(self.name + " " + str(self.B)+ " " + str(self.L) + " " +str(self.H) + " " + str(self.s))
      def writeOnFile(self):
          return(self.name + " " + str(self.B)+ " " + str(self.L) + " " +str(self.H) + " " + str(self.s))
"""

a = 6378137
e = 0.0818191910428
e2 = 0.00669438




class DoneFileReadClass():
      def __init__(self,line):

           parts = line.split()
           self.X = float(parts[1])
           self.Y = float(parts[2])
           self.Z = float(parts[3])

          
      

class lowPrecsCoords():
    def __init__(self, line,h):
        parts = line.split()
        self.name = parts[0]
        self.B = float(parts[1])
        self.L = float(parts[2])
        self.H = float(h)

        N = a*((1-e2*(math.sin(math.radians(self.B))**2))**-0.5)
        
        self.X = (N+self.H)*math.cos(math.radians(self.B))*math.cos(math.radians(self.L)) 
        
        self.Y = (N+self.H)*math.cos(math.radians(self.B))*math.sin(math.radians(self.L))
        
        self.Z = (N*(1-e2)+self.H)*math.sin(math.radians(self.B))
        
        self.H = float(parts[3])


    def printCoords(self):
        print(self.name + " " + str(self.L) + " " + str(self.B) + " " + str(self.H))


        
coords = []
coordsDone = []
matchedCoords = []

def match(mid,low,result):
    matchedFile = open(result, "w")
    h=.0
    with open(mid) as f:
        lines = f.readlines()
        for j in lines:
            arr = j.split()
            if(len(arr)>2):
                coordsDone.append(DoneFileReadClass(j))
            else:
                print(j)
                h=float(j)
    br=0
    with open(low) as f:
        lines = f.readlines()
        for j in lines:
            if(len(j.split())>1):
                if(j[0]!='%'):
                    coords.append(lowPrecsCoords(j,h))
            br = br+1

    def findSmallestS(line , fileToMatch):
        s = math.sqrt((line.X-fileToMatch[0].X)**2 + (line.Y-fileToMatch[0].Y)**2 +(line.Z-fileToMatch[0].Z)**2)
        match = fileToMatch[0]
        for i in fileToMatch:
          temp = math.sqrt((line.X-i.X)**2 + (line.Y-i.Y)**2 +(line.Z-i.Z)**2)
          if(temp<s):
              s=temp
              match = i
    
    
   
        matchedFile.write(str(match.name)+" " + str(line.X) + " " + str(line.Y) + " " + str(line.Z) + " " + str(s) + "\n")
    

    for i in coordsDone:
        findSmallestS(i,coords)