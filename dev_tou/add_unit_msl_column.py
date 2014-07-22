# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 13:41:25 2014

@author: Bassett_S
"""
import arcpy
arcpy.env.workspace = r'C:\GISData\STATEMAP_TOR\OFMS106_TOR.gdb\Units_DEM_Elev2'


featureclasses = arcpy.ListFeatureClasses()
fieldName1 = "unit_msl"
fieldName2 = "elev_diff"

for i in featureclasses:
    arcpy.AddField_management(i, fieldName1, "DOUBLE")
    
for i in featureclasses:
    try:    
        arcpy.AddField_management(i, fieldName2, "DOUBLE")
    except:
        pass


expression = "!RASTERVALU!-!unit_bls!"

for i in featureclasses:
    arcpy.CalculateField_management(i, fieldName1, expression, "PYTHON")


expression = "abs(!RASTERVALU!-!doc_elev!)"

for i in featureclasses:
    arcpy.CalculateField_management(i, fieldName2, expression, "PYTHON")


for i in featureclasses:
    arcpy.Near_analysis(i,i)

