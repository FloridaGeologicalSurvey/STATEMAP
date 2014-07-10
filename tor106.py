# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 11:47:09 2014

@author: Bassett_S
"""


import arcpy, os
workspace = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb'
outworkspace = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\Units'
ofms100 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\Wells_OFMS100'
ofms94 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\Wells_OFMS94'
ofms105 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\DB_Wells'
ofms106 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\SA_Wells'


with arcpy.da.SearchCursor(ofms106, "*") as cursor:
	t106 = [row for row in cursor]

with arcpy.da.SearchCursor(ofms105, "*") as cursor:
	t105 = [row for row in cursor]
	
with arcpy.da.SearchCursor(ofms100, "*") as cursor:
	t100 = [row for row in cursor]

with arcpy.da.SearchCursor(ofms94, "*") as cursor:
	t94 = [row for row in cursor]

#field names	
f106 = [i.name for i in arcpy.ListFields(ofms106)]
f105 = [i.name for i in arcpy.ListFields(ofms105)]
f100 = [i.name for i in arcpy.ListFields(ofms100)]
f94 = [i.name for i in arcpy.ListFields(ofms94)]


#wnumbers
wnum94 = [i[2] for i in t94]
wnum100 = [i[2] for i in t100]
wnum106 = [i[2] for i in t106]
wnum105 = [i[2] for i in t105]


#106 To columns= [1, 2, 49]
masterWNum = []
to106 = []
for i in t106:
    thisLine = []
    if i[49] != None:
        thisLine = [i[1],int(i[2]),i[49], 106]
        to106.append(thisLine)
        masterWNum.append(int(i[2]))


#105 To columns= [1, 2, 14]
to105 = []
for i in t105:
    thisLine = []
    if i[14] != None and int(i[2]) not in masterWNum:
        thisLine = [i[1],int(i[2]),i[14], 105]
        to105.append(thisLine)
        masterWNum.append(int(i[2]))


#100 To columns = [1, 2, 55]
to100 = []
for i in t100:
    thisLine = []
    if i[55] != None and int(i[2]) not in masterWNum and i[55] != 999:
        thisLine = [i[1],int(i[2]),i[55], 100]
        to100.append(thisLine)
        masterWNum.append(int(i[2]))


#94 To columns = [1, 2, 31]
to94 = []
for i in t94:
    thisLine = []
    if len(i[31].strip()) != 0 and int(i[2]) not in masterWNum:
        thisLine = [i[1],int(i[2]),float(i[31]), 94]
        to94.append(thisLine)
        masterWNum.append(int(i[2]))

toPath = os.path.join(outworkspace, "To")

arcpy.CreateFeatureclass_management(outworkspace, "To", "POINT")
arcpy.AddField_management(toPath, "wnumber", "LONG")
arcpy.AddField_management(toPath, "unit_top", "DOUBLE", 4, 1)
arcpy.AddField_management(toPath, "ofms_num", "LONG")

cursor = arcpy.da.InsertCursor(toPath, ("SHAPE@XY", "wnumber", "unit_top","ofms_num"))

for i in to106:
    cursor.insertRow(i)
del cursor

cursor = arcpy.da.InsertCursor(toPath, ("SHAPE@XY", "wnumber", "unit_top","ofms_num"))
for i in to105:
    cursor.insertRow(i)
del cursor

cursor = arcpy.da.InsertCursor(toPath, ("SHAPE@XY", "wnumber", "unit_top","ofms_num"))   
for i in to100:
    cursor.insertRow(i)
del cursor

cursor = arcpy.da.InsertCursor(toPath, ("SHAPE@XY", "wnumber", "unit_top","ofms_num"))    
for i in to94:
    cursor.insertRow(i)

del cursor

    
