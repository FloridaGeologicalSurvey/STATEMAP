# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 15:35:27 2014

@author: Bassett_s

Scripts must be run in ArcCatalog Python interpreter, not Spyder IDE

"""
import arcpy

path = r'C:\GISData\Sinkhole Project\CleanOFMS.gdb\DirtyWells\OFMS92_Wells'
writePath = r'C:\GISData\Sinkhole Project\CleanOFMS.gdb\CleanWells'

fields = arcpy.ListFields(path)
fname = [field.name for field in fields]
ftype = [field.type for field in fields]

with arcpy.da.SearchCursor(path, '*') as cursor:
    rows = [row for row in cursor]

with arcpy.da.SearchCursor(path, 'SHAPE@XY') as cursor:
    xy = [row for row in cursor]
ofms92units = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

unitDict = {}
for i in ofms92units:
    unitDict[i] = fname[i]


    
    
ofms92surffm = 27





