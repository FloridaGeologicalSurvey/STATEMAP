# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 11:47:09 2014

@author: Bassett_S
"""


import arcpy, os
workspace = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb'
outworkspace = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\Units'
ofms106 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\SA_Wells'
ofms105 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\DB_Wells'
ofms103 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\OFMS103_104'
ofms101 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\OFMS101_Wells'
ofms100 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\Wells_OFMS100'
ofms94 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\Wells_OFMS94'
ofms93 = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\OFMS93_Wells'


######## FUNCTIONS #################################

def printFields(fnames, ftypes):
    for v, (i, j) in enumerate(zip(fnames, ftypes)):
        print v, i, j

###################################################


with arcpy.da.SearchCursor(ofms106, "*") as cursor:
	t106 = [row for row in cursor]

with arcpy.da.SearchCursor(ofms105, "*") as cursor:
	t105 = [row for row in cursor]

with arcpy.da.SearchCursor(ofms103, "*") as cursor:
	t103 = [row for row in cursor]
 
with arcpy.da.SearchCursor(ofms101, "*") as cursor:
    t101 = [row for row in cursor]
    
with arcpy.da.SearchCursor(ofms100, "*") as cursor:
	t100 = [row for row in cursor]

    
with arcpy.da.SearchCursor(ofms94, "*") as cursor:
	t94 = [row for row in cursor]
    
with arcpy.da.SearchCursor(ofms93, "*") as cursor:
	t93 = [row for row in cursor]
 
#field names	
f106 = [i.name for i in arcpy.ListFields(ofms106)]
f105 = [i.name for i in arcpy.ListFields(ofms105)]
f103 = [i.name for i in arcpy.ListFields(ofms103)]
f101 = [i.name for i in arcpy.ListFields(ofms101)]
f100 = [i.name for i in arcpy.ListFields(ofms100)]
f94 = [i.name for i in arcpy.ListFields(ofms94)]
f93 = [i.name for i in arcpy.ListFields(ofms93)]

#field types
ftype106 = [i.type for i in arcpy.ListFields(ofms106)]
ftype105 = [i.type for i in arcpy.ListFields(ofms105)]
ftype103 = [i.type for i in arcpy.ListFields(ofms103)]
ftype101 = [i.type for i in arcpy.ListFields(ofms101)]
ftype100 = [i.type for i in arcpy.ListFields(ofms100)]
ftype94 = [i.type for i in arcpy.ListFields(ofms94)]
ftype93 = [i.type for i in arcpy.ListFields(ofms93)]


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
    'to' : 49 
    }
for i in t106:
    thisLine = []
    if i[columns['to']] != None:
        shape = i[columns['shape']]
        wnumber = i[columns['wnumber']]
        surf_fm = i[columns['surf']]
        elev = i[columns['elev']]
        to_top = i[columns['to']]
        thisLine = [shape, wnumber, surf_fm, elev, to_top, 106]
        toMaster.append(thisLine)
        masterWNum.append(wnumber)


columns = {
    'shape' : 1, 
    'wnumber' : 2,
    'surf' : 7, 
    'elev' : 4, 
    'to' : 14 
    }
for i in t105:
    thisLine = []
    if i[columns["to"]] != None and int(i[columns["wnumber"]]) not in masterWNum:
        shape = i[columns['shape']]
        wnumber = i[columns['wnumber']]
        surf_fm = i[columns['surf']]
        elev = i[columns['elev']]
        to_top = i[columns['to']]
        thisLine = [shape, wnumber, surf_fm, elev, to_top, 105]
        toMaster.append(thisLine)
        masterWNum.append(wnumber)

columns = {
    'shape' : 1, 
    'wnumber' : 2,
    'surf' : 8, 
    'elev' : 4, 
    'to' : 21 
    }
for i in t103:
    thisLine = []
    if i[columns["to"]] != None and (i[columns["wnumber"]] != None and int(i[columns["wnumber"]]) not in masterWNum):
        shape = i[columns['shape']]
        wnumber = int(i[columns['wnumber']])
        surf_fm = i[columns['surf']]
        elev = i[columns['elev']]
        to_top = i[columns['to']]
        thisLine = [shape, wnumber, surf_fm, elev, to_top, 103]
        toMaster.append(thisLine)
        masterWNum.append(wnumber)

       
columns = {
    'shape' : 55, 
    'wnumber' : 3,
    'surf' : 39, 
    'elev' : 35, 
    'to' : 49 
    }       

for i in t101:
    thisLine = []
    if i[columns["to"]] != None and int(i[columns["wnumber"]]) not in masterWNum and i[columns["to"]] != 999:
        shape = i[columns['shape']]
        wnumber = int(i[columns['wnumber']])
        surf_fm = i[columns['surf']]
        elev = i[columns['elev']]
        to_top = i[columns['to']]
        thisLine = [shape, wnumber, surf_fm, elev, to_top, 101]
        toMaster.append(thisLine)
        masterWNum.append(wnumber)

columns = {
    'shape' : 1, 
    'wnumber' : 2,
    'surf' : 48, 
    'elev' : 20, 
    'to' : 55 
    }  
for i in t100:
    thisLine = []
    if i[columns["to"]] != None and int(i[columns["wnumber"]]) not in masterWNum and i[columns["to"]] != 999:
        shape = i[columns['shape']]
        wnumber = int(i[columns['wnumber']])
        surf_fm = i[columns['surf']]
        elev = float(i[columns['elev']])
        to_top = i[columns['to']]
        thisLine = [shape, wnumber, surf_fm, elev, to_top, 100]
        toMaster.append(thisLine)
        masterWNum.append(wnumber)


columns = {
    'shape' : 1, 
    'wnumber' : 2,
    'surf' : 25, 
    'elev' : 17, 
    'to' : 31 
    }  
for i in t94:
    thisLine = []
    if len(i[columns["to"]].strip()) != 0 and i[columns["wnumber"]] not in masterWNum:
        shape = i[columns['shape']]
        wnumber = i[columns['wnumber']]
        surf_fm = i[columns['surf']]
        elev = float(i[columns['elev']])
        to_top = float(i[columns['to']])
        thisLine = [shape, wnumber, surf_fm, elev, to_top, 94]
        toMaster.append(thisLine)
        masterWNum.append(wnumber)



toPath = os.path.join(outworkspace, "To")

arcpy.CreateFeatureclass_management(outworkspace, "To", "POINT")
arcpy.AddField_management(toPath, "wnumber", "LONG")
arcpy.AddField_management(toPath, "surf_fm", "TEXT", "", "", 254)
arcpy.AddField_management(toPath, "doc_elev", "DOUBLE", 5, 2)
arcpy.AddField_management(toPath, "unit_bls", "DOUBLE", 4, 1)
arcpy.AddField_management(toPath, "ofms_num", "LONG")


cursor = arcpy.da.InsertCursor(toPath, ("SHAPE@XY", "wnumber", "surf_fm","doc_elev", "unit_bls","ofms_num"))
for i in toMaster:
    cursor.insertRow(i)
del cursor  
