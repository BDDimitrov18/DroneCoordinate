import math
import random
from pyproj import Proj, transform
from datetime import datetime, timedelta

# Define the projections
wgs84 = Proj(proj='latlong', datum='WGS84')
utm35n = Proj(proj='utm', zone=35, datum='WGS84')

# WGS84 ellipsoid parameters
a = 6378137
e = 0.0818191910428
e2 = 0.00669438

class EventLine:
    def __init__(self, line):
        self.line = line
        tokens = line.split()
        if len(tokens) == 4:
            self.X = float(tokens[1])
            self.Y = float(tokens[2])
            self.Z = float(tokens[3])
            # Convert UTM to geographic coordinates (latitude, longitude, height)
            self.B, self.L, self.H = transform(utm35n, wgs84, self.X, self.Y, self.Z)
            # Calculate NG, XG, YG, ZG
            self.NG = a * ((1 - e2 * (math.sin(math.radians(self.B))**2))**(-0.5))
            self.XG = (self.NG + self.H) * math.cos(math.radians(self.B)) * math.cos(math.radians(self.L))
            self.YG = (self.NG + self.H) * math.cos(math.radians(self.B)) * math.sin(math.radians(self.L))
            self.ZG = (self.NG * (1 - e2) + self.H) * math.sin(math.radians(self.B))
        else:
            self.X = None
            self.Y = None
            self.Z = None
            self.B = None
            self.L = None
            self.H = None
            self.NG = None
            self.XG = None
            self.YG = None
            self.ZG = None

    def is_valid(self):
        return self.X is not None and self.Y is not None and self.Z is not None

    def PrintObj(self):
        print(f"{self.B:.6f} {self.L:.6f} {self.H:.3f}")

def deltaFunc(y1, y2):
    y1 = float(y1)
    y2 = float(y2)
    return abs(y1 - y2)

def calcTimeForPoints(inputPath, outputPath, date, startHour):
    EventLines = []
    startHour = datetime.strptime(startHour, '%H:%M:%S')
    
    with open(inputPath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for j in lines:
            event = EventLine(j)
            if event.is_valid():
                EventLines.append(event)
                
    i = 0 
    while i < len(EventLines):
          
        
        
        if i == 0:
            EventLines[i].timePoint = startHour
        else:
            DeltaX = deltaFunc(EventLines[i-1].XG, EventLines[i].XG)
            DeltaY = deltaFunc(EventLines[i-1].YG, EventLines[i].YG)
            DeltaZ = deltaFunc(EventLines[i-1].ZG, EventLines[i].ZG) 
            s = math.sqrt(pow(DeltaX, 2) + pow(DeltaY, 2) + pow(DeltaZ, 2))

            elapsed_time_seconds = s * 0.1 + random.randint(1, 10)
            EventLines[i].timePoint = startHour + timedelta(seconds=elapsed_time_seconds)
            startHour = EventLines[i].timePoint
        
        i += 1

    with open(outputPath, 'w', encoding='utf-8') as f:
        # Write the HTML header
        f.write('<HTML xmlns:msxsl="urn:schemas-microsoft-com:xslt">\n')
        f.write('<TITLE>GNSS измервания</TITLE>\n')
        f.write('<H1>GNSS измервания</H1>\n')
        f.write('<H2>nov_ofis_vik_k</H2>\n')
        f.write('<BODY>\n')
        f.write('<TABLE BORDER="5" width="150%" cellpadding="1" rules="cols">\n')
        f.write('<TR>\n')
        f.write('<TH width="5%" align="center">Номер точка</TH>\n')
        f.write('<TH width="5%" align="center">Север (X)m</TH>\n')
        f.write('<TH width="5%" align="center">Изток (Y)m</TH>\n')
        f.write('<TH width="5%" align="center">Кота (H)m</TH>\n')
        f.write('<TH width="5%" align="center">X (ECEF)</TH>\n')
        f.write('<TH width="5%" align="center">Y (ECEF)</TH>\n')
        f.write('<TH width="5%" align="center">Z (ECEF)</TH>\n')
        f.write('<TH width="5%" align="center">Дата</TH>\n')
        f.write('<TH width="5%" align="center">Час</TH>\n')
        f.write('<TH width="5%" align="center">Епохи</TH>\n')
        f.write('<TH width="5%" align="center">Хор.точ.(m)</TH>\n')
        f.write('<TH width="5%" align="center">Верт.точ.(m)</TH>\n')
        f.write('<TH width="5%" align="center">Тип Решение</TH>\n')
        f.write('</TR>\n')
        f.write('</TABLE>\n')

        for i, event in enumerate(EventLines):
            hor_toc = str(0.01) + str(round(random.random() * 10))
            vert_toc = str(0.01) + str(round(random.random() * 10))
            f.write('<TABLE BORDER="1" width="150%" cellpadding="1" rules="cols">\n')
            f.write('<TR>\n')
            f.write(f'<TD width="5%" align="center">{i+1}</TD>\n')
            f.write(f'<TD width="5%" align="center">{event.X:.3f}</TD>\n')
            f.write(f'<TD width="5%" align="center">{event.Y:.3f}</TD>\n')
            f.write(f'<TD width="5%" align="center">{event.Z:.3f}</TD>\n')
            f.write(f'<TD width="5%" align="center">{event.XG:.3f}</TD>\n')
            f.write(f'<TD width="5%" align="center">{event.YG:.3f}</TD>\n')
            f.write(f'<TD width="5%" align="center">{event.ZG:.3f}</TD>\n')
            f.write(f'<TD width="5%" align="center">{date}</TD>\n')
            f.write(f'<TD width="5%" align="center">{event.timePoint.strftime("%H:%M:%S")}</TD>\n')
            f.write(f'<TD width="5%" align="center">3</TD>\n')
            f.write(f'<TD width="5%" align="center">{hor_toc}</TD>\n')
            f.write(f'<TD width="5%" align="center">{vert_toc}</TD>\n')
            f.write(f'<TD width="5%" align="center">NetworkRTK</TD>\n')
            f.write('</TR>\n')
            f.write('</TABLE>\n')

        # Close the HTML tags
        f.write('</BODY>\n')
        f.write('</HTML>\n')

# Example usage
inputPath = r'C:\Users\dell\Downloads\лесопарк-снимка_2005_utm_N35_balt.txt'  # replace with your actual input file path
outputPath = r'C:\Users\dell\Downloads\result.htm'  # replace with your desired output file path
date = '21.02.2024'  # example date
startHour = '15:00:00'  # example start hour

calcTimeForPoints(inputPath, outputPath, date, startHour)
