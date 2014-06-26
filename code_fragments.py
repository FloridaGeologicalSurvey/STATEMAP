# -*- coding: utf-8 -*-
"""
Created on Tue May 20 10:49:39 2014

@author: Bassett_s
"""
import csv, arcpy
ss = r"C:\PythonData\Clint2"

def readHeader(filePath):
    with open(filePath, 'rb') as f:
        f_csv = csv.reader(f, delimiter="\t")
        header = next(f_csv)
    return header

def readData(filePath):
    with open(filePath, 'rb') as f:
        f_csv = csv.reader(f, delimiter="\t")
        header = next(f_csv)
        allRows = [row for row in f_csv]
    return allRows
        
head = readHeader(ss)
data = readData(ss)
wnums = [i[0] for i in data]
uniqueWnums = list(set(wnums))

sourceList = []
for i in uniqueWnums:
    thisRow = [i]
    sources = []
    for j in data:
        if i == j[0]:
            sources.append(j[1])
        else: pass
    thisRow.append(sources)
    sourceList.append(thisRow)

noSource = []
singleSource = []
multiSource = []
for i in sourceList:
    if len(i[1])==0:
        noSource.append(i)
    elif len(i[1])==1:
        singleSource.append(i)
    elif len(i[1])>1:
        multiSource.append(i)
sMap = []
for i in multiSource:
    for j in i[1]:
        if j[0:4]=="OFMS":
            sMap.append(i)
            break
notSmap = []
for i in multiSource:
    if i not in sMap:
        notSmap.append(i)


priority = ['OFMS 105', 'OFMS 104', 'OFMS103', 'OFMS102',  'OFMS101', 'OFMS100', 'OFMS99',  'OFMS98', 'OFMS97', 'OFMS94', 'OFMS93', 'OFMS92', 'OFMS91', 'FGS_Bulletin68', 'FAVAV2']
pDict = {}
for v, i in enumerate(priority):
    pDict[i] = v
pRevDict = {}
for v, i in enumerate(priority):
    pRevDict[v] = i

pMaster = []
for i in multiSource:
    pList = []
    for j in i[1]:
        pList.append(pDict[j])
    pMaster.append([i[0], pRevDict[min(pList)]])






masterList = []
for i in data:
    for j in singleSource:
        if i[0]==j[0]:
            masterList.append(i)
done = []
for i in data:
    for j in pMaster:
        if i[0]==j[0] and i[1]==j[1] and done.count(j[0])==0:
            masterList.append(i)
            done.append(i[0])
            






        


                

"""
with open(r"C:\PythonData\ClintSourcesBad.txt", 'wt') as f:
    for i in fN:
        f.write(str(i))
        f.write('\t')
    f.write('\n')
    for i in masterList:
        for j in i:
            f.write(str(j))
            f.write("\t")
        f.write("\n")

for v,i in enumerate(head):
    print v, head[v]
    
    
    
    
for i in mList:
    if mList.count(i)>1:
        print mList.index(i)


for i in masterList:
    if i[0] == '19999' or i[0]=="0" or i[0]=="1904":
        print i        

"""

"""
#Arcpy code run in ArcCatalog interpreter
import arcpy, csv
from arcpy import env
workspacePath = r"C:\GISData\Sinkhole Project\Clint_TOR.gdb"
arcpy.CreateTable_management(workspacePath, "ClintTable")

ClintTable = r"C:\GISData\Sinkhole Project\Clint_TOR.gdb\ClintTable"
bad = r"C:\PythonData\ClintSourcesBad.txt"
#run un-commented code in this file


fNames = r"C:\PythonData\clint_fNames.txt"
fTypes = r"C:\PythonData\clint_fTypes2.txt"
fT = readHeader(fTypes)
fN = readHeader(fNames)

for i,x in zip(fN, fT):
    if x == "TEXT":
        arcpy.AddField_management(ClintTable, i, x, field_length=254)
    else:
        arcpy.AddField_management(ClintTable, i, x)

skipped = []
rows = arcpy.InsertCursor(ClintTable)    


for i in masterList:
    row = rows.newRow()
    print "-"*40
    print i[0]
    try:
        for t, x, y in zip(fT, fN, i):      
            #print x, t, y
            if t == "TEXT":
                if len(y.strip()) == 0:
                    cast = None
                else:
                    cast = str(y)
                row.setValue(x, cast)
            elif t == "SHORT" or t == "LONG":
                if len(y.strip()) == 0:
                    cast = None
                else:
                    cast = int(float(y))
                row.setValue(x, cast)
            elif t == "FLOAT":
                if len(y.strip()) == 0 or y=="?" or y=="9999" or y =="-9999":
                    cast = None
                elif y.strip()=="NR":
                    cast = float(-9999)
                else:
                    cast = float(y)
                row.setValue(x, cast)
        print "*"*20,"SUCCESS","*"*20
        rows.insertRow(row)
    except:
        skipped.append([i[0], t, x])



del row
del rows


fullSkipped = []
for i in masterList:
    for j in skipped:
        if i[0] == j:
            fullSkipped.append(i)
    
with open(r"C:\PythonData\ClintSourcesBad.txt", 'wt') as f:
    for i in fN:
        f.write(str(i))
        f.write('\t')
    f.write('\n')
    for i in fullSkipped:
        for j in i:
            f.write(str(j))
            f.write("\t")
        f.write("\n")
            
#ClintSourcesBad.txt was modified by hand into the following file
badPath = r"C:\PythonData\ClintSourcesBad_load.txt"

bad = readData(badPath)
skipped2 = []    
#reload attempt
for i in bad:
    row = rows.newRow()
    print "-"*40
    print i[0]
    try:
        for t, x, y in zip(fT, fN, i):      
            #print x, t, y
            if t == "TEXT":
                if len(y.strip()) == 0:
                    cast = None
                else:
                    cast = str(y)
                row.setValue(x, cast)
            elif t == "SHORT" or t == "LONG":
                if len(y.strip()) == 0:
                    cast = None
                else:
                    cast = int(float(y))
                row.setValue(x, cast)
            elif t == "FLOAT":
                if len(y.strip()) == 0 or y=="?" or y=="9999" or y =="-9999":
                    cast = None
                elif y.strip()=="NR":
                    cast = float(-9999)
                else:
                    cast = float(y)
                row.setValue(x, cast)
        print "*"*20,"SUCCESS","*"*20
        rows.insertRow(row)
    except:
        skipped2.append([i[0], t, x])
        