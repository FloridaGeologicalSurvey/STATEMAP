# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 13:21:19 2014

@author: Bassett_S
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 13:17:21 2014

@author: Bassett_S
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 13:02:54 2014

@author: Bassett_S
"""


import arcpy, os

workspace = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb'
outworkspace = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\Units'
ofms106 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\SA_Wells'
ofms105 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\DB_Wells'


unitName = "Qa"
unitColumn = {
    '106': 16,
    '105': 9,
    }
    

######## FUNCTIONS #################################

def printFields(fnames, ftypes):
    for v, (i, j) in enumerate(zip(fnames, ftypes)):
        print v, i, j

###################################################


with arcpy.da.SearchCursor(ofms106, "*") as cursor:
	t106 = [row for row in cursor]

with arcpy.da.SearchCursor(ofms105, "*") as cursor:
	t105 = [row for row in cursor]


 
#field names	
f106 = [i.name for i in arcpy.ListFields(ofms106)]
f105 = [i.name for i in arcpy.ListFields(ofms105)]


#field types
ftype106 = [i.type for i in arcpy.ListFields(ofms106)]
ftype105 = [i.type for i in arcpy.ListFields(ofms105)]



#for v, (i, j) in enumerate(zip(f101, ftype101)):
#    print v, i, j
    
#wnumbers
#wnum94 = [i[2] for i in t94]
#wnum100 = [i[2] for i in t100]
#wnum106 = [i[2] for i in t106]
#wnum105 = [i[2] for i in t105]


masterWNum = []
toMaster = []



columns = {
    'shape' : 1, 
    'wnumber' : 2,
    'surf' : 10, 
    'elev' : 3, 
    'unit' : unitColumn['106'] 
    }
for i in t106:
    thisLine = []
    if i[columns['unit']] != None:
        shape = i[columns['shape']]
        wnumber = i[columns['wnumber']]
        surf_fm = i[columns['surf']]
        elev = i[columns['elev']]
        to_top = i[columns['unit']]
        thisLine = [shape, wnumber, surf_fm, elev, to_top, 106]
        toMaster.append(thisLine)
        masterWNum.append(wnumber)


columns = {
    'shape' : 1, 
    'wnumber' : 2,
    'surf' : 7, 
    'elev' : 4, 
    'unit' : unitColumn['105'] 
    }
for i in t105:
    thisLine = []
    if i[columns["unit"]] != None and int(i[columns["wnumber"]]) not in masterWNum:
        shape = i[columns['shape']]
        wnumber = i[columns['wnumber']]
        surf_fm = i[columns['surf']]
        elev = i[columns['elev']]
        to_top = i[columns['unit']]
        thisLine = [shape, wnumber, surf_fm, elev, to_top, 105]
        toMaster.append(thisLine)
        masterWNum.append(wnumber)

toPath = os.path.join(outworkspace, unitName)

arcpy.CreateFeatureclass_management(outworkspace, unitName, "POINT")
arcpy.AddField_management(toPath, "wnumber", "LONG")
arcpy.AddField_management(toPath, "surf_fm", "TEXT", "", "", 254)
arcpy.AddField_management(toPath, "doc_elev", "DOUBLE", 5, 2)
arcpy.AddField_management(toPath, "unit_bls", "DOUBLE", 4, 1)
arcpy.AddField_management(toPath, "ofms_num", "LONG")


cursor = arcpy.da.InsertCursor(toPath, ("SHAPE@XY", "wnumber", "surf_fm","doc_elev", "unit_bls","ofms_num"))
for i in toMaster:
    cursor.insertRow(i)
del cursor  
