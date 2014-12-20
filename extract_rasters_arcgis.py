# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 13:29:00 2014

@author: Bassett_S
"""

import arcpy
import os



class RasterClip:
    """Class for rasters that need to be clipped, projected, and tiled"""
    def __init__(self, aoiPath, mosaicPath, workspace, name, cascade=False, project_method="NEAREST"):
        self.method = project_method        
        
        #paths
        self.aoiPath = aoiPath
        self.mosaicPath = mosaicPath
        self.workspace = workspace
        self.name = name
        self.aoiProjected = None
        self.clip = None
        self.project = None
        
        #SRS
        self.aoiSRS = None
        self.mosaicSRS = None
        self.transformation = None
                
        #Arcpy env settings
        arcpy.env.overwriteOutput = True
        arcpy.env.mask = self.aoiPath
        arcpy.env.extent = self.aoiPath
        
        #tiling
        self.extent = None
        
        #initialize workspaces and attributes
        self.rasterspace = self.create_raster_workspace()
        self.tilespace = self.create_tile_workspace()
        self.set_aoiSRS()
        self.set_mosaicSRS()
        self.set_transformation()
        
        if cascade:
            self.project_aoi()
            self.clip_to_rasterspace()
            self.project_clip_raster(self.method)
            
        
    def check_valid_aoiSRS(self):
        if self.aoiSRS.name == 'GCS_WGS_1984':
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
                                        
    def __del__(self):
        arcpy.Delete_management(self.tilespace)
        arcpy.Delete_management(self.rasterspace)
 
       
class Tilespace:
    """Class for building tilesets"""
    
    def __init__(self, aoi, tilespace, step, cascade = False):
        """
        Inputs:
        aoi = path to the aoi feature class, must be in WGS projection
        tilespace = path to the tilespace where the tiles are to be built
        step = size of tiles, in degrees
        """
        
        #paths
        self.aoi = aoi
        self.tilespace = tilespace
        self.step = step
        
        #extent
        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None
        
        # Number of vertical and horizontal tiles
        self.htiles = None
        self.vtiles = None
        
        #tileset array
        self.tileset = None
        
        #tileset paths        
        self.tilesetPath = None
        self.tilesetClipPath = None
        
        #list of paths for the individual tiles
        self.tilePaths = None

        if cascade:
            self.set_extent()
            self.set_tilecount()
            self.set_tileset()
            self.write_tileset()
            self.write_tileset_id()
            self.clip_tileset()
            self.explode_tileset()
            
    def set_extent(self):
        extent = str(arcpy.Describe(self.aoi).extent).split(" ")
        extent = [float(item) for item in extent[0:4]]
        self.minX, self.minY, self.maxX, self.maxY = extent
    
    def set_tilecount(self):
        self.htiles = int((self.maxX - self.minX) / self.step) + 1
        self.vtiles = int((self.maxY - self.minY) / self.step) + 1
        
    def set_tileset(self):
        tileTuples = []
        incY = self.minY
        incX = self.minX
        for x in range(self.htiles):
            for y in range(self.vtiles):
                tileTuples.append(self.step_tile(incX, incY, self.step))
                incY += self.step
                    
            incY = self.minY
            incX += self.step
        self.tileset = tileTuples
    
    def step_tile(self, minX, minY, step):
        return[(minX, minY), (minX + step, minY), 
                (minX + step, minY + step), (minX, minY + step)]
    
    def write_tileset(self):
        features = []
        totalTiles = self.htiles * self.vtiles
        arcpy.AddMessage("Creating {0} tiles".format(totalTiles))
        
        for tile in self.tileset:
            features.append(arcpy.Polygon(arcpy.Array([arcpy.Point(*coords) for coords in tile])))
        self.tilesetPath = os.path.join(self.tilespace, "tileset")
        
        arcpy.CopyFeatures_management(features, self.tilesetPath)
        srs = arcpy.Describe(self.aoi).spatialReference
        arcpy.DefineProjection_management(self.tilesetPath, srs)
    
    def write_tileset_id(self):
        arcpy.AddField_management(self.tilesetPath, "tile_id","TEXT")
        with arcpy.da.UpdateCursor(self.tilesetPath, "tile_id") as cursor:
            for v, row in enumerate(cursor):
                row[0] = str(v)
                cursor.updateRow(row)
                
    def clip_tileset(self):
        self.tilesetClipPath = os.path.join(self.tilespace, "tileset_clip")
        arcpy.Clip_analysis(self.tilesetPath, self.aoi, self.tilesetClipPath)
        
    def explode_tileset(self):
        arcpy.MakeFeatureLayer_management(self.tilesetClipPath, "tileset_lyr")
        count = int(str((arcpy.GetCount_management(self.tilesetClipPath))))
        tilePaths = []
        for i in range(0, count):
            arcpy.SelectLayerByAttribute_management("tileset_lyr", 
                                                    "NEW_SELECTION",
                                                    "tile_id = '{0}'".format(i))
            newName = "Tile_{0}".format(i)
            newPath = os.path.join(self.tilespace, newName)
            tilePaths.append(newPath)
            arcpy.CopyFeatures_management("tileset_lyr", newPath)
        self.tilePaths = tilePaths
        


class Extractor:
    def __init__(self, tilespace, raster, name, cascade = False):
        """Class that works to extract tiles from a parent raster
        Inputs:
        tilespace: the file GDB that holdes the tiles produced by the tileset class
        raster: the original raster to be extracted from
        name: the base name for the new tiles
        """
        
        self.tilespace = tilespace
        self.raster = raster
        self.name = name
        
        self.tiles = None
        self.outputWorkspace = None        
        
        if cascade:
            self.inventory_tilespace()
            self.set_output_workspace()
            self.extract_tiles()
            
    def inventory_tilespace(self):
        arcpy.env.workspace = self.tilespace
        fcList = arcpy.ListFeatureClasses("Tile_*")
        fcPaths = [os.path.join(self.tilespace, item) for item in fcList]
        self.tiles = fcPaths
        arcpy.env.workspace = None
     
    def set_output_workspace(self):
        baseFolder = os.path.split(self.tilespace)[0]
        outputFolder = os.path.join(baseFolder, self.name)
        os.mkdir(outputFolder)
        self.outputWorkspace = outputFolder        
        
    def extract_tiles(self):
        for path in self.tiles:
            arcpy.env.mask = path
            arcpy.env.extent = path
            tileName = os.path.split(path)[1]
            tileNumber = tileName.split("_")[1]
            tileOutput = os.path.join(self.outputWorkspace, "{0}_{1}.tif".format(self.name, tileNumber))
            arcpy.CopyRaster_management(in_raster = self.raster,
                                        out_rasterdataset=tileOutput,
                                        RGB_to_Colormap = "RGBToColormap")



def clip_rasters(name, mpath, aoi, outputWorkspace, method):
    craster = RasterClip(aoi, mpath, outputWorkspace, name, cascade=True, project_method=method)
    arcpy.AddMessage("Building Tiles for AOI")    
    tspace = Tilespace(aoi, craster.tilespace, 0.25, cascade=True)
    arcpy.AddMessage("Extracting Raster Tiles")    
    extractor = Extractor(craster.tilespace, craster.project, name, cascade=True)
    del tspace, extractor
    del craster
 

   
if __name__ == "__main__":                                     
    aoi = arcpy.GetParameterAsText(0)
    outputWorkspace = arcpy.GetParameterAsText(1)        
    includeDRG = arcpy.GetParameter(2)
    includeCIR95 = arcpy.GetParameter(3)
    includeCIR99 = arcpy.GetParameter(4)
    includeCIR04 = arcpy.GetParameter(5)
    
    if includeDRG:
        arcpy.AddMessage("Beginning DRG")
        clip_rasters("DRG", r"\\fgs-csksv12-srv\Quarantine\DRG\DRG_24k.gdb\DRG24k", aoi, outputWorkspace, "NEAREST")
    
    if includeCIR95:
        arcpy.AddMessage("Beginning CIR95")
        clip_rasters("CIR95", r'\\fgs-csksv12-srv\Quarantine\CIR\CIR Catalog.gdb\CIR95', aoi, outputWorkspace, "BILINEAR")
        
    if includeCIR99:
        arcpy.AddMessage("Beginning CIR99")
        clip_rasters("CIR99", r'\\fgs-csksv12-srv\Quarantine\CIR\CIR Catalog.gdb\CIR99', aoi, outputWorkspace, "BILINEAR")
        
    if includeCIR04:
        arcpy.AddMessage("Beginning CIR04")
        clip_rasters("CIR04", r'\\fgs-csksv12-srv\Quarantine\CIR\CIR Catalog.gdb\CIR04', aoi, outputWorkspace, "BILINEAR")
        