# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 14:13:41 2014

@author: Bassett_S
"""

import arcpy

"""
fcPath = arcpy.GetParameterAsText(0)
outputPath = arcpy.GetParameterAsText(1)
"""

fcPath = 'U:\\FGS-old\\Projects\\DEM_Sinkhole_Project\\Data\\Field Data\\Sites_Visited.mdb\\Sites_Visited'
outputPath = r'C:\PythonWorkspace\test_meta.csv'


fields = arcpy.ListFields(fcPath)

with open(outputPath, 'w') as f:
    for i in fields:
        f.write('{0}\t{1}\t{2}\n'.format(str(i.name), str(i.type), str(i.length)))

arcpy.AddMessage('{0} meta.csv created'.format(outputPath))
