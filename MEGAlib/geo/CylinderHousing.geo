##This file defines the outer aluminum housing of the cylindrical CsI detectors on BurstCube. Based on model from Oct 2018.

#Inner diameter of housing is 91.25mm, outer diamter is 99.8mm, top is 1 mm thick

#Outer shell of aluminum housing
Volume CylindricalHousing
CylindricalHousing.Material Vacuum
CylindricalHousing.Visibility 0
CylindricalHousing.Virtual true
CylindricalHousing.Shape TUBS 4.5625 4.99 2.1 0 360


// Build the housing around the CsI Cylinder dim are R_outter=4.981 cm, R_inner=4.59 cm, h= 2.0cm
Volume AluminiumFrame
AluminiumFrame.Material Aluminium
AluminiumFrame.Shape TUBS  4.59 4.981 1.0  0. 360.
AluminiumFrame.Position 0 0 0
AluminiumFrame.Color 1
AluminiumFrame.Visibility 1
AluminiumFrame.Mother CylindricalHousing

//This is the Al window on top
//the tech specs say Al top in the hole dim are R=4.981 cm, h=0.1 cm
Volume AlWindow
AlWindow.Material Aluminium
AlWindow.Shape TUBS  0. 4.981 0.05  0. 360.
AlWindow.Position 0 0 1.05
AlWindow.Color 1
AlWindow.Visibility 1
AlWindow.Mother CylindricalHousing


