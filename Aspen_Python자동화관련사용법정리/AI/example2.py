import os ##
import argparse ##
import logging ##
import csv ## 
import win32com.client ## 

ASPEN_FILE = "[GEN_TARGET]" ## 
AspenSimulation = win32com.client.gencache.EnsureDispatch("Apwn.Document") ##
AspenSimulation.InitFromArchive2(os.path.abspath(ASPEN_FILE)) ## 
AspenSimulation.Visible = "[GEN_TARGET]|True|False" ## 
STRM = AspenSimulation.Tree.Elements("Data").Elements("Streams")  ##
BLK  = AspenSimulation.Tree.Elements("Data").Elements("Blocks") ## 
def close_simulation(sim):
    fullpath = sim.FullName
    sim.Close(os.path.abspath(fullpath))
RESULT = "[GEN_TARGET]"
# CASE_STUDY [GEN_TARGET]
# SAVE SECTION [GEN_TARGET]


