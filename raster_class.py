# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 13:29:00 2014

@author: Bassett_S
"""

import arcpy
import os
import shutil


class RasterClip:
    """Class for rasters that need to be clipped, projected, and tiled"""
    def __init__(self, aoiPath, mosaicPath, workspace, name):
        
        #paths
        self.aoiPath = aoiPath
        self.mosaicPath = mosaicPath
        self.workspace = workspace
        self.name = name
        self.aoiProjected = None
        self.clip = None
        self.project = None
        
        #CRS variables
        self.aoiSRS = None
        self.mosaicSRS = None
        self.transformation = None
                
        #Arcpy env settings
        arcpy.env.overwriteOutput = True
        arcpy.env.mask = self.aoiPath
        arcpy.env.extent = self.aoiPath
        
        #initialize workspaces
        self.rasterspace = self.create_raster_workspace()
        self.tilespace = self.create_tile_workspace()
        self.set_aoiSRS()
        self.set_mosaicSRS()
        self.set_transformation()
        
    def check_valid_aoiSRS(self):
        if self.aoiSRS == 'GCS_WGS_1984':
            print "AOI SRS Valid"
            arcpy.AddMessage("AOI SRS is valid")
            return True
        else:
            print "AOI SRS is not valid"
            arcpy.AddMessage("AOI SRS is not valid!")
            return False
    
    def create_raster_workspace(self):
        rasterspaceName = "RasterWorkspace.gdb"
        rasterspacePath = os.path.join(self.workspace, rasterspaceName)
        if not os.path.exists(rasterspacePath):
            arcpy.AddMessage("Creating Raster Workspace")
            arcpy.CreateFileGDB_management(self.workspace, rasterspaceName, "CURRENT")
        return rasterspacePath
    
    def create_tile_workspace(self):
        tilespaceName = "TileWorkspace.gdb"
        tilespacePath = os.path.join(self.workspace, tilespaceName)
        
        if not os.path.exists(tilespacePath):
            arcpy.AddMessage("Creating Tile Workspace")
            arcpy.CreateFileGDB_management(self.workspace, tilespaceName, "CURRENT")
        return tilespacePath
        
    def set_transformation(self):
        if self.mosaicSRS.name == "FDEPAlbersHARN" or \
            self.mosaicSRS.name == "NAD_1983_HARN_Florida_GDL_Albers" or \
            self.mosaicSRS.name == "NAD_1983_HARN_StatePlane_Florida_West_FIPS_0902_Feet" or \
            self.mosaicSRS.name == "NAD_1983_HARN_StatePlane_Florida_East_FIPS_0901_Feet":
            self.transformation = "NAD_1983_HARN_To_WGS_1984_2"
        elif self.mosaicSRS.name == "Albers_Conical_Equal_Area" \
            or self.mosaicSRS.name == "NAD_1983_UTM_Zone_16N":
            self.transformation = "WGS_1984_(ITRF00)_To_NAD_1983"
        
    def set_aoiSRS(self):
        srs = arcpy.Describe(self.aoiPath).spatialReference
        self.aoiSRS = srs
        
    def set_mosaicSRS(self):
        srs = arcpy.Describe(self.mosaicPath).spatialReference       
        self.mosaicSRS = srs
        
    def project_aoi(self):
        aoiProjPath = os.path.join(self.rasterspace, "aoiProjected")
        
        arcpy.Project_management(
                                  in_dataset = self.aoiPath, 
                                  out_dataset = aoiProjPath, 
                                  out_coor_system = self.mosaicSRS, 
                                  transform_method = self.transformation
                                  )

        self.aoiProjected = aoiProjPath
    
    def clip_to_rasterspace(self):
        self.clip = os.path.join(self.rasterspace, "clip")
        
        arcpy.AddMessage("Clipping Raster from Network Location")        
        arcpy.CopyRaster_management(
                                    in_raster = self.mosaicPath,
                                    out_rasterdataset = self.clip
                                    )
    
    def project_clip_raster(self, method):
        self.project = os.path.join(self.rasterspace, "project")
        
        arcpy.AddMessage("Projecting Raster")
        arcpy.ProjectRaster_management(
                                        in_raster=self.clip, 
                                        out_raster=self.project,
                                        out_coor_system=self.aoiSRS,
                                        resampling_type = method,
                                        geographic_transform = self.transformation
                                        )
        
        
        