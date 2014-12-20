import arcpy, os


def mxdReport(mxd, report):
    dfNames = arcpy.mapping.ListDataFrames(mxd)
    layers = [[i for i in j] for j in arcpy.mapping.ListDataFrames(mxd)]
    layerNames = [[i.longName for i in j] for j in layers]
    pLayers = [[j.split("\\") for j in i] for i in layerNames]

               
    targetColumn = 5        
    with open(report, "w") as f:
        f.write("Data Frame\tLevel1\tLevel2\tLevel3\t\t\t\t\tIs Feature\tPath\n")
        printed = []
        for i,x,z in zip(pLayers, dfNames, layers):
            if x not in printed:
                f.write(x.name)
                f.write("\n")
                printed.append(x)
                
            for j, lyr in zip(i,z):
                 for v,k in enumerate(j):
                    if k not in printed:
                        if lyr.supports("DATASOURCE"):
                            f.write("\t"*(v+1))
                            f.write(str(k))
                            makeupTabs = targetColumn - v+1
                            f.write("\t"*makeupTabs)
                            f.write(str(lyr.isFeatureLayer))
                            f.write("\t")
                            f.write(lyr.dataSource)
                            f.write("\n")
                            printed.append(k)
                        else:
                            f.write("\t"*(v+1))
                            f.write(str(k))
                            makeupTabs = targetColumn - v+1
                            f.write("\t"*makeupTabs)
                            f.write(str(lyr.isFeatureLayer))
                            f.write("\n")
                            printed.append(k)

if __name__ == "__main__":
    mxds = [arcpy.mapping.MapDocument(r'S:\Statemap\OFMS_106_StAugustine\MXD\OFMS_SA_PLATE_1_DRAFT_DELIVERABLE.mxd'),arcpy.mapping.MapDocument(r'S:\Statemap\OFMS_106_StAugustine\MXD\OFMS_SA_PLATE_2_DRAFT_DELIVERABLE.mxd'),arcpy.mapping.MapDocument(r'S:\Statemap\OFMS_106_StAugustine\MXD\OFMS_SA_PLATE_3_DRAFT_DELIVERABLE.mxd')]
    reports = [r'C:\PythonWorkspace\mxdReport1.txt',r'C:\PythonWorkspace\mxdReport2.txt',r'C:\PythonWorkspace\mxdReport3.txt']
    for m,r in zip(mxds, report):
        mxdReport(m,r)
    
