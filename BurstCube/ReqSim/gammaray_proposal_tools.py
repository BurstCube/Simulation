import numpy as np
import matplotlib.pylab as plot
from scipy import interpolate
from BurstCube.LocSim.Detector import *
from BurstCube.LocSim.Spacecraft import Spacecraft
import healpy as hp
from pylab import cm
import matplotlib.colors as mpl_col


def load_mission(mission, lat=0., lon=np.radians(260.)):

    """Detector setup for various missions.

    Parameters
    ----------
    mission : str
            string with the name of a specific mission.

    lat : float
          the latitude of the mission in degrees.

    lon : float
          the longitude of the mission in degrees.

    Returns
    ---------
    Spacecraft : BurstCube Spacecraft Object

    """
    missions = ('Bia', 'GBM', 'Fermi', 'HAM', 'Nimble', 'BATSE', 'BurstCube')

    if mission not in missions:
        print('No such mission', mission)
        return

    if mission == 'Bia':
        pointings = {'01': ('30:0:0', '55:0:0'),
                     '02': ('90:0:0', '55:0:0'),
                     '03': ('150:0:0', '55:0:0'),
                     '04': ('210:0:0', '55:0:0'),
                     '05': ('270:0:0', '55:0:0'),
                     '06': ('330:0:0', '55:0:0'),
                     '07': ('0:0:0', '0:0:0')}
        index = 0.6
        Aeff = 320.  # cm2

    if((mission == 'GBM') or (mission == 'Fermi')):
        pointings = {'01': ('45:54:0', '20:36:0'),
                     '02': ('45:6:0', '45:18:0'),
                     '03': ('58:24:0', '90:12:0'),
                     '04': ('314:54:0', '45:12:0'),
                     '05': ('303:12:0', '90:18:0'),
                     '06': ('3:24:0', '89:48:0'),
                     '07': ('224:54:0', '20:24:0'),
                     '08': ('224:36:0', '46:12:0'),
                     '09': ('236:36:0', '90:0:0'),
                     '10': ('135:12:0', '45:36:0'),
                     '11': ('123:42:0', '90:24:0'),
                     '12': ('183:42:0', '90:18:0')}
        Aeff = 132.
        index = 0.78
        lat = np.radians(50.)
        lon = np.radians(260.)

    if ((mission == 'HAM') or (mission == 'Nimble')):
        ang = 45.
        pointings = {'01': ('60:00:00', str(ang)+':0:0'),
                     '02': ('120:00:00', str(ang)+':0:0'),
                     '03': ('180:00:00', str(ang)+':0:0'),
                     '04': ('240:00:00', str(ang)+':0:0'),
                     '05': ('300:00:00', str(ang)+':0:0'),
                     '06': ('00:00:00', str(ang)+':0:0'),
                     '07': ('00:00:00', '00:00:00')}
        Aeff = 132  # cm2
        index = 0.78

    if mission == 'BATSE':
        ang = 45
        pointings = {'01': ('0:0:0', str(ang)+':0:0'),
                     '02': ('90:0:0', str(ang)+':0:0'),
                     '03': ('180:0:0', str(ang)+':0:0'),
                     '04': ('270:0:0', str(ang)+':0:0'),
                     '05': ('0:0:0', str(ang+90)+':0:0'),
                     '06': ('90:0:0', str(ang+90)+':0:0'),
                     '07': ('180:0:0', str(ang+90)+':0:0'),
                     '08': ('270:0:0', str(ang+90)+':0:0')}
        index = 1.0
        Aeff = 1500.

    if mission == 'BurstCube':
        pointings = {'01': ('0:0:0', '45:0:0'),
                     '02': ('90:0:0', '45:0:0'),
                     '03': ('180:0:0', '45:0:0'),
                     '04': ('270:0:0', '45:0:0')}
        Aeff = 61.
        index = 0.6

    sc = Spacecraft(pointings, lat=lat, lon=lon)

    return sc, Aeff, index


def plot_exposures(pointings, Aeff_fact, index=1, lat=0., lon=np.radians(260.),
                   Earth=True, antiEarth=False, NSIDE=32, doplot=True):

    """Short descrtiption of this function.

    Parameters
    ----------
    pointings : dictionary
        Dictionary with the pointings of the detectors.

    Aeff_fact : float
        Effective Area

    index : float
        Index (not sure what this is)

    lat : float
        Latitude of the observatory in degress

    lon : float
        Longitude of the observatory in radians

    Earth : bool
        Unknown

    antiEarth : bool
        Unknown

    NSIDE : int
        Resolution of the healpix map

    doplot : bool
        Make the plots.


    Returns
    ---------
    
    sc : BurstCube.Spacecraft object.
        The observatory.

    fs : unknown
        Unknown

    exposure_positions : unknown
        Unknown

    exposures : unknown
        Unknown

    """

    npointings = len(pointings)
    sc = Spacecraft(pointings, lat=lat, lon=lon)
    exposure_positions_hp = np.arange(hp.nside2npix(NSIDE))
    exposure_positions_pix = hp.pix2ang(NSIDE, exposure_positions_hp,
                                        lonlat=True)
    exposure_positions = np.vstack(exposure_positions_pix)
    exposures = np.array([[detector.exposure(position[0], position[1],
                                             alt=-90., index=index)
                           for position in exposure_positions.T]
                          for detector in sc.detectors])

    exps = exposures.sum(axis=0)*Aeff_fact
    fs = exps  # -min(gbm_exps))/max(gbm_exps)

    if Earth:
        vec = hp.ang2vec(180, 0, lonlat=True)
        i = hp.query_disc(NSIDE, vec, 67*np.pi/180.)
        fs[i] = 0
        exposures[:, i] = 0
    if antiEarth:
        vec = hp.ang2vec(np.degrees(lon)-260.+180., 0, lonlat=True)
        i = hp.query_disc(NSIDE, vec, 67*np.pi/180.)
        fs[i] = 0
        exposures[:, i] = 0

    if doplot:
        plot.figure(figsize=(20, npointings))
        s = np.argsort(pointings.keys())
        for j in range(npointings):
            i = s[j]
            hp.mollview(exposures[i]/max(exposures[i])*Aeff_fact,
                        title='Detector ',
                        sub=[np.round(npointings/3.+0.5), 3, int(str(j+1))])
            # +pointings.keys()[i],\

        hp.mollview(fs, title='Sum of All Detectors')
#    plot.savefig(biadir+'exposure_maps_'+str(ang)+'.png')
    return sc, fs, exposure_positions, exposures


def num_detectors(sc, exposure_positions, antiEarth=False, NSIDE=32,
                  Earth=True, fov=60.):

    """Short descrtiption of this function.

    

    Parameters
    ----------
    sc : BurstCube.Spacecraft Object
        The observatory that this is being calculated for

    exposure_positions : unknown
        Unknown

    antiEarth : bool
        Unknown (default = False)

    NSIDE : int
        Resolution of the healpix map (default = 32)

    Earth : bool
        Unknown (default = True)

    fov : float
        Field of View in degrees (default = 60.)


    Returns
    ---------
    fs_det : unknown
        unknown

    """

    npointings = len(sc.pointings)
    #  evaluate detector overlap
    exposures = np.array([[detector.exposure(position[0], position[1],
                                             alt=-23., horizon=fov, index=0)
                           for position in exposure_positions.T]
                          for detector in sc.detectors])

    plot.figure(figsize=(20, npointings))
    s = np.argsort(list(sc.pointings.keys()))
    for j in range(npointings):
        i = s[j]
        hp.mollview(exposures[i],
                    title='Detector '+list(sc.pointings.keys())[i],
                    sub=[np.round(npointings/3.+0.5), 3, int(str(j+1))])
    exps = exposures.sum(axis=0)
    #  bia_fs=(exps-min(exps))/max(exps)
    fs_det = exps  # -min(gbm_exps))/max(gbm_exps)

    cmap_skewed = colormap_skewed(exps)

    if Earth:
        vec = hp.ang2vec(180, 0, lonlat=True)
        i = hp.query_disc(NSIDE, vec, 67*np.pi/180.)
        fs_det[i] = 0

    if antiEarth:
        vec = hp.ang2vec(0, 0, lonlat=True)
        i = hp.query_disc(NSIDE, vec, 67*np.pi/180.)
        fs_det[i] = 0

    hp.mollview(fs_det, title='Overlap of Detectors', cmap=cmap_skewed)

    return fs_det

def num_detectors_frac(fs_det, printResults=True):

    """Short descrtiption of this function.

   
    Parameters
    ----------
    fs_det : Unknown
        Unknown
    
    printResults : bool
        Print out the result

    Returns
    ---------
    fracs : list
        Fraction of sky seen by number of detectors

    """

    ndet = int(np.max(fs_det))
    npix = float(len(fs_det))

    fracs = [float(len(np.where(fs_det == i)[0])/npix) for i in range(ndet)]

    if printResults:
        print('Fraction of sky seen by # of detectors:')
        for i, frac in enumerate(fracs):
            print(str(i)+' '+str(frac))

    return fracs


def colormap_skewed(exps):

    """Short descrtiption of this function.

   
    Parameters
    ----------
    exps : Unknown
        Unknown
    
    Returns
    ---------
    cmap_skewed : matplotlib colorma
        Skewed colormap

    """
    
    vmin_skewed = -1.0
    vmid_skewed = 3.0
    vmax_skewed = np.max(exps)
    vstep = 1.0
    levels = np.arange(vmin_skewed, vmax_skewed+vstep, vstep)
    #  cmap = cm.get_cmap('bwr', len(levels)-1)
    deltamax = max(vmax_skewed-vmid_skewed, vmid_skewed-vmin_skewed)

    # Full range either side of vmid
    vfull = [vmid_skewed-deltamax, vmid_skewed+deltamax]
    # Levels over full value range
    # levfull = np.arange( vfull[0], vfull[1], vstep )

    ncols = len(levels) - 1  # number of colours we actually want to use

    vlo_frac = (vmin_skewed-vfull[0]) / (2.0*deltamax)  # 0 or greater
    vhi_frac = (vmax_skewed-vfull[0]) / (2.0*deltamax)  # 1 or less
    cmap_base = cm.get_cmap('bwr')  # maps the range 0-1 to colours
    cols = cmap_base(np.linspace(vlo_frac, vhi_frac, ncols))
    cmap_skewed = mpl_col.LinearSegmentedColormap.from_list('skewed',
                                                            cols, N=ncols)
    cmap_skewed.set_bad('gray')
    cmap_skewed.set_under('w')

    return cmap_skewed


def thetaphi2radec(theta, phi):

    """Converts theta and phi to ra and dec.


    Parameters
    ----------
    theta : float
        theta in radians

    phi : float
        phi in radians

    Returns
    ----------
    ra: float
        Right ascencian in degrees

    dec: float
        Declination in degrees.
    
        """
    
    dec = -np.degrees(theta-np.pi/2.)
    ra = np.degrees(np.pi*2-phi)

    return ra, dec


def random_sky(n=1):

    u=np.random.rand(n)
    v=np.random.rand(n)

    phi=2*np.pi*u
    theta=np.arccos(2*v-1.)

    ra,dec=thetaphi2radec(theta,phi)

    if len(ra)==1:
        ra=ra[0]
        dec=dec[0]

    return ra,dec

def separation(ra1,dec1,ra2,dec2):

    rra1=np.radians(ra1)
    rra2=np.radians(ra2)
    rdec1=np.radians(dec1)
    rdec2=np.radians(dec2)

#    sep=np.degrees(np.sqrt(2-2.*np.cos(rra1-rra2)-2.*np.sin(rra1)*np.sin(rra2)*(np.cos(rdec1-rdec2)-1.)))
    sep=np.degrees(np.arccos(np.sin(rdec1)*np.sin(rdec2)+np.cos(rdec1)*np.cos(rdec2)*np.cos(rra2-rra1)))
 
    return sep

## bit of useful code for interpolating in log space
def loginterpol(x,y,x1):

    f=interpolate.interp1d(np.log10(x),np.log10(y),bounds_error=False,fill_value="extrapolate",kind='linear')
    y1=10**f(np.log10(x1))

    return y1

def loginterpol2d(x,y,z,x1,y1):

    wz=np.where(z==0)[0]
    zz=z
    zz[wz]=1.
    f=interpolate.interp2d(x,y,np.log10(zz),bounds_error=False,fill_value="extrapolate",kind='linear')
    z1=10**f(x1,y1)

    return z1

#function to match GRBs in the Trigger catalog to those in the grb catalog so that we can create an array of the grbs in both
#We will use the trigger timescale found in the trigger catalog 
def match_catalogs_name(name1,name2):

    ind_dict = dict((q,e) for e,q in enumerate(name1))
    inter = set(ind_dict).intersection(name2)
    m1 = [ind_dict[element] for element in inter]
    print(np.shape(m1))
    
    ind_dict = dict((q,e) for e,q in enumerate(name2))
    inter = set(ind_dict).intersection(name1)
    m2 = [ind_dict[element] for element in inter]
    print(np.shape(m2))
    
    return m1,m2
