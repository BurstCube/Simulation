import numpy as np
import math as mth
import random as rand
import healpy as hp


def length(v):
    """
    Finds the length of a vector
    
    Parameters
    ----------
    
    v : array
        numpy array representative of the vector you want to find the magnitude of. 
    
    Returns
    -------
    
    magv : float
        magnitude of v.
    """
    magv = mth.sqrt(np.dot(v, v))
    return magv

def angle(v1, v2):
    """"
    Finds the angle between 2 vectors
    
    Parameters
    ----------
    
    v1 : array
    v2 : array
        The arrays representing the vectors who's angle is to be calculated.
        
    Returns
    -------
    
    ang : float
        Angle between the 2 vectors. 
        
    """

    ang = np.arccos(np.dot(v1, v2) / (length(v1) * length(v2)))
    return ang



#Fuck around w this one. 

def look_up_A(detnorm,source,array=False):
    """The look up table for detector A. 
    Currently for all these functions the coordinates are relative to the top of the spacecraft,
    not indivudial detectors. To tranform just rotate by this specific detnorm. 
    
    Parameters
    ----------   
    detnorm : array
        The vector normal to detector A. 
    source : array
        The vector pointing to where in the sky the GRB came from. 
    
    
    Returns
    -------
    
    x : float
        The exponent of dependence for the detector's response.
    """
    if array:
        ang = findAngles(detnorm,source)   

    if not array:
        ang = angle(detnorm,source)

    sourceang = hp.vec2ang(source)
    sourcetheta = sourceang[0]
    sourcephi = sourceang[1]    #convert to degrees for now, not a big dealio or anything yet. 
    sourcetheta = np.around(np.rad2deg(sourcetheta))   #This needs to be able to take in an array and produce corresponding R's. 
    sourcephi = np.around(np.rad2deg(sourcephi))
    X = np.arange(0, 180, 1)  #full sky now. 
    Y = np.arange(0, 360, 1)
    X, Y = np.meshgrid(X, Y)
    R = 0.76*np.ones(shape=np.shape(X))

    
    
    if not array:
        if ang> np.pi/2:
            x = 0 
        else:
            mask1 = X == sourcetheta
            mask2 = Y == sourcephi
    
            x = R[mask1 & mask2]
            

    else:

        
        x = []
        
        for i in range(len(source)):
            
            sourceang = hp.vec2ang(source[i])
            
            mask1 = X == np.around(np.rad2deg(sourceang[0]))  #theta mask
            mask2 = Y == np.around(np.rad2deg(sourceang[1])) #phi mask
        
            x.append(R[mask1 & mask2])
            
    return x






def look_up_B(detnorm,source,array=False):
    """The look up table for detector B. 
    Currently for all these functions the coordinates are relative to the top of the spacecraft,
    not indivudial detectors. To tranform just rotate by this specific detnorm. 
    
    Parameters
    ----------   
    detnorm : array
        The vector normal to detector B. 
    source : array
        The vector pointing to where in the sky the GRB came from. 
    
    
    Returns
    -------
    
    x : float
        The exponent of dependence for the detector's response.
    """
    if array:
        #for fitting purposes, creates the entire lookup table all at once. Unfortuntaley I only know how to do this by putting them in a loop as done below, which is time costly. 
        ang = findAngles(detnorm,source)   

    if not array:
        ang = angle(detnorm,source)
    sourceang = hp.vec2ang(source)
    sourcetheta = sourceang[0]
    sourcephi = sourceang[1]    #convert to degrees for now, not a big dealio or anything yet. 
    sourcetheta = np.around(np.rad2deg(sourcetheta))   #This needs to be able to take in an array and produce corresponding R's. 
    sourcephi = np.round(np.rad2deg(sourcephi))
    X = np.arange(0, 180, 1)  #full sky now. 
    Y = np.arange(0, 360, 1)
    X, Y = np.meshgrid(X, Y)
    #creates meshgrid for theta phi, and masks the source's position to get response exponent. 
    
    R = 0.76*np.ones(shape=np.shape(X))
    
    
    if not array:
        if ang> np.pi/2:
            x = 0 
        else:
            mask1 = X == sourcetheta
            mask2 = Y == sourcephi
    
            x = R[mask1 & mask2]
            

    else:
        x = []
        
        for i in range(len(source)):
            
            sourceang = hp.vec2ang(source[i])
            
            mask1 = X == np.around(np.rad2deg(sourceang[0]))  #theta mask
            mask2 = Y == np.around(np.rad2deg(sourceang[1])) #phi mask
        
            x.append(R[mask1 & mask2])
            
    return x












def look_up_C(detnorm,source,array=False):
    """The look up table for detector C. 
    
    Parameters
    ----------   
    detnorm : array
        The vector normal to detector C. 
    source : array
        The vector pointing to where in the sky the GRB came from. 
    
    
    Returns
    -------
    
    x : float
        The exponent of dependence for the detector's response.

    Example:

    Let's say for this detector, past 30 degrees and for azimuths of
    60 - 180, it's blocked. This is what it would look like:

    R = 0.76*np.ones(shape=np.shape(X))

     R[30:,60:180] = 0

    """
    if array:
        ang = findAngles(detnorm,source)   

    if not array:
        ang = angle(detnorm,source)
    sourceang = hp.vec2ang(source)
    sourcetheta = sourceang[0]
    sourcephi = sourceang[1]
    #convert to degrees for now, not a big dealio or anything yet. 
    sourcetheta = np.around(np.rad2deg(sourcetheta))   #This needs to be able to take in an array and produce corresponding R's. 
    sourcephi = np.around(np.rad2deg(sourcephi))
    X = np.arange(0, 180, 1)  #full sky now. 
    Y = np.arange(0, 360, 1)
    X, Y = np.meshgrid(X, Y)
    R = 0.76*np.ones(shape=np.shape(X))  #response function
    
    
    if not array:
        if ang> np.pi/2:
            x = 0 
        else:
            mask1 = X == sourcetheta
            mask2 = Y == sourcephi
    
            x = R[mask1 & mask2]
            

    else:
        
        x = []
        
        
        for i in range(len(source)):
            
            sourceang = hp.vec2ang(source[i])
            
            mask1 = X == np.around(np.rad2deg(sourceang[0]))  #theta mask
            mask2 = Y == np.around(np.rad2deg(sourceang[1])) #phi mask
        
            x.append(R[mask1 & mask2])
            
    return x



def look_up_D(detnorm,source,array=False):
    """The look up table for detector D. 
    
    Parameters
    ----------   
    detnorm : array
        The vector normal to detector D. 
    source : array
        The vector pointing to where in the sky the GRB came from. 
    
    
    Returns
    -------
    
    x : float
        The exponent of dependence for the detector's response.
    """
    if array:
        ang = findAngles(detnorm,source)   

    if not array:
        ang = angle(detnorm,source)
        
    sourceang = hp.vec2ang(source)
    sourcetheta = sourceang[0]
    sourcephi = sourceang[1]
    #convert to degrees for now, not a big dealio or anything yet. 
    sourcetheta = np.around(np.rad2deg(sourcetheta))   #This needs to be able to take in an array and produce corresponding R's. 
    sourcephi = np.around(np.rad2deg(sourcephi))
    X = np.arange(0, 180, 1)  #full sky now. 
    Y = np.arange(0, 360, 1)
    X, Y = np.meshgrid(X, Y)
    R = 0.76*np.ones(shape=np.shape(X))
    
    
    if not array:
        if ang> np.pi/2:
            x = 0 
        else:
            mask1 = X == sourcetheta
            mask2 = Y == sourcephi
    
            x = R[mask1 & mask2]
            

    else:
        x = []
        
        for i in range(len(source)):
            
            sourceang = hp.vec2ang(source[i])
            
            mask1 = X == np.around(np.rad2deg(sourceang[0]))  #theta mask
            mask2 = Y == np.around(np.rad2deg(sourceang[1])) #phi mask
        
            x.append(R[mask1 & mask2])
            
    return x







def response(A,x):
    """Meant to imitate the actual response of a scintillator.
    Inputs 2 vectors, and responds with a cos^x dependence.
    
    Parameters
    -----------
    A : float
        The angular separation in radians between the normal vector of the
        detector, and the position in the sky of the simulated GRB.
    
    x : float
        The dependence

    Returns
    -------
    R : float
        The response function of how the scintillator will respond to a source
        at angle A.

    """
    #meant to imitate the response of the detectors for effective area vs. angle, found to be around .77
 #   print(length(A),length(B))
#if cosine is negative, 
    #Maybe include the pi/2 thing here. 
    
    R = pow(abs(np.cos(A)),x)
    #How I fix the angle stuff now. 
    mask = A > np.pi/2
    return R
