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
AluminiumFrame.Color 1
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
AlWindow.Color 1
AlWindow.Visibility 1
AlWindow.Mother CylindricalHousing

Volume AlMountFlatMount
AlMountFlatMount.Virtual true
AlMountFlatMount.Material Vacuum
AlMountFlatMount.Shape BRIK 5.0 5.0 1.0
AlMountFlatMount.Position 0 -6.7 -0.5
AlMountFlatMount.Rotation 45 0 0 
AlMountFlatMount.Mother CylindricalHousing

Volume AlMount
AlMount.Material Aluminium
AlMount.Shape GTRA 2.404 0 0 0 0.2826 4.808 4.808 0 0.2826 0.01 0.01 0
AlMount.Position 0 0 0
#AlMount.Rotation 290 225 70
AlMount.Rotation 0 0 0
AlMount.Color 3
AlMount.Visibility 1
AlMount.Mother AlMountFlatMount


Volume AlMountArm
AlMountArm.Material Aluminium
AlMountArm.Shape GTRA 0.497 26.565 0 0 0.2826 2.39 2.39 0 0.2826 1.89 1.89 0

AlMountArm.Copy AlMountArm1
AlMountArm1.Position 5.65 0 -3.95
AlMountArm1.Rotation 0 45 0
AlMountArm1.Color 3
AlMountArm1.Visibility 1
AlMountArm1.Mother AlMountFlatMount

AlMountArm.Copy AlMountArm2
AlMountArm2.Position -5.65 0 -3.95
AlMountArm2.Rotation 0 45 180
AlMountArm2.Color 3
AlMountArm2.Visibility 1
AlMountArm2.Mother AlMountFlatMount

Volume AlBaseMount
AlBaseMount.Material Aluminium
AlBaseMount.Shape GTRA 1.446 -9.87 0 0 0.337 3.8 3.8 0 0.337 2.267 2.267 0

AlBaseMount.Copy AlBaseMount1
AlBaseMount1.Position -3.541 -2.4 -1.837
AlBaseMount1.Rotation 90 0 -54.74
AlBaseMount1.Color 4
AlBaseMount1.Visibility 1
AlBaseMount1.Mother CylindricalHousing

AlBaseMount.Copy AlBaseMount2
AlBaseMount2.Position 3.541 -2.4 -1.837
AlBaseMount2.Rotation 90 180 54.74
AlBaseMount2.Color 4
AlBaseMount2.Visibility 1
AlBaseMount2.Mother CylindricalHousing

Volume AlBaseMountCutout
AlBaseMountCutout.Material Vacuum
AlBaseMountCutout.Shape TUBS 2 4.87 0.337 0 360
AlBaseMountCutout.Position 0 0 -1.837
AlBaseMountCutout.Color 4
AlBaseMountCutout.Visibility 1
AlBaseMountCutout.Mother CylindricalHousing



