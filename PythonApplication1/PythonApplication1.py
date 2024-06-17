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
import CalcTimeForPoint
import HTMCalcTimeUI




print('Choose an option: ')
print('1. Calculate middle point')
print('2. match')
print('3. HTM FILE FORMAT OPERATION')

option = input("Enter the option number(From 1 to 3):")
option = int(option)
if(option == 1):
    UImiddling.StartMIdUi()
if(option == 2):
    UIMatching.matchUi()
if(option == 3):
    HTMCalcTimeUI.runUi()

