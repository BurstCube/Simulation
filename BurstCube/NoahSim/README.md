I've updated the simulation so now it runs lightyears faster than the initial one I submitted at the end of my internship, essentially proving I was able to do what I was paid for 3 months for in the span of a week. Whoops!  

It still retains the same capabilities, and is now actually a useful tool for scientific use!

What's left is to update the functions used to deploy the simulation, print out a few plots, and try out a couple of alternating versions to track their effectiveness. 


The method now works as follows. For any given burstcube orientation, there are 4 detectors, and due to a burst, there will be a corresponding # of counts resulting. Looking a little like this. 


index    A    B    C    D 
-----   ---  ---  ---  ---
some #  ai   bi   ci   di
some #  aj   bj   cj   dj
some #  ak   bk   ck   dk


and so on. All these numbers

 Leveraging the abilities of healpy, we know that this index corresponds to a certain pixel, and with it the sky coordinates of the burst. 


 By recreating this table but with the affected bursts via a detector with gaussian noise + some background counts, we can use a chi squared minimization routine to locate the estimated pixel # and therefore inferred localization. 


Combining this software with the MEGAlib simulations and estimations of BurstCube individual detector response, this is a powerful tool to affirm the science case of BurstCube and gradually test and compare different designs. 


For more information, please consult the readthedocs documentation, or the contained source code. 



NoahSim
=======

In here is all of Noah Kasmanoff's python based simulations of BurstCube. The simulations generate GRBs of a given strength throughout the sky, and reproduce the effect in a model of BurstCube with the desired parameters (detector tilt, background, instrument shadowing, etc.) to reconstruct the GRB, and give the user a sense of how well BurstCube performs at a certain point and/or throughout the sky. TSM plotting also available. 


To run these simulations, on your terminal enter "python runnoahsims.py". Inside runnoahsims.py the parameters are designated. For more information please refer to the documentation available. 


please email me at nkasmanoff@gmail.com for further questions/issues. 
