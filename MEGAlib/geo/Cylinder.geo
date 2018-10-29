/////////
// 
// This is the geometry file that creates one cylinder of the BurstCube CubeSat Satellite
// All the simulations use the MEGAlib toolkit (http://megalibtoolkit.com) 
//
// Author: Regina Caputo (regina.caputo@nasa.gov)
// Date: Oct 29, 2018
//
// Usage: in one of the geo.setup files
//
/////////

///// Uncomment these lines to run standalone 
//SurroundingSphere 100.0 0.0 0.0 0.0 100.0
//Include Materials.geo
/////


// Build the volume to put everything in dim are R=5.0, h=3.5 cm
Volume DetectorVolume
DetectorVolume.Material Vacuum 
DetectorVolume.Shape TUBS  0. 5.0 1.75  0. 360. 
DetectorVolume.Color 1
DetectorVolume.Visibility 0
// NEEDS THIS LINE TO VIEW ALONE:
//DetectorVolume.Mother 0

//This is the CsI Detector
Include $BURSTCUBE/Simulation/MEGAlib/geo/CalorimeterCSIProperties.det

// Build the housing around the CsI Cylinder dim are R_outter=4.981 cm, R_inner=4.59 cm, h= 2.0cm
Volume AluminiumFrame
AluminiumFrame.Material Aluminium
AluminiumFrame.Shape TUBS  4.59 4.981 1.0  0. 360. 
AluminiumFrame.Position 0 0 0
AluminiumFrame.Color 1
AluminiumFrame.Visibility 1
AluminiumFrame.Mother DetectorVolume

//This is the Al window on top
//the tech specs say Al top in the hole dim are R=4.981 cm, h=0.1 cm
Volume AlWindow
AlWindow.Material Aluminium 
AlWindow.Shape TUBS  0. 4.981 0.05  0. 360. 
AlWindow.Position 0 0 1.05
AlWindow.Color 1
AlWindow.Visibility 1
AlWindow.Mother DetectorVolume

// Build the teflon coating around the CsI Cylinder dim are R_outter=4.59 cm, R_inner=4.54 cm, h= 1.9cm
Volume TeflonFrame
TeflonFrame.Material Teflon
TeflonFrame.Shape TUBS  4.54 4.59 0.95  0. 360. 
TeflonFrame.Position 0 0 -0.05
TeflonFrame.Color 4
TeflonFrame.Visibility 1
TeflonFrame.Mother DetectorVolume

// Build the vacuum gap?? around the teflon around the CsI cylinder dim are R_outter=4.54 cm, R_inner=4.49 cm, h= 1.9 cm
Volume VacuumFrame
VacuumFrame.Material Vacuum
VacuumFrame.Shape TUBS  4.49 4.54 0.95 0. 360. 
VacuumFrame.Position 0 0 -0.05
VacuumFrame.Color 9
VacuumFrame.Visibility 1
VacuumFrame.Mother DetectorVolume

// Single cylinder of Scintillator CsI 
//tech specs say it R=4.49, h=1.9 cm
Volume CSICylinder
CSICylinder.Material CsI
CSICylinder.Visibility 1
CSICylinder.Color 2
CSICylinder.Shape TUBS 0. 4.49 0.95  0. 360. 
CSICylinder.Position 0. 0. -0.05
CSICylinder.Mother DetectorVolume

//This chunk is the sticky bit after the Al window
//the tech specs say Epoxy dim are R=4.59 cm, h=0.05 cm
Volume StickyWindow
StickyWindow.Material Epoxy
StickyWindow.Shape TUBS  0. 4.59 0.025 0. 360.
StickyWindow.Position 0 0 0.975
StickyWindow.Color 6
StickyWindow.Visibility 1
StickyWindow.Mother DetectorVolume

//This chunk is the teflon bit after the sticky window
//the tech specs say teflon dim are R=4.59 cm, h=0.05 cm
Volume TeflonWindow
TeflonWindow.Material Epoxy
TeflonWindow.Shape TUBS  0. 4.59 0.025 0. 360.
TeflonWindow.Position 0 0 0.925
TeflonWindow.Color 4
TeflonWindow.Visibility 1
TeflonWindow.Mother DetectorVolume

//This chunk is the Silicone rubber optical interface
//the tech specs say need this window above glass. Dim are R=4.74 cm, h=0.1 cm
Volume SiliconeWindowOne
SiliconeWindowOne.Material Silicone
SiliconeWindowOne.Shape TUBS  0. 4.74 0.05 0. 360.
SiliconeWindowOne.Position 0 0 -1.05
SiliconeWindowOne.Color 5
SiliconeWindowOne.Visibility 1
SiliconeWindowOne.Mother DetectorVolume

//This chunk is the window on bottom
//the tech specs say quartz the window is below the CsI but not in the hole. Dim are R=4.74 cm, h=0.3 cm
Volume GlassWindow
GlassWindow.Material Silica
GlassWindow.Shape TUBS  0. 4.74 0.15 0. 360.
GlassWindow.Position 0 0 -1.25
GlassWindow.Color 7
GlassWindow.Visibility 1
GlassWindow.Mother DetectorVolume

//This chunk is the Silicone rubber optical interface
//the tech specs say need this window above glass. Dim are R=4.74 cm, h=0.1 cm
Volume SiliconeWindowTwo
SiliconeWindowTwo.Material Silicone
SiliconeWindowTwo.Shape TUBS  0. 4.74 0.05 0. 360.
SiliconeWindowTwo.Position 0 0 -1.45
SiliconeWindowTwo.Color 5
SiliconeWindowTwo.Visibility 1
SiliconeWindowTwo.Mother DetectorVolume

// Build the volume to put the readouts in dim are R=4.5, h=0.22 cm
Volume ReadOutDetectorVolume
ReadOutDetectorVolume.Material Vacuum 
ReadOutDetectorVolume.Shape TUBS  0. 4.5 0.11  0. 360. 
//ReadOutDetectorVolume.Rotation 25.0 -25.0 0.0
ReadOutDetectorVolume.Position 0. 0. -1.61
ReadOutDetectorVolume.Color 1
ReadOutDetectorVolume.Visibility 1
ReadOutDetectorVolume.Mother DetectorVolume


//This chunk is the Si plane below the glass
//the tech specs say Si in the Al Frame/hole dim are  R=4.5, h=0.020 cm
//Slightly smaller than the circumfrence to avoid overlap
Volume SiPlane
SiPlane.Material Silicon
SiPlane.Shape TUBS 0. 4.5 0.01 0. 360. 
//For the nominal thickness
SiPlane.Position 0. 0. 0.1
SiPlane.Color 8
SiPlane.Visibility 1
SiPlane.Mother ReadOutDetectorVolume

//This chunk is the G10 below the Si
//the tech specs say dim are R=4.5, h=0.20 cm
Volume G10Plane
G10Plane.Material CircuitBoard
G10Plane.Shape TUBS 0. 4.5 0.1 0. 360.
G10Plane.Position 0. 0. -0.01
G10Plane.Color 8
G10Plane.Visibility 1
G10Plane.Mother ReadOutDetectorVolume

