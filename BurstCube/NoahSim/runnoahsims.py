NSIDE = 16
STRENGTH = 500
BACKGROUND = 1000
TILT = 45
ALTERNATING = False
TEST = False
TALK = True
plot = True
#%matplotlib inline only a notebook feature. 

"""
Parameters
----------

NSIDE : int
	Must be a power of 2, corresponding to the number of pixels to occupy TSM (ie NSIDE = 8 => 768 pixels, etc.)

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
testcube = BurstCube(BACKGROUND,TILT,alternating =ALTERNATING)
if TALK:
    print("Initializing...")
_ = testcube.initialize #supress output, this creates the ideal response database for reference. 
if TALK: 
    print("done!")

offsets , errors = testcube.response2GRB(sim1,talk=TALK,test = TEST)


if plot:
#Only difference is the graphs are opened in the notebook, as opposed to saved. 
    from healpy import newvisufunc
    import matplotlib.pyplot as plt
    newvisufunc.mollview(offsets,min=0, max=15,unit='Localization Offset (degrees)',graticule=True,graticule_labels=True)
    if type(ALTERNATING) == int:
        plt.title('All Sky Localization Accuracy for BurstCube with Orientation ' + str(TILT) +' by '+str(ALTERNATING) +' deg' )  #should add something about design too! 
    #plt.savefig('offset'+'tilt'+str(TILT)+'s'+str(STRENGTH)+'bg'+str(BACKGROUND)+'.png')
       	plt.savefig('offset'+str(TILT)+'by'+str(ALTERNATING)+'s'+str(STRENGTH)+'bg'+str(BACKGROUND)+'.png')

    else:
        plt.title('All Sky Localization Offsets for BurstCube with Orientation ' + str(TILT) + ' deg' )  #should add something about design too! 
       	plt.savefig('offset'+str(TILT)+'s'+str(STRENGTH)+'bg'+str(BACKGROUND)+'.png')

    plt.figure()
    newvisufunc.mollview(errors,min=0, max=100,unit='Localization Error (degrees)',graticule=True,graticule_labels=True)
    
    if type(ALTERNATING) == int:
        plt.title('All Sky Localization Errors for BurstCube with Orientation ' + str(TILT) +' by '+str(ALTERNATING) +' deg' )  #should add something about design too! 
        plt.savefig('error'+str(TILT)+'by'+str(ALTERNATING)+'s'+str(STRENGTH)+'bg'+str(BACKGROUND)+'.png')

    #plt.savefig('error'+'tilt'+str(TILT)+'s'+str(STRENGTH)+'bg'+str(BACKGROUND)+'.png')
    else:
        plt.title('All Sky Localization Errors for BurstCube with Orientation ' + str(TILT) + ' deg' )
       	plt.savefig('error'+str(TILT)+'s'+str(STRENGTH)+'bg'+str(BACKGROUND)+'.png')




