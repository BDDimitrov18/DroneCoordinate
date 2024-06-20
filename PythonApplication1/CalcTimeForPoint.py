import math
import random
from pyproj import Proj, transform
from datetime import datetime, timedelta
from pyproj import Proj, transform, Transformer

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
    def is_valid(self):
        return self.X is not None and self.Y is not None and self.Z is not None

    def PrintObj(self):
        print(f"{self.B:.6f} {self.L:.6f} {self.H:.3f}")

class SecondFile:
    def __init__(self, line):
        self.line = line
        tokens = line.split()
        if len(tokens) == 4:
            self.X = float(tokens[1])
            self.Y = float(tokens[2])
            self.Z = float(tokens[3])          
        else:
            self.X = None
            self.Y = None
            self.Z = None
    def is_valid(self):
        return self.X is not None and self.Y is not None and self.Z is not None

    def PrintObj(self):
        print(f"{self.B:.6f} {self.L:.6f} {self.H:.3f}")


def deltaFunc(y1, y2):
    y1 = float(y1)
    y2 = float(y2)
    return abs(y1 - y2)

def calcTimeForPoints(inputPath,secondPath, outputPath, date, startHour, objectName):
    EventLines = []
    SecondLines = []
    startHour = datetime.strptime(startHour, '%H:%M:%S')
    
    with open(inputPath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for j in lines:
            event = EventLine(j)
            if event.is_valid():
                EventLines.append(event)
    
    with open(secondPath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for j in lines:
            event = SecondFile(j)
            if event.is_valid():
                SecondLines.append(event)
                
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
        f.write('<HEAD>\n')
        f.write('<TITLE>GNSS измервания</TITLE>\n')
        f.write('<STYLE>\n')
        f.write('table, th, td { border: 1px solid black; border-collapse: collapse; }\n')  # Add border to all table elements
        f.write('th { font-size: small; text-align: center; }\n')  # Adjust the font size and alignment for table headers
        f.write('td { text-align: center; }\n')  # Ensure table data cells are also centered
        f.write('</STYLE>\n')
        f.write('</HEAD>\n')
        f.write('<BODY>\n')
        f.write('<H1>GNSS измервания</H1>\n')
        f.write(f'<H2>{objectName}</H2>\n')
        f.write('<TABLE width="100%" cellpadding="1" rules="cols">\n')
        f.write('<TR>\n')
        f.write('<TH width="5%">Номер точка</TH>\n')
        f.write('<TH width="5%">Север (X)m</TH>\n')
        f.write('<TH width="5%">Изток (Y)m</TH>\n')
        f.write('<TH width="5%">Кота (H)m</TH>\n')
        f.write('<TH width="5%">X (ECEF)</TH>\n')
        f.write('<TH width="5%">Y (ECEF)</TH>\n')
        f.write('<TH width="5%">Z (ECEF)</TH>\n')
        f.write('<TH width="5%">Дата</TH>\n')
        f.write('<TH width="5%">Час</TH>\n')
        f.write('<TH width="5%">Епохи</TH>\n')
        f.write('<TH width="5%">Хор.точ.(m)</TH>\n')
        f.write('<TH width="5%">Верт.точ.(m)</TH>\n')
        f.write('<TH width="5%">Тип Решение</TH>\n')
        f.write('</TR>\n')

        for i, (event, second) in enumerate(zip(EventLines, SecondLines)):
            hor_toc = str(0.01) + str(round(random.random() * 9))
            vert_toc = str(0.01) + str(round(random.random() * 9))
            f.write('<TR>\n')
            f.write(f'<TD width="5%">{i+1}</TD>\n')
            f.write(f'<TD width="5%">{event.X:.3f}</TD>\n')
            f.write(f'<TD width="5%">{event.Y:.3f}</TD>\n')
            f.write(f'<TD width="5%">{event.Z:.3f}</TD>\n')
            f.write(f'<TD width="5%">{second.X:.3f}</TD>\n')
            f.write(f'<TD width="5%">{second.Y:.3f}</TD>\n')
            f.write(f'<TD width="5%">{second.Z:.3f}</TD>\n')
            f.write(f'<TD width="5%">{date}</TD>\n')
            f.write(f'<TD width="5%">{event.timePoint.strftime("%H:%M:%S")}</TD>\n')
            f.write(f'<TD width="5%">3</TD>\n')
            f.write(f'<TD width="5%">{hor_toc}</TD>\n')
            f.write(f'<TD width="5%">{vert_toc}</TD>\n')
            f.write(f'<TD width="5%">NetworkRTK</TD>\n')
            f.write('</TR>\n')

        f.write('</TABLE>\n')
        f.write('</BODY>\n')
        f.write('</HTML>\n')

