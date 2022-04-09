from exif import Image
from pathlib import Path
import os
import wx
from wx.core import Size
from datetime import datetime
import math
import MatchFiles
import CalculateMidPoint
import ExtractExif
import visualInterface
import UImiddling
import UIMatching



print('Choose an option: ')
print('1. Calculate middle point')
print('2. match')

option = input("Enter the option number(From 1 to 2):")
option = int(option)
if(option == 1):
    UImiddling.StartMIdUi()
if(option == 2):
    UIMatching.matchUi()
    


#h = CalculateMidPoint.calculateMidPointFunc()
#print(h)
#MatchFiles.match(h)

#C:\tate\20.3.22\2021-11-18-07-33-49_events.txt
