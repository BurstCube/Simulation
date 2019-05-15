/////////
// 
// This is the setup file which contains the geometry file for ONE of the cylinders of the BurstCube CubeSat (website: )
// All the simulations use the MEGAlib toolkit (http://megalibtoolkit.com) 
//
// Author: Regina Caputo (regina.caputo@nasa.gov)
// Date: December 21, 2017
//
// Edited by Carolyn Kierans October 25, 2018
//
//
// Usage: geomega -g BurstCube_1Cylinder.geo.setup
//
/////////

//This file is to be called by BurstCubeCylinder.geo.setup. Uncomment the lines below to view this geometry on it's own with
//geomega -g BurstCube_1Cylinder.geo



#This is the CsI Detector with Optica pad, Quarts, Teflon, Epoxy, etc. The housing and SiPM board are in separate files.
Include $BURSTCUBE/Simulation/MEGAlib/geo/CalorimeterCSIProperties.det

#Start a virtual volume for all parts to live within
Volume SingleCsI
SingleCsI.Material Vacuum
SingleCsI.Virtual true
SingleCsI.Visibility 0
SingleCsI.Shape TUBS 0. 5. 1.5 0. 360.



#Single cylinder of Scintillator CsI 
#tech specs say it R=4.49, h=1.9 cm
Volume CSICylinder
CSICylinder.Material CsI
CSICylinder.Visibility 1
CSICylinder.Color 2
CSICylinder.Shape TUBS 0. 4.49 0.95  0. 360. 
CSICylinder.Position 0. 0. -0.05
CSICylinder.Mother SingleCsI

#Build the teflon coating around the CsI Cylinder dim are R_outter=4.59 cm, R_inner=4.54 cm, h= 1.9cm
#From CAD drawing measurement Oct 2018 dims are R_outter=4.55 cm, R_inner=4.50cm
Volume TeflonFrame
TeflonFrame.Material Teflon
#TeflonFrame.Shape TUBS  4.54 4.59 0.95  0. 360.
TeflonFrame.Shape TUBS 4.50 4.55 0.95 0. 360.
TeflonFrame.Position 0 0 -0.05
TeflonFrame.Color 8
TeflonFrame.Visibility 1
TeflonFrame.Mother SingleCsI

#Build the vacuum gap?? around the teflon around the CsI cylinder dim are R_outter=4.54 cm, R_inner=4.49 cm, h= 1.9 cm
#CK questions why we need to add vacuum here when the whole volume is in vacuum already...
Volume VacuumFrame
VacuumFrame.Material Vacuum
#VacuumFrame.Shape TUBS  4.49 4.54 0.95 0. 360.
VacuumFrame.Shape TUBS 4.49 4.50 0.95 0. 360.
VacuumFrame.Position 0 0 -0.05
VacuumFrame.Color 9
VacuumFrame.Visibility 0
VacuumFrame.Mother SingleCsI


//This chunk is the sticky bit after the Al window
//the tech specs say Epoxy dim are R=4.59 cm, h=0.05 cm
#CK doesnt see this in the CAD model..
#Volume StickyWindow
#StickyWindow.Material Epoxy
#StickyWindow.Shape TUBS  0. 4.59 0.025 0. 360.
#StickyWindow.Position 0 0 0.975
#StickyWindow.Color 6
#StickyWindow.Visibility 1
#StickyWindow.Mother SingleCsI

#Teflon top
//Regina's comment: the tech specs say teflon dim are R=4.59 cm, h=0.05 cm
#From the CAD drawing measurement Oct 2018 dims are R=4.50 cm h = 0.05 cm
Volume TeflonWindow
TeflonWindow.Material Teflon
#TeflonWindow.Shape TUBS  0. 4.59 0.025 0. 360.
TeflonWindow.Shape TUBS  0. 4.49 0.025 0. 360.
TeflonWindow.Position 0 0 0.925
TeflonWindow.Color 3
TeflonWindow.Visibility 1
TeflonWindow.Mother SingleCsI

#This chunk is the Silicone rubber optical interface i.e. Optical Pad on the top
//Regina's comment: the tech specs say need this window above glass. Dim are R=4.74 cm, h=0.1 cm
Volume SiliconeWindowTop
SiliconeWindowTop.Material Silicone
#SiliconeWindowTop.Shape TUBS  0. 4.74 0.05 0. 360.
SiliconeWindowTop.Shape TUBS 0. 4.55 0.05 0. 360.
SiliconeWindowTop.Position 0 0 1.0
SiliconeWindowTop.Color 5
SiliconeWindowTop.Visibility 1
SiliconeWindowTop.Mother SingleCsI

#This chunk is the Silicone rubber optical interface i.e. Optical Pad on below the CsI
//Regina's comment: the tech specs say need this window above glass. Dim are R=4.74 cm, h=0.1 cm
#From CAD model Oct 2018 dims are R_outer = 4.775cm
Volume SiliconeWindowBottomOne
SiliconeWindowBottomOne.Material Silicone
SiliconeWindowBottomOne.Shape TUBS 0. 4.775 0.05 0. 360.
SiliconeWindowBottomOne.Position 0 0 -1.05
SiliconeWindowBottomOne.Color 5
SiliconeWindowBottomOne.Visibility 1
SiliconeWindowBottomOne.Mother SingleCsI

#This chunk is the Quartz window on bottom
//Regina's comment: the tech specs say quartz the window is below the CsI but not in the hole. Dim are R=4.74 cm, h=0.3 cm
# From the CAD model Oct 2018 dims are R = 4.825 cm h = 0.3 cm
Volume GlassWindow
GlassWindow.Material Silica
#GlassWindow.Shape TUBS  0. 4.74 0.15 0. 360.
GlassWindow.Shape TUBS 0. 4.825 0.15 0. 360.
GlassWindow.Position 0 0 -1.25
GlassWindow.Color 6
GlassWindow.Visibility 1
GlassWindow.Mother SingleCsI

#This chunk is the Silicone rubber optical interface i.e. Optical Pad below the Quartz window
//Regina's comment: the tech specs say need this window above glass. Dim are R=4.74 cm, h=0.1 cm
# From the CAD model Oct 2018 dims are R = 4.75 cm
Volume SiliconeWindowBottomTwo
SiliconeWindowBottomTwo.Material Silicone
SiliconeWindowBottomTwo.Shape TUBS  0. 4.74 0.05 0. 360.
SiliconeWindowBottomTwo.Position 0 0 -1.45
SiliconeWindowBottomTwo.Color 2
SiliconeWindowBottomTwo.Visibility 1
SiliconeWindowBottomTwo.Mother SingleCsI

# Quartz Epoxy ring surrounding Quartz window made up two parts with different inner radii
Volume QuartzEpoxyRingOne
QuartzEpoxyRingOne.Material Epoxy
QuartzEpoxyRingOne.Shape TUBS  4.825 4.875 0.125 0. 360.
QuartzEpoxyRingOne.Position 0 0 -1.25
QuartzEpoxyRingOne.Color 7
QuartzEpoxyRingOne.Visibility 1
QuartzEpoxyRingOne.Mother SingleCsI

Volume QuartzEpoxyRingTwo
QuartzEpoxyRingTwo.Material Epoxy
QuartzEpoxyRingTwo.Shape TUBS  4.775 4.875 0.05 0. 360.
QuartzEpoxyRingTwo.Position 0 0 -1.05
QuartzEpoxyRingTwo.Color 7
QuartzEpoxyRingTwo.Visibility 1
QuartzEpoxyRingTwo.Mother SingleCsI




#// Build the volume to put the readouts in dim are R=4.5, h=0.22 cm
#Volume ReadOutDetectorVolume
#ReadOutDetectorVolume.Material Vacuum 
#ReadOutDetectorVolume.Shape TUBS  0. 4.5 0.11  0. 360. 
#//ReadOutDetectorVolume.Rotation 25.0 -25.0 0.0
#ReadOutDetectorVolume.Position 0. 0. -1.61
#ReadOutDetectorVolume.Color 1
#ReadOutDetectorVolume.Visibility 1
#ReadOutDetectorVolume.Mother SingleCsI


#//This chunk is the Si plane below the glass
#//the tech specs say Si in the Al Frame/hole dim are  R=4.5, h=0.020 cm
#//Slightly smaller than the circumfrence to avoid overlap
#Volume SiPlane
#SiPlane.Material Silicon
#SiPlane.Shape TUBS 0. 4.5 0.01 0. 360. 
#//For the nominal thickness
#SiPlane.Position 0. 0. 0.1
#SiPlane.Color 8
#SiPlane.Visibility 1
#SiPlane.Mother ReadOutDetectorVolume

#//This chunk is the G10 below the Si
#//the tech specs say dim are R=4.5, h=0.20 cm
#Volume G10Plane
#G10Plane.Material CircuitBoard
#G10Plane.Shape TUBS 0. 4.5 0.1 0. 360.
#G10Plane.Position 0. 0. -0.01
#G10Plane.Color 8
#G10Plane.Visibility 1
#G10Plane.Mother ReadOutDetectorVolume


