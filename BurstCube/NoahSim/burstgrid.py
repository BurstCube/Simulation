"""
This file serves effectively as a grid search, I will be trying to tune the parameters of the burstcube model, primarily
 the tilt(and whether or not it will be alternating) and use this as a means to optimize / identify the best setup 
 for localization. I'm primarily concerned with how BurstCube performs when at least one detector is capable or seeing
 the burst, so will only track this effectiveness over that segment of the sky. 
"""


import numpy as np
from NoahCube import Sky, BurstCube
from healpy import newvisufunc
import matplotlib.pyplot as plt
NSIDE = 16
STRENGTH = 500
BACKGROUND = 1000
TEST = False
TALK = False
plot = True

tilt1s = [30,35,45]
tilt2s = [30,40,45]

sim1 = Sky(NSIDE,STRENGTH)
geo_offset = []
geo_error = []
for a in tilt1s:
    for b in tilt2s:
        if a == b:
            b = False
            print('tilt ' + str(a))
        else:
        	print('tilt',a,b)
        testcube = BurstCube(BACKGROUND,a,alternating = b)
        _ = testcube.initialize #supress output for now, but it is now a property so we chilling. 
        offsets , errors = testcube.response2GRB(sim1,talk=TALK)
        im = offsets
        imerror = errors		
        offsets = offsets[0:round(.843*len(offsets))] #goes to 135 as based on skymap
        errors = errors[0:round(.843*len(errors))]
        geo_offset.append(np.mean(offsets))
        geo_error.append(np.mean(errors))
        print('avg offset: ' + str(np.mean(offsets)) + ' deg')
        print('avg error: '+ str(np.mean(errors)) + ' deg')
        if plot:
        	newvisufunc.mollview(im,min=0, max=60,unit='Localization Accurary (degrees)',graticule=True,graticule_labels=True)
        	plt.title('All Sky Localization Accuracy for BurstCube')  #should add something about design too
        	if b != False: #alternating
        		plt.savefig('offset'+str(a)+'by'+str(b)+'.png')
        	else:
        		plt.savefig('offset'+str(a)+'.png')
        	plt.figure()
        	newvisufunc.mollview(imerror,min=0, max=60,unit='Localization Error (degrees)',graticule=True,graticule_labels=True)
        	plt.title('All Sky Localization Errors for BurstCube')  #should add something about design too! 
        	if b != False: #alternating
        		plt.savefig('error'+str(a)+'by'+str(b)+'S'+str(STRENGTH)+'B'+str(BACKGROUND)+'.png')
        	else:
        		plt.savefig('error'+str(a)+'S'+str(STRENGTH)+'B'+str(BACKGROUND)+'.png')

print('best localizer: ',min(geo_offset))
print('smallest error: ', min(geo_error))

