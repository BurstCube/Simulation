# Intro

The ReqSim module runs simulations to develop the requirments for
BurstCube (and other missions).

To run:

 > import BurstCube.ReqSim.ReqSim as BRS
 > RecSimDict = BRS.run()
 > BRS.printRun(RecSimDict)
 > BRS.plotRun(RecSimDict)

This will run the simulation and then print the results and then plot
the results.  You can access all the data in the dictionary that the
function returns.

# To Do

* make it a class
* write more docstrings
* provide options for the print statment
* ...

