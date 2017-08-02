#Author: Deidre Mensah
#Date Modified: 3/31/2017
#Purpose: Tool to intersect features in a workspace and calculate acreage of intersectd features.

#inputs: features to be intersected, features that will do the intersecting
#outputs: features that have been intersected to a boundary
#processing: intersects multiple features with one single one

#imports modules
import arcpy
import os

#creates variables to store input parameters to be entered in by user
input_workspace = arcpy.GetParameterAsText(0)
intersect_fc = arcpy.GetParameterAsText(1)
output_workspace = arcpy.GetParameterAsText(2)
    
#sets the environmental workspace settings (stores filepath)
arcpy.env.workspace = input_workspace

#overwrites output files in workspace to prevent program from stopping
arcpy.env.overwriteOutput = True

#creates list of feature classes from workspace, which was set 5 lines ago
fc_list = arcpy.ListFeatureClasses()
if len(fc_list) == 0:
    arcpy.AddError(input_workspace + " has no feature classes.")

#Removes a feature class that has the same filepath as the workspace
desc = arcpy.Describe(intersect_fc)
if desc.path == input_workspace:
    fc_list.remove(desc.file)

#Creates output folder with the same name as the output feature class if doesn't already exist.
if arcpy.Exists(output_workspace) == False:
    arcpy.CreateFolder_management(os.path.split(output_workspace)[0], os.path.split(output_workspace)[1])

#Loops through a list of feature classes in workspace, creates file path location for each newly created feature class and clips features.
for fc in fc_list:
    out_fc = os.path.join(output_workspace, fc)
    arcpy.AddMessage("Intersecting " + fc + "...")
    arcpy.Intersect_analysis([fc, intersect_fc], out_fc,"ALL","","")
    
#Adds "ACRES" field to each feature class
    fieldName = "ACRES"
    fieldType = "DOUBLE"
    arcpy.AddField_management(fc, fieldName, fieldType)
    arcpy.CalculateField_management(fc, fieldName, "!shape.area@acres!", "PYTHON", "")
else:
    arcpy.AddMessage("Your features have been intersected and the acreages have been calculated!")
