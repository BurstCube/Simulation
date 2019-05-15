#To have the referen≈ce point of this volume be the Cylindar housing, start with the Cylinder

Shape TUBS AluminiumCylinder
AluminiumCylinder.Parameters 4.5625 4.99 1.025 0. 360.0

#Start with trianglular base
Shape TRD1 TriangleBase
TriangleBase.Parameters 8.77 0.01 0.596 6.205
Orientation TriangleBaseOri
TriangleBaseOri.Position 0 1.35 -1.6
TriangleBaseOri.Rotation -90 0 0
Shape Union TrianglePlusCylinder
TrianglePlusCylinder.Parameters AluminiumCylinder TriangleBase TriangleBaseOri

#This is the Al window on top
# The CAD model has a rounded edge which we're not taking into account here.
Shape TUBS AlWindow
AlWindow.Parameters 0. 4.75 0.05 0. 360.
Orientation AlWindowOri
AlWindowOri.Position 0 0 1.125
Shape Union TrianglePlusCap
TrianglePlusCap.Parameters TrianglePlusCylinder AlWindow AlWindowOri

#Cut corners
Shape TRD1 TriangleCutOut
TriangleCutOut.Parameters 2.615 0.01 0.6 1.85
Orientation TriCutOutOri1
TriCutOutOri1.Position 6.18 -3.03 -1.6
TriCutOutOri1.Rotation -90 0 0
Orientation TriCutOutOri2
TriCutOutOri2.Position -6.18 -3.03 -1.6
TriCutOutOri2.Rotation -90 0 0
Shape Subtraction TriangleMinusTriCutOut1
TriangleMinusTriCutOut1.Parameters TrianglePlusCap TriangleCutOut TriCutOutOri1
Shape Subtraction TriangleMinusTriCutOut2
TriangleMinusTriCutOut2.Parameters TriangleMinusTriCutOut1 TriangleCutOut TriCutOutOri2

#Flat base
Shape TRD1 AlHousingFlatTriangle
AlHousingFlatTriangle.Parameters 4.947 0.01 0.2826 2.477
Orientation FlatBaseOri
FlatBaseOri.Position 0 -6.4 -0.23
FlatBaseOri.Rotation 45 0 0
Shape Union TriPlusFlat
TriPlusFlat.Parameters TriangleMinusTriCutOut2 AlHousingFlatTriangle FlatBaseOri


Shape BOX AlHousingFlatArm
AlHousingFlatArm.Parameters 0.497 0.2826 1.83
Orientation AlHousingFlatArmOri1
AlHousingFlatArmOri1.Position 5 -4 -2
AlHousingFlatArmOri1.Rotation 52 -30 -30
#Shape Union TrianglePlusFlatArms
#TrianglePlusFlatArms.Parameters TriPlusFlat AlHousingFlatArm AlHousingFlatArmOri1

#AlHousingFlatArm.Copy AlHousingFlatArm2
#AlHousingFlatArm2.Position -5.37 1.85 0
#AlHousingFlatArm2.Rotation 0 0 135
#AlHousingFlatArm2.Color 4
#AlHousingFlatArm2.Visibility 1
#AlHousingFlatArm2.Mother WorldVolume

Shape BOX AddSideBox
#AddSideBox.Parameters 0.176 0.587 2.98
Orientation AddSideBoxOri
AddSideBoxOri.Position 4 -4 -2
AddSideBoxOri.Rotation 54.74 0 0
Shape Union TriPlusExtra
TriPlusExtra.Parameters TriPlusFlat AddSideBox AddSideBoxOri



#Add to extra shape to triangle
Shape TRD1 TriAdd
TriAdd.Parameters 0.7 0.01 5.333 0.596
Orientation TriAddOri1
TriAddOri1.Position -3.1 3.2 -1.6
TriAddOri1.Rotation 0 180 -35.25
Orientation TriAddOri2
TriAddOri2.Position 3.1 3.2 -1.6
TriAddOri2.Rotation 0 180 35.25
Shape Union TriPlusMoreTri1
TriPlusMoreTri1.Parameters TriPlusExtra TriAdd TriAddOri1
Shape Union TriPlusMoreTri2
TriPlusMoreTri2.Parameters TriPlusMoreTri1 TriAdd TriAddOri2


#Cut out circle
Shape TUBE CircleCutOut
CircleCutOut.Parameters 0 4.875 0.6 0 360
Orientation CutOutOri
CutOutOri.Position 0 0 -1.6
CutOutOri.Rotation 0 0 0
Shape Subtraction TriangleMinusCutOut
TriangleMinusCutOut.Parameters TriPlusMoreTri2 CircleCutOut CutOutOri

#Cut out top
Shape BOX TopCutOut
TopCutOut.Parameters 1.5 0.5 1.5
Orientation TopCutOutOri
TopCutOutOri.Position 0 7.6 -1.2
TopCutOutOri.Rotation 45 0 0 
Shape Subtraction TriangleMinusTopCut
TriangleMinusTopCut.Parameters TriangleMinusCutOut TopCutOut TopCutOutOri



Volume AlHousing
AlHousing.Material Aluminium
AlHousing.Shape TriangleMinusTopCut
AlHousing.Color 4
AlHousing.Position 0 0 0 
AlHousing.Rotation 0 0 0

