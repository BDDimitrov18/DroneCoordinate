
from exif import Image
from pathlib import Path
import os
import wx
from wx.core import Size
from datetime import datetime
import math
def extract():
    # This is my path
    pathf= "E:/Проба/"
 
    # to store files in a list
    filepaths = []

    textfile= open("E:/Проба/testfile.txt","w")

    # dirs=directories

    for (root, dirs, file) in os.walk(pathf):
        for f in file:
            if '.png' or '.jpg' in f:
                filepaths.append(pathf + f)


    for path in filepaths:
        with open(path, "rb") as src:
         img = Image(src)
         if img.has_exif:
            try: 
               print(f"Image {src.name}: {img.gps_longitude} , {img.gps_latitude} , ({img.gps_altitude}) , ({img.datetime_original})\n")
               textfile.write(f"Image {src.name}: {img.gps_longitude} , {img.gps_latitude} , ({img.gps_altitude}) , ({img.datetime_original})\n")
            except AttributeError:
                print("No Coordinates")
         else:
            info = "does not contain any EXIF information"
        #"E:/testExif/DJI_0050.JPG"
    textfile.close()
    #coord, time
