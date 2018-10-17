"""The following python file contains the "BurstCube" and "Sky" class. 


This is the simulation framework used to emulate the results of state of the art
simulations on GRB localization, and use these results to characterize
the BurstCube spacecraft at a better cost and understanding. 

For questions/comments please contact me, Noah Kasmanoff, at
nkasmanoff@gmail.com or https://github.com/nkasmanoff


Further documentation is provided below. 

The first class is Sky, which uses the healpy module 
along with specifications by the user to fill the sky locations with a GRB source to be 
subsequently detected by the BurstCube class. 

"""
import numpy as np
#import dependencies 
from healpy import nside2npix, pix2ang


#an update to the Sky class. 
from healpy import nside2npix, pix2ang


class Sky():
    """
    Generates an array of GRB's given
    certains strength at different sky positions.
    
    Output should be an array.
    
    The number of pixels used to obtain a higher resolution is correlated to the NSIDE specified. 
    
    
    # of pixels = 12 * nside ^2, also nside has to be a power of 2, but that's besides the point. 
    """
    
    def __init__(self, NSIDE, strength):

        # depending on NSIDE, there will be anywhere
        # from 12 to infinite spots on the sky w/ GRBs
        self.Ao = strength
        self.pixels = nside2npix(NSIDE)

        # want to convert these pixels into theta phi coords.
        self.sourceangs = []
        for i in range(self.pixels):
            self.sourceangs.append(pix2ang(NSIDE, i))









"""The following cell contains the "BurstCube" class.  This is the
simulation I hope to use emulate the results of state of the art
simulations on GRB localization, and use these results to characterize
the burstcube spacecraft.

For questions/comments please contact me, Noah Kasmanoff, at
nkasmanoff@gmail.com or https://github.com/nkasmanoff

"""
from sklearn.preprocessing import normalize
from pandas import DataFrame
from numpy import rad2deg, deg2rad, pi, sqrt, add, array, average
from healpy import ang2vec, newvisufunc
from numpy import mean,ones,abs,asarray,isnan
# sometimes one import method works, sometimes another one
# does. Here's a quick fix.
try:
    from BurstCube.NoahSim import burstutils as bf
except ImportError:
    import burstutils as bf

from random import gauss
#import statistics as s


# making classes of objects, allows for different instances of
# burstcube, easy to compare.


class BurstCube():
    #enter initial parameter, such as the tilt and background of the instance. 
    #note that if you want the tilt to be alternating,
    #you need to first make this true, and then enter that value when prompted. 
    def __init__(self, background, dettilt, alternating=False):
        if alternating == False:
            self.tilt = deg2rad(dettilt)
            self.tiltA = self.tiltB = self.tiltC = self.tiltD = self.tilt
        
        else:
            self.tiltB = alternating
            self.tiltB = deg2rad(self.tiltB)
            self.tiltC = self.tiltA = deg2rad(dettilt)
            self.tiltD = self.tiltB
        
        self.zenith = [0, 0]
        self.bg = background
        self.nside = 32  #for the fitting dataframe, this is the nside to fit from. Very flexible!
    
    #these properties are each of the detectors initialized in the proper frame. (Spherical)
    
    @property
    def detA(self):
        """BurstCube is composed of 4 separate scintillators to detect and
        localize events.  In this software package, they are labelled
        A through D.

        """
        return [self.zenith[0] + self.tiltA, self.zenith[1]]
    
    @property 
    def detB(self):
        """BurstCube is composed of 4 separate scintillators to detect and localize events. 
        In this software package, they are labelled A through D. 
        """
        return [ self.zenith[0] + self.tiltB , self.zenith[1] + pi/2 ]
    @property
    def detC(self):
        """BurstCube is composed of 4 separate scintillators to detect and localize events. 
        In this software package, they are labelled A through D. 
        """
        return [ self.zenith[0] + self.tiltC , self.zenith[1] + pi ]
    @property 
    def detD(self):
        """BurstCube is composed of 4 separate scintillators to detect and localize events. 
        In this software package, they are labelled A through D. 
        """
        return [ self.zenith[0] + self.tiltD , self.zenith[1] + 3*pi/2 ]
    
    @property
    def normA(self):
        return  ang2vec(self.detA[0],self.detA[1])
    @property 
    def normB(self):
        return  ang2vec(self.detB[0],self.detB[1])
    @property
    def normC(self):
        return  ang2vec(self.detC[0],self.detC[1])
    @property 
    def normD(self):
        return  ang2vec(self.detD[0],self.detD[1])

    
    @property
    def dets(self):
        return [self.normA,self.normB,self.normC,self.normD] 

    #now that the properties of burstcube have been designed, now its time to initialize the model's localization capabilities    
    @property
    def initialize(self):  
    
    #first need to include the GRB.
       
        """
        The 'initialize' function must be run before the BurstCube instance can run the full simulation. 
        The way this action works is it quickly works out what what the relative response of each 
        detector would correspond to assuming there is no gaussian noise in each detector, in other words assuming
        an 'ideal response' at each position (assuming the detectors can even see the burst) and this 'ideal dataset' is compared the simulation to find the best fitting sky position. 
        
        Parameters
        ----------
        
        Returns
        -------
        
        self.ideal_data : dataframe
            A pandas dataframe containing the relative # of counts in each detector ideally for every sky position. 
        """
        
        GRB = Sky(self.nside,1)  #inherits GRB
            #range of values used in the fitting. 
        skypoints = len(GRB.sourceangs)   #number of GRBs you're testing
        
        ideal_responses = []
        for i in range(skypoints):  #for each part of the sky. 
            
            sourceAng = GRB.sourceangs[i]

            
            sourcexyz = ang2vec(sourceAng[0],sourceAng[1]) #cartesian position of the burst at this position
            
            """A"""
            sepA=bf.angle(sourcexyz,self.normA)  
            xA = bf.look_up_A(self.normA,sourcexyz)
    
            dtheoryA=GRB.Ao*bf.response(sepA,xA)  
                    
            """B"""
            sepB=bf.angle(sourcexyz,self.normB)
            xB = bf.look_up_B(self.normB,sourcexyz)
            dtheoryB=GRB.Ao*bf.response(sepB,xB)  

            
            """C"""
            sepC=bf.angle(sourcexyz,self.normC)
            xC =  bf.look_up_C(self.normC,sourcexyz)
            dtheoryC=GRB.Ao*bf.response(sepC,xC)  #still need to define strength, brb and gonna do that 

            """D"""
            sepD=bf.angle(sourcexyz,self.normD)
            xD = bf.look_up_D(self.normD,sourcexyz)
            dtheoryD=GRB.Ao*bf.response(sepD,xD)  #still need to define strength, brb and gonna do that 
            ideal_responses.append([dtheoryA,dtheoryB,dtheoryC,dtheoryD])
        ideal_responses = normalize(ideal_responses,axis=1)
        for i in range(len(ideal_responses)):
            #this is a quick fix for removing the normalizing below horizon. 
            if ideal_responses[i][0] == ideal_responses[i][1] == ideal_responses[i][2] == ideal_responses[i][3]:
                ideal_responses[i][0] = 100
                ideal_responses[i][1] = 100
                ideal_responses[i][2] = 100
                ideal_responses[i][3] = 100
        self.ideal_data = DataFrame([])
        self.ideal_data['A'] = ideal_responses[:,0]
        self.ideal_data['B'] = ideal_responses[:,1]
        self.ideal_data['C'] = ideal_responses[:,2]
        self.ideal_data['D'] = ideal_responses[:,3]
        
        return self.ideal_data
    

    def response2GRB(self, GRB,test=False,talk=False):  

    #first need to include the GRB.
        if talk: 
            if self.tiltB != self.tiltA:
                print("Detector Class: " + str(rad2deg(self.tiltA)) + ' by ' + str(rad2deg(self.tiltB)) + 'degrees')
            else: 
                print("Detector Class: " + str(rad2deg(self.tiltA)) + ' degrees')
 
        """
        Respond2GRB will determine the sky position of an array of GRB sources assuming some inherent background noise within 
        detectors, along with fluctuations of either Gaussian or Poissonian nature. At the moment I'm assuming Gaussian, and to build a sufficent case
        each position in the sky is tested 100 times and averaged for this average localization offset.
        
        Simply adding +1 to this minimum and identifying that value would correspond to the standard deviation or error in this set. I'll add that now. 

        Parameters
        ----------
        GRB : object
            An instance of the separately defined "GRBs" class that contains a number of evenly spaced sky positions of a given strength. 
        
        test : boolean 
            For sanity purposes, if the simulation seems to give unrealistic results, switching to test mode allows for much quicker sampling, allowing it easier to spot potential errors. 
        
        
        talk : boolean
            If desired, prints position by position results. 
        
        Returns
        ----------
        localizationerrors : array
            numpy array that contains the average localization uncertainty at each sky position. 
        
        Additionally, response2GRB will print the sky position it is currently sampling, along with the average offset of localizations at that spot. 
        
        """
        stdev = True
        skyvals = []
        skyunc = []
        if test:
            nsamples = 1
            skypoints = 1

        else:
            #range of values used in the fitting. 
            skypoints = len(GRB.sourceangs)   #number of GRBs you're testing
            nsamples = 13

        actual_responses = []
        for i in range(skypoints):  #for each grb
            
            sourceAng = GRB.sourceangs[i]
            if talk:
                print("For bursts @ " + str(rad2deg(sourceAng)))

            sourcexyz = ang2vec(sourceAng[0],sourceAng[1]) #cartesian position of the burst at this position
            loop = 0 #I'm going to want to sample each sky position more than once,
                    #here's where I define how many times that is
            loc_offsets = []
            loc_errors = []
            for i in range(nsamples): 
                """A"""
                sepA=bf.angle(sourcexyz,self.normA)  
                xA = bf.look_up_A(self.normA,sourcexyz)
    
                dtheoryA=GRB.Ao*bf.response(sepA,xA)  
                    
                countsA = dtheoryA + self.bg
                unccountsA = sqrt(countsA)
                detactualA = gauss(countsA,unccountsA)
                if detactualA-self.bg < 0:
                    detactualA = 0
                detcountsA = detactualA - self.bg
                
                """B"""
                sepB=bf.angle(sourcexyz,self.normB)
                xB = bf.look_up_B(self.normB,sourcexyz)
                dtheoryB=GRB.Ao*bf.response(sepB,xB)  
                countsB = dtheoryB + self.bg 
                unccountsB = sqrt(countsB)
                detactualB = gauss(countsB,unccountsB)  #there is a lot of noise, present, updating it now. 
                if detactualB-self.bg < 0:
                    detactualB = 0
                    
                detcountsB = detactualB - self.bg
                
            
                """C"""
                sepC=bf.angle(sourcexyz,self.normC)
                xC =  bf.look_up_C(self.normC,sourcexyz)
                dtheoryC=GRB.Ao*bf.response(sepC,xC)  #still need to define strength, brb and gonna do that 
                countsC = dtheoryC + self.bg #another artifact, incl this background effect somewhere
                unccountsC = sqrt(countsC)
                detactualC = gauss(countsC,unccountsC)  #there is a lot of noise, present, updating it now. 
                if detactualC-self.bg < 0:
                    detactualC = 0
                    
                detcountsC = detactualC - self.bg
                
                

                """D"""
                sepD=bf.angle(sourcexyz,self.normD)
                xD = bf.look_up_D(self.normD,sourcexyz)
                dtheoryD=GRB.Ao*bf.response(sepD,xD)  #still need to define strength, brb and gonna do that 
                     
                   # print("dtheory test: " + str(dtheory))
                    # this check passes too. 
                    
                countsD = dtheoryD + self.bg #another artifact, incl this background effect somewhere
                unccountsD = sqrt(countsD)
                detactualD = gauss(countsD,unccountsD)  #there is a lot of noise, present, updating it now. 
                if detactualD-self.bg < 0:
                    detactualD = 0 
                detcountsD = detactualD - self.bg
                arr = array([float(detcountsA),float(detcountsB),float(detcountsC),float(detcountsD)])
                arr = arr.reshape(1,-1)
              #  if talk:
                #    print(arr)
                normalized_arr = normalize(arr,axis=1) #converted 
            #This tab corresponds to a new sky pos being tested, will have to evaluate all of these at once maybe? 
                observed_data = DataFrame([])
                observed_data['A'] = normalized_arr[0][0]* ones(len(self.ideal_data))
                observed_data['B'] = normalized_arr[0][1]* ones(len(self.ideal_data))
                observed_data['C'] = normalized_arr[0][2]* ones(len(self.ideal_data))
                observed_data['D'] = normalized_arr[0][3]* ones(len(self.ideal_data))
        
                #SO NOW WITH THIS OBSERVED DATA, COMPARE TO IDEAL RESPONES. 
                chiterms  = (self.ideal_data - observed_data)**2 / self.ideal_data
                observed_data['chisquared'] = chiterms.sum(axis=1)
                chimin = observed_data['chisquared'].loc[observed_data['chisquared'] == min(observed_data['chisquared'])].index[0]
                recpos = pix2ang(ipix=int(chimin),nside=self.nside)
                recvec = ang2vec(recpos[0],recpos[1])
                if stdev:
                    def find_nearest(array, value):
                        array = asarray(array)
                        idx = (abs(array - value)).argmin()
                        return array[idx]

                    error_pix = find_nearest(observed_data['chisquared'].values,(min(observed_data['chisquared'])+1))
                    #print(error_pix)
                    error_ang = pix2ang(ipix=int(error_pix),nside=self.nside)
                  #  print(error_ang)  #there is an invalid value in here?
                    
                    error_vec = ang2vec(error_ang[0],error_ang[1])
                    
                    loc_error = rad2deg(bf.angle(error_vec,recvec))
                   # print(type(loc_error))
                    if isnan(loc_error):
                        loc_error = 90
                     #otherwise nan, means it was over 90 from the original so just set as 90x
                    
                loc_offset = rad2deg(bf.angle(sourcexyz,recvec))
               # print("Loc offset = " + str(locoffset) + " deg")
                
                loc_offsets.append(loc_offset)
                loc_errors.append(loc_error)
                #convert recpos into degrees sepearaiton.
                
            loc_offsets = array(loc_offsets)
            loc_errors = array(loc_errors)
           # nanmask = nanmask = np.isnan(locunc)
           # locunc = locunc[~nanmask]
            if talk:
                print("Avg offset: " + str(mean(loc_offsets)))
                print("Std. Error: " + str(mean(loc_errors)))
                print(" ")
            skyvals.append(mean(loc_offsets))
            skyunc.append(mean(loc_error))

        skyvals = array(skyvals)
        skyunc = array(skyunc)
        return skyvals,skyunc
    

            
            
