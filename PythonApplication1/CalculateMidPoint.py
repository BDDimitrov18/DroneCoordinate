from exif import Image
from pathlib import Path
import os
import wx
from wx.core import Size
from datetime import datetime
import math


a = 6378137
e = 0.0818191910428
e2 = 0.00669438


class EventLine:
    def __init__(self, line):
        self.line = line
        tokens = line.split()
        self.time = tokens[1];
        self.B = float(tokens[2]);
        self.L = float(tokens[3]);
        self.H = float(tokens[4]);

        self.N = a*((1-e2*(math.sin(math.radians(self.B))**2))**(-0.5)) # D2*((1-E3*((SIN(RADIANS(B2))^2)))^-(1/2))
        
        self.X = (self.N+self.H)*math.cos(math.radians(self.B))*math.cos(math.radians(self.L)) 
        
        self.Y = (self.N+self.H)*math.cos(math.radians(self.B))*math.sin(math.radians(self.L))
        
        self.Z = (self.N*(1-e2)+self.H)*math.sin(math.radians(self.B))


    def PrintObj(self):
        print(f"{self.time} {self.B} {self.L} {self.H}")

class SinglePair:
    def __init__(self, FirstEventLine,SecondEventLine):
        self.first = FirstEventLine;
        self.second = SecondEventLine



def calculateMidPointFunc(inputPath,outputPath,resultPathCalc, offset):
    EventLines = []
    SinglePoints = []

    br = 0
    with open(inputPath) as f:
        lines = f.readlines()
        for j in lines:
            if(br>24):
                if(j[0]!='%'):
                    EventLines.append(EventLine(j))
            br= br+1


    def deltaFunc(y1,y2):
        y1= float(y1)
        y2= float(y2)
        return (y1-y2)

    DoneFile = open(outputPath, 'w')
    ResultFileCalc = open(resultPathCalc, 'w')
    print(len(EventLines))
    i=0
    counter = 0
    differenceFloatSum=0
    h=0
    while i < len(EventLines)-1:
        h+=EventLines[i].H+EventLines[i+1].H
        datetimeObjF = datetime.strptime(EventLines[i].time, '%H:%M:%S.%f')
        datetimeObjS = datetime.strptime(EventLines[i+1].time, '%H:%M:%S.%f')
        difference  = datetimeObjS - datetimeObjF
        differenceStr = str(difference)
        splitedTime = differenceStr.split(':')
        differenceFloat = float(splitedTime[2])
        if(differenceFloat>=0.35 and differenceFloat<=0.65):
            DeltaX = deltaFunc(EventLines[i+1].X,EventLines[i].X)
            DeltaY = deltaFunc(EventLines[i+1].Y,EventLines[i].Y)
            DeltaZ = deltaFunc(EventLines[i+1].Z,EventLines[i].Z)
        
        
            EventLines[i+1].line = EventLines[i+1].line.replace("\n","")
            s = math.sqrt(pow(DeltaX,2) + pow(DeltaY,2) + pow(DeltaZ,2))
            if(differenceFloat >=0.35 and differenceFloat<=0.45):
              s1 = s/2 + offset # + offset
              differenceFloat /=2
          
            else:
              s1 = s/3 + offset # + offset
              differenceFloat /=3
              differenceFloat *=2
             
            Xmid = (DeltaX/s)*s1 + float(EventLines[i].X)
            Ymid = (DeltaY/s)*s1 + float(EventLines[i].Y)
            Zmid = (DeltaZ/s)*s1 + float(EventLines[i].Z)
       
            DoneFile.write(str(counter)+ " " + str(round(Xmid,3)) +  " " + str(round(Ymid,3)) + " " + str(round(Zmid,3))+"\n")
            counter+=1

            differenceFloatSum += differenceFloat

            i+=2

        else:
            SinglePoints.append(SinglePair(EventLines[i],EventLines[i+1]))
            i+=1

        differenceFloatAverage = differenceFloatSum/counter
        i=0
        counter =0
        while i < len(SinglePoints):
            DeltaX = deltaFunc(SinglePoints[i].second.X,SinglePoints[i].first.X)
            DeltaY = deltaFunc(SinglePoints[i].second.Y,SinglePoints[i].first.Y)
            DeltaZ = deltaFunc(SinglePoints[i].second.Z,SinglePoints[i].first.Z)

            s = math.sqrt(pow(DeltaX,2) + pow(DeltaY,2) + pow(DeltaZ,2))

            V=s/(SinglePoints[i].second.time-SinglePoints[i].first.time)

            s1 = s/(differenceFloatAverage*V)

            Xmid = (DeltaX/s)*s1 + float(EventLines[i].X)
            Ymid = (DeltaY/s)*s1 + float(EventLines[i].Y)
            Zmid = (DeltaZ/s)*s1 + float(EventLines[i].Z)

            ResultFileCalc.write(str(counter) + " " + str(round(Xmid,3)) +  " " + str(round(Ymid,3)) + " " + str(round(Zmid,3))+"\n")
            counter +=1
            i+=2


            




    h/=(len(EventLines)-1)
    DoneFile.write(str(h))
    DoneFile.close()

