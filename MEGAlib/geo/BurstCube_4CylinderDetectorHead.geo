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

Include $BURSTCUBE/Simulation/MEGAlib/geo/CalorimeterCSIProperties.det

//This is the CsI Detector
Include BurstCube_1Cylinder.geo
Include CylinderHousing.geo
Include CalorimeterCSIProperties.det



#Start a virtual volume for all parts to live within
Volume DetectorHead
DetectorHead.Material Vacuum
DetectorHead.Virtual true
DetectorHead.Visibility 0
DetectorHead.Shape BRIK 50.0 50.0 50.0


#Detector1
SingleCsI.Copy DetectorVolume_1
DetectorVolume_1 Position 5.5 5.5 0.
DetectorVolume_1.Rotation 45 0 135
DetectorVolume_1.Mother DetectorHead

CylindricalHousing.Copy DetectorHousing_1
DetectorHousing_1 Position 5.5 5.5 0.
DetectorHousing_1.Rotation 45 0 135
DetectorHousing_1.Mother DetectorHead

#ReadOutDetectorVolume.Copy ReadOutDetectorVolume_1
#ReadOutDetectorVolume_1 Position 5. 5. -1.4
#ReadOutDetectorVolume_1.Rotation 45 0 135
#ReadOutDetectorVolume_1.Mother DetectorHead



#Detector2
SingleCsI.Copy DetectorVolume_2
DetectorVolume_2 Position -5.5 5.5 0.
DetectorVolume_2.Rotation 45 0 225
DetectorVolume_2.Mother DetectorHead

CylindricalHousing.Copy DetectorHousing_2
DetectorHousing_2 Position -5.5 5.5 0.
DetectorHousing_2.Rotation 45 0 225
DetectorHousing_2.Mother DetectorHead

#ReadOutDetectorVolume.Copy ReadOutDetectorVolume_2
#ReadOutDetectorVolume_2 Position -5. 5. -1.4
#ReadOutDetectorVolume_2.Rotation 45 0 225
#ReadOutDetectorVolume_2.Mother DetectorHead



#Detector3
SingleCsI.Copy DetectorVolume_3
DetectorVolume_3 Position 5.5 -5.5 0.
DetectorVolume_3.Rotation 45 0 45
DetectorVolume_3.Mother DetectorHead

CylindricalHousing.Copy DetectorHousing_3
DetectorHousing_3 Position 5.5 -5.5 0.
DetectorHousing_3.Rotation 45 0 45
DetectorHousing_3.Mother DetectorHead

#ReadOutDetectorVolume.Copy ReadOutDetectorVolume_3
#ReadOutDetectorVolume_3 Position 5.5 -5.5 -1.4
#ReadOutDetectorVolume_3.Rotation 45 0 45
#ReadOutDetectorVolume_3.Mother DetectorHead



#Detector4
SingleCsI.Copy DetectorVolume_4
DetectorVolume_4 Position -5.5 -5.5 0.
DetectorVolume_4.Rotation 45 0 315
DetectorVolume_4.Mother DetectorHead

CylindricalHousing.Copy DetectorHousing_4
DetectorHousing_4 Position -5.5 -5.5 0.
DetectorHousing_4.Rotation 45 0 315
DetectorHousing_4.Mother DetectorHead

#ReadOutDetectorVolume.Copy ReadOutDetectorVolume_4
#ReadOutDetectorVolume_4 Position -5. -5. -1.4
#ReadOutDetectorVolume_4.Rotation 45 0 315
#ReadOutDetectorVolume_4.Mother DetectorHead


# Base Trigger
Trigger MainTrigger
MainTrigger.Veto false
MainTrigger.TriggerByDetector true
MainTrigger.Detector DCalCSI 1


