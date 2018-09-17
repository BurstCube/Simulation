
NSIDE = 16
STRENGTH = 500
BACKGROUND = 1000
TILT = 45
ALTERNATING = False
TEST = False
TALK = False
plot = True
"""
Parameters
----------

NSIDE : int
	A power of 2, corresponding to the number of pixels to occupy TSM (ie NSIDE = 8 => 768 pixels, etc.)

STRENGTH : float
	The desired strength of the incident GRBs. 

BACKGROUND : float 
	The desired background in the detectors. 


TILT : float
	Angle in degrees to bend the detectors. Optimal range is somewhere between 30 and 45 degrees. 

ALTERNATING : bool
	Condition on whether or not you want to alternate the tilt pattern of the detectors. 

TEST : bool
	Condition on whether or not you are testing over the entire sky, or just one for testing purposes. 

TALK : bool  
	Condition on whether or not you want simulation to tell you the sky localization for every point, as it is running. 
"""
from NoahCube import Sky, BurstCube

sim1 = Sky(NSIDE,STRENGTH)

#run this file, and you immediately get

#run this file, and you immediately get
testcube = BurstCube(BACKGROUND,TILT,alternating =False)
_ = testcube.initialize #supress output for now, but it is now a property so we chilling. 


offsets , errors = testcube.response2GRB(sim1,talk=TALK)


if plot:
	from healpy import newvisufunc
	import matplotlib.pyplot as plt
	newvisufunc.mollview(offsets,min=0, max=60,unit='Localization Accurary (degrees)',graticule=True,graticule_labels=True)
	plt.title('All Sky Localization Accuracy for BurstCube')  #should add something about design too! 
	plt.savefig('offset'+'tilt'+str(TILT)+'s'+str(STRENGTH)+'bg'+str(BACKGROUND)+'.png')

	plt.figure()
	newvisufunc.mollview(errors,min=0, max=60,unit='Localization Accurary (degrees)',graticule=True,graticule_labels=True)
	plt.title('All Sky Localization Errors for BurstCube')  #should add something about design too! 
	plt.savefig('error'+'tilt'+str(TILT)+'s'+str(STRENGTH)+'bg'+str(BACKGROUND)+'.png')


#