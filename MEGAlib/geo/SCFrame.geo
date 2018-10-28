//Building the Aluminium base and wall for the spacecraft housing 

//Thin plate at the bottom
Volume SCPlate
SCFrame.Material Aluminium
SCFrame.Visibility 1
SCFrame.Color 6
SCFrame.Shape BOX 18.034225 11.70559 0.14986

//Thicker plate on the bottom where things are mounted
Volume SCBase
SCBase.Material Aluminium
SCBase.Visibility 1
SCBase.Color 6
SCBase.Shape BOX 17.4752 11.3245 0.95504

//Wall dividing instrument and Actual space craft
Volume SCWall
SCWall.Material Aluminium
SCWall.Visibility 1
SCWall.Color 6
SCWall.Shape BOX 0.635 11.3245 3.725