##This file defines the outer aluminum housing of the cylindrical CsI detectors on BurstCube. Based on model from Oct 2018.

#Inner diameter of housing is 91.25mm, outer diamter is 99.8mm, top is 1 mm thick

#Outer shell of aluminum housing, positon here uses the same center point as the Cylinder.geo volumes.
Volume CylindricalHousing
CylindricalHousing.Material Vacuum
CylindricalHousing.Visibility 0
CylindricalHousing.Virtual true
CylindricalHousing.Shape TUBS 4.5625 4.99 2.1 0 360`

# Build the housing around the CsI Cylinder 
//Regina's comment: dim are R_outter=4.981 cm, R_inner=4.59 cm, h= 2.0cm
# From CAD R_inner = 4.5625 and R_outer = 4.99
Volume AluminiumFrame
AluminiumFrame.Material Aluminium
#AluminiumFrame.Shape TUBS  4.59 4.981 1.0  0. 360.
AluminiumFrame.Shape TUBS 4.5625 4.99 1.025 0. 360.0
AluminiumFrame.Position 0 0 0.025
AluminiumFrame.Color 4
AluminiumFrame.Visibility 1
AluminiumFrame.Mother CylindricalHousing


#This is the Al window on top
//the tech specs say Al top in the hole dim are R=4.981 cm, h=0.1 cm
# The CAD model has a rounded edge which we're not taking into account here.
Volume AlWindow
AlWindow.Material Aluminium
#AlWindow.Shape TUBS  0. 4.981 0.05  0. 360.
AlWindow.Shape TUBS 0. 4.75 0.05 0. 360.
#AlWindow.Position 0 0 1.05
AlWindow.Position 0 0 1.1
AlWindow.Color 4
AlWindow.Visibility 1
AlWindow.Mother CylindricalHousing


#The base of the aluminum housing which is parallel with the spacecraft floor, aka "flat"
Volume AlHousingFlatMount
AlHousingFlatMount.Virtual true
AlHousingFlatMount.Material Vacuum
AlHousingFlatMount.Shape BRIK 7.0 5.0 0.5
#AlHousingFlatMount.Position 0 -5. -1.6
AlHousingFlatMount.Position 0 -5.05 -1.6
AlHousingFlatMount.Rotation -45 0 0 
AlHousingFlatMount.Mother CylindricalHousing

Volume AlHousingFlatTriangle
AlHousingFlatTriangle.Material Aluminium
AlHousingFlatTriangle.Shape TRD1 4.947 0.01 0.2826 2.477
AlHousingFlatTriangle.Position 0 -1.77 0
AlHousingFlatTriangle.Rotation 90 0 0
AlHousingFlatTriangle.Color 4
AlHousingFlatTriangle.Visibility 1
AlHousingFlatTriangle.Mother AlHousingFlatMount

Volume AlHousingFlatArm
AlHousingFlatArm.Material Aluminium
AlHousingFlatArm.Shape GTRA 0.497 26.565 0 0 0.2826 1.83 1.83 0 0.2826 1.34 1.34 0

AlHousingFlatArm.Copy AlHousingFlatArm1
AlHousingFlatArm1.Position 5.37 1.85 0
AlHousingFlatArm1.Rotation 90 0 45
AlHousingFlatArm1.Color 4
AlHousingFlatArm1.Visibility 1
AlHousingFlatArm1.Mother AlHousingFlatMount

AlHousingFlatArm.Copy AlHousingFlatArm2
AlHousingFlatArm2.Position -5.37 1.85 0
AlHousingFlatArm2.Rotation -90 0 135
AlHousingFlatArm2.Color 4
AlHousingFlatArm2.Visibility 1
AlHousingFlatArm2.Mother AlHousingFlatMount


#Complicated structure beneath the cyclindiral housing 
Volume AlHousingBase
AlHousingBase.Virtual true
AlHousingBase.Material Vacuum
AlHousingBase.Shape BRIK 7.0 6.0 0.337
AlHousingBase.Position 0 1.5 -1.837
AlHousingBase.Mother CylindricalHousing

Volume AlHousingBaseLower
AlHousingBaseLower.Material Aluminium
AlHousingBaseLower.Shape GTRA 1.446 -9.87 0 0 0.337 3.8 3.8 0 0.337 2.267 2.267 0

AlHousingBaseLower.Copy AlHousingBaseLower1
AlHousingBaseLower1.Position -3.541 -3.4 0
AlHousingBaseLower1.Rotation 90 0 -54.74
AlHousingBaseLower1.Color 4
AlHousingBaseLower1.Visibility 1
AlHousingBaseLower1.Mother AlHousingBase

AlHousingBaseLower.Copy AlHousingBaseLower2
AlHousingBaseLower2.Position 3.541 -3.4 0
AlHousingBaseLower2.Rotation 90 180 54.74
AlHousingBaseLower2.Color 4
AlHousingBaseLower2.Visibility 1
AlHousingBaseLower2.Mother AlHousingBase

Volume AlHousingBaseCutout
AlHousingBaseCutout.Material Vacuum
AlHousingBaseCutout.Shape TUBS 2 4.87 0.337 0 360
AlHousingBaseCutout.Position 0 -1.5 0
AlHousingBaseCutout.Color 2
AlHousingBaseCutout.Visibility 1
AlHousingBaseCutout.Mother AlHousingBase

Volume AlHousingBaseTip
AlHousingBaseTip.Material Aluminium
AlHousingBaseTip.Shape TRD1 2.301 0.01 0.337 1.628
AlHousingBaseTip.Position 0 4.25 0
AlHousingBaseTip.Rotation -90 0 0 
AlHousingBaseTip.Color 4
AlHousingBaseTip.Mother AlHousingBase



