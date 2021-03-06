# -*- coding: utf-8 -*-
###################################################################################
#
#  InitGui.py
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
###################################################################################


import os


import Asm4wb_locator
global Asm4wb_icon
Asm4wb_path = os.path.dirname( Asm4wb_locator.__file__ )
Asm4wb_icon = os.path.join( Asm4wb_path , 'Resources/icons/Assembly4.svg' )

# I don't like this being here
import selectionFilter


"""
    +-----------------------------------------------+
    |            Initialize the workbench           |
    +-----------------------------------------------+
"""
class Assembly4Workbench(Workbench):

    global Asm4wb_icon
    global selectionFilter
    MenuText = "Assembly 4"
    ToolTip = "Assembly 4 workbench"
    Icon = Asm4wb_icon

    def __init__(self):
        "This function is executed when FreeCAD starts"
        pass

    def Activated(self):
        "This function is executed when the workbench is activated"
        FreeCAD.Console.PrintMessage("Activating Assembly4 WorkBench\n")
        
        # make buttons of the selection toolbar checkable
        from PySide import QtGui
        mainwin = Gui.getMainWindow()
        sf_tb = None
        for tb in mainwin.findChildren(QtGui.QToolBar):
            if tb.objectName()=='Selection Filter':
                sf_tb = tb
        # make all buttons except last one (clear selection filter) checkable
        if sf_tb is not None:
            for button in sf_tb.actions()[0:-1]:      
                button.setCheckable(True)
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        selectionFilter.observerDisable()
        FreeCAD.Console.PrintMessage("Leaving Assembly4 WorkBench\n")
        return 

    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"

        """
    +-----------------------------------------------+
    |        This is where all is defined           |
    +-----------------------------------------------+
        """
    def Initialize(self):
        FreeCAD.Console.PrintMessage("Assembly4 WorkBench initializing .")
        FreeCADGui.updateGui()
        import newModelCmd         # creates a new App::Part container called 'Model'
        self.dot()
        import newDatumCmd         # creates a new LCS in 'Model'
        self.dot()
        import newPartCmd          # creates a new App::Part container called 'Model'
        self.dot()
        import mirrorPartCmd       # creates a new App::Part container with the mirrored part of the selection
        self.dot()
        import infoPartCmd         # edits part information for BoM
        self.dot()
        import insertLinkCmd       # inserts an App::Link to a 'Model' in another file
        self.dot()
        import placeLinkCmd        # places a linked part by snapping LCS (in the Part and in the Assembly)
        self.dot()
        import placeDatumCmd       # places an LCS relative to an external file (creates a local attached copy)
        self.dot()
        import importDatumCmd      # creates an LCS in assembly and attaches it to an LCS relative to an external file
        self.dot()
        import releaseAttachmentCmd# creates an LCS in assembly and attaches it to an LCS relative to an external file
        self.dot()
        import VariablesLib        # creates an LCS in assembly and attaches it to an LCS relative to an external file
        self.dot()
        import AnimationLib        # creates an LCS in assembly and attaches it to an LCS relative to an external file
        self.dot()
        import updateAssemblyCmd   # updates all parts and constraints in the assembly
        self.dot()
        #import newLinkArray       # creates a new array of App::Link
        #import makeLinkArray      # creates a new array of App::Link
        import gotoDocumentCmd     # opens the documentof the selected App::Link
        self.dot()
        import Asm4_Measure        # Measure tool in the Task panel
        self.dot()
        import makeBomCmd          # creates the parts list
        self.dot()
        import HelpCmd             # shows a basic help window
        self.dot()
        import showHideLcsCmd      # shows/hides all the LCSs
        self.dot()
        import configurationEngine # save/restore configuration
        self.dot()

        # Fasteners
        if self.checkWorkbench('FastenersWorkbench'):
            # a library to handle fasteners from the FastenersWorkbench
            import FastenersLib
            self.FastenersCmd = 'Asm4_Fasteners'
        else:
            # a dummy library if the FastenersWorkbench is not installed
            import FastenersDummy
            self.FastenersCmd = 'Asm4_insertScrew'
        self.dot()


        # Define Menus
        # commands to appear in the Assembly4 menu 'Assembly'
        self.appendMenu( "&Assembly", self.assemblyMenuItems() )
        self.dot()

        # self.appendMenu("&Geometry",["Asm4_newPart"])

        # additional entry in the Help menu
        self.appendMenu("&Help", ["Asm4_Help"])
        self.dot()

        # Define Toolbars
        # commands to appear in the Assembly4 toolbar
        self.appendToolbar( "Assembly", self.assemblyToolbarItems() )
        self.dot()

        # build the selection toolbar
        self.appendToolbar( "Selection Filter", self.selectionToolbarItems() )
        self.dot()

        # self.appendToolbar("Geometry",["Asm4_newPart"])

        FreeCAD.Console.PrintMessage(" done.\n")
        """
    +-----------------------------------------------+
    |           Initialisation finished             |
    +-----------------------------------------------+
        """



    """
    +-----------------------------------------------+
    |            Assembly Menu & Toolbar            |
    +-----------------------------------------------+
    """
    def assemblyMenuItems(self):
        commandList = [ "Asm4_newModel",
                        "Asm4_newPart", 
                        "Asm4_newBody", 
                        "Asm4_insertLink", 
                        self.FastenersCmd, 
                        "Separator",
                        "Asm4_newSketch", 
                        "Asm4_newLCS", 
                        "Asm4_newPlane", 
                        "Asm4_newAxis", 
                        "Asm4_newPoint", 
                        "Asm4_newHole", 
                        "Asm4_importDatum", 
                        "Separator",
                        "Asm4_placeLink", 
                        "Asm4_mirrorPart", 
                        #"Asm4_newCircularArray", 
                        "Asm4_placeFastener", 
                        "Asm4_cloneFastenersToAxes", 
                        "Asm4_placeDatum", 
                        "Asm4_releaseAttachment", 
                        #"Asm4_makeLinkArray",
                        "Separator",
                        "Asm4_infoPart", 
                        "Asm4_makeBOM", 
                        "Asm4_Measure", 
                        'Asm4_showLcs',
                        'Asm4_hideLcs',
                        "Asm4_addVariable", 
                        "Asm4_delVariable", 
                        "Asm4_Animate", 
                        "Asm4_updateAssembly"]
        return commandList
        
    def assemblyToolbarItems(self):
        commandList = [ "Asm4_newModel",
                        "Asm4_newPart", 
                        "Asm4_newBody", 
                        "Asm4_infoPart", 
                        "Asm4_insertLink", 
                        self.FastenersCmd, 
                        "Separator",
                        "Asm4_newSketch", 
                        'Asm4_createDatum',
                        "Asm4_importDatum", 
                        "Separator",
                        "Asm4_placeLink", 
                        'Asm4_placeFastener',
                        #'Asm4_cloneFastenersToAxes',
                        "Asm4_placeDatum", 
                        "Asm4_mirrorPart", 
                        #"Asm4_newCircularArray", 
                        "Separator",
                        #"Asm4_makeLinkArray",
                        #"Draft_PolarArray",
                        "Asm4_makeBOM", 
                        "Asm4_Measure", 
                        "Asm4_variablesCmd",
                        "Asm4_Animate",
                        "Asm4_updateAssembly"]
        return commandList


    """
    +-----------------------------------------------+
    |                 Selection Toolbar             |
    +-----------------------------------------------+
    """
    def selectionToolbarItems(self):
        # commands to appear in the Selection toolbar
        commandList =  ["Asm4_SelectionFilterVertexCmd",
                        "Asm4_SelectionFilterEdgeCmd",
                        "Asm4_SelectionFilterFaceCmd",
                        "Asm4_selObserver3DViewCmd" ,
                        "Asm4_SelectionFilterClearCmd"]
        return commandList


    """
    +-----------------------------------------------+
    |                Contextual Menus               |
    +-----------------------------------------------+
    """
    def ContextMenu(self, recipient):
        # This is executed whenever the user right-clicks on screen"
        # "recipient" will be either "view" or "tree"
        contextMenu  = ['Asm4_gotoDocument'  ,
                        'Asm4_showLcs'       ,
                        'Asm4_hideLcs'       ]
        # commands to appear in the 'Assembly' sub-menu in the contextual menu (right-click)
        assemblySubMenu =[ "Asm4_insertLink"    , 
                        "Asm4_placeLink"     , 
                        "Asm4_importDatum"   ,
                        "Asm4_placeDatum"    ,
                        'Asm4_FSparameters'  ,
                        'Asm4_placeFastener' ,
                        'Asm4_cloneFastenersToAxes' ,
                        'Separator'          ,
                        'Asm4_saveConfiguration',
                        'Asm4_restoreConfiguration']
        # commands to appear in the 'Create' sub-menu in the contextual menu (right-click)
        createSubMenu =["Asm4_newSketch",  
                        "Asm4_newBody", 
                        "Asm4_newLCS", 
                        "Asm4_newAxis", 
                        "Asm4_newPlane", 
                        "Asm4_newPoint", 
                        "Asm4_newHole", 
                        "Asm4_insertScrew", 
                        "Asm4_insertNut", 
                        "Asm4_insertWasher"]

        self.appendContextMenu( "", "Separator")
        self.appendContextMenu( "", contextMenu ) # add commands to the context menu
        self.appendContextMenu( "Assembly", assemblySubMenu ) # add commands to the context menu
        self.appendContextMenu( "Create", createSubMenu ) # add commands to the context menu
        self.appendContextMenu( "", "Separator")



    """
    +-----------------------------------------------+
    |               helper functions                |
    +-----------------------------------------------+
    """
    def checkWorkbench( self, workbench ):
        # checks whether the specified workbench (a 'string') is installed
        listWB = Gui.listWorkbenches()
        hasWB = False
        for wb in listWB.keys():
            if wb == workbench:
                hasWB = True
        return hasWB


    def dot(self):
        FreeCAD.Console.PrintMessage(".")
        FreeCADGui.updateGui()


    
"""
    +-----------------------------------------------+
    |          actually make the workbench          |
    +-----------------------------------------------+
"""
wb = Assembly4Workbench()
Gui.addWorkbench(wb)



