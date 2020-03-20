import numpy as np
import healpy as hp
from BurstCube.LocSim.Spacecraft import Spacecraft


class Mission(Spacecraft):

    """This is a mission object that is a child of the BurstCube
    Spacecraft Object.  It's got some extra features like effective area
    and you can setup a specfic real world spacecraft when you initialize
    it.  This is useful for a lot of the requirement sims."""

    Missions = ('Bia', 'GBM', 'Fermi', 'HAM',
                'Nimble', 'BATSE', 'BurstCube')
    
    def __init__(self, mission,  lat=0., lon=np.radians(260.),
                 antiEarth=False, Earth=True, NSIDE=32, fov=60.,
                 ea_dir=''):

        """Detector setup for various missions.

        Parameters
        ----------
        mission : str
            string with the name of a specific mission.

        lat : float
          the latitude of the mission in degrees (default = 0).

        lon : float
          the longitude of the mission in degrees.

        Returns
        ---------
        
        """
        
        self.mission = mission
        self.antiEarth = antiEarth
        self.Earth = Earth
        self.NSIDE = NSIDE
        self.fov = fov
        self.ea_dir = ea_dir

        if self.mission not in self.Missions:
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
            self.cosindex = 0.6
            self.Aeff = 320.  # cm2

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
            self.Aeff = 132.
            self.cosindex = 0.78
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
            self.Aeff = 132  # cm2
            self.cosindex = 0.78

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
            self.cosindex = 1.0
            self.Aeff = 1500.

        if mission == 'BurstCube':
            pointings = {'01': ('0:0:0', '45:0:0'),
                         '02': ('90:0:0', '45:0:0'),
                         '03': ('180:0:0', '45:0:0'),
                         '04': ('270:0:0', '45:0:0')}
            self.Aeff = 61.
            self.cosindex = 0.6

        super().__init__(pointings, lat, lon)

    def loadAeff(self):

        """Load the full effictive areas.  Only have BurstCube and GBM now."""
        
        from pkg_resources import resource_filename
        from astropy.io import ascii as as_ascii
        
        filenames = {'BurstCube': 'BC_eff_area_curves.ecsv',
                     'GBM': 'gbm_effective_area.dat',
                     'Fermi':  'gbm_effective_area.dat'}

        ea_file = filenames[self.mission]

        if self.ea_dir == '':
            fname = resource_filename('BurstCube',
                                      'data/' + ea_file)
        else:
            fname = self.ea_dir+ea_file
        if self.mission == 'BurstCube':
            bcaeffs = as_ascii.read(fname, format='ecsv')
            w = np.where((bcaeffs['diameter'] == 90)
                         & (bcaeffs['height'] == 19))
            aeff = bcaeffs[w]
        elif (self.mission == 'GBM') or (self.mission == 'Fermi'):
            aeff = np.genfromtxt(fname, skip_header=2,
                                 names=('energy', 'aeff'))
        else:
            raise AttributeError("No such Mission")
        
        self.Aeff_full = aeff

        
    def calcExposures(self):

        """Short descrtiption of this function.

        Parameters
        ----------
        Earth : bool
            Unknown

        antiEarth : bool
            Unknown

        NSIDE : int
            Resolution of the healpix map

        Returns
        ---------
        """

        exposure_positions_hp = np.arange(hp.nside2npix(self.NSIDE))
        exposure_positions_pix = hp.pix2ang(self.NSIDE, exposure_positions_hp,
                                            lonlat=True)
        self.exposure_positions = np.vstack(exposure_positions_pix)
        self.exposures = np.array([[detector.exposure(position[0], position[1],
                                                      alt=-90.,
                                                      index=self.cosindex)
                                    for position in self.exposure_positions.T]
                                   for detector in self.detectors])

        exps = self.exposures.sum(axis=0)*self.Aeff
        self.fs = exps  # -min(gbm_exps))/max(gbm_exps)

        if self.Earth:
            vec = hp.ang2vec(180, 0, lonlat=True)
            i = hp.query_disc(self.NSIDE, vec, 67*np.pi/180.)
            self.fs[i] = 0
            self.exposures[:, i] = 0
        if self.antiEarth:
            vec = hp.ang2vec(np.degrees(self.lon)-260.+180., 0, lonlat=True)
            i = hp.query_disc(self.NSIDE, vec, 67*np.pi/180.)
            self.fs[i] = 0
            self.exposures[:, i] = 0
  
    def plotExposures(self):

        """Plots the exposures on the sky."""

        import matplotlib.pylab as plot

        npointings = len(self.pointings)
        
        plot.figure(figsize=(20, npointings))
        s = np.argsort(self.pointings.keys())
        for j in range(npointings):
            i = s[j]
            hp.mollview(self.exposures[i]/max(self.exposures[i])*self.Aeff,
                        title='Detector ',
                        sub=[np.round(npointings/3.+0.5), 3,
                             int(str(j+1))])
            # +pointings.keys()[i],\

        hp.mollview(self.fs, title='Sum of All Detectors')
        #  plot.savefig(biadir+'exposure_maps_'+str(ang)+'.png')

    @property
    def _exp_overlap(self):

        """Property to get the exposure overlap on the sky.  Ony runs once."""
        
        try:
            return self._exposures_ovlp
        except AttributeError:
            print('Calculating Overlap')
            #  evaluate detector overlap
            exposures = np.array([[detector.exposure(position[0],
                                                     position[1],
                                                     alt=-23.,
                                                     horizon=self.fov,
                                                     index=0)
                                   for position in self.exposure_positions.T]
                                  for detector in self.detectors])
            self._exposures_ovlp = exposures
            return self._exposures_ovlp
            
    @property
    def fs_det(self):

        """Property to calculate the exposures per detector in healpix."""

        fs_det = self._exp_overlap.sum(axis=0)

        if self.Earth:
            vec = hp.ang2vec(180, 0, lonlat=True)
            i = hp.query_disc(self.NSIDE, vec, 67*np.pi/180.)
            fs_det[i] = 0

        if self.antiEarth:
            vec = hp.ang2vec(0, 0, lonlat=True)
            i = hp.query_disc(self.NSIDE, vec, 67*np.pi/180.)
            fs_det[i] = 0

        return fs_det

    @property
    def fs_det_frac(self):

        ndet = int(np.max(self.fs_det))
        npix = float(len(self.fs_det))

        fracs = [float(len(np.where(self.fs_det == i)[0])/npix)
                 for i in range(ndet)]

        return fracs

    def print_fs_det_frac(self):

        fracs = self.fs_det_frac
        
        print('Fraction of sky seen by # of detectors:')
        for i, frac in enumerate(fracs):
            print(str(i)+' '+str(frac))
        
    def plot_fs_det(self):
        
        from gammaray_proposal_tools import colormap_skewed
        
        npointings = len(self.pointings)
        exposures = self._exp_overlap
        s = np.argsort(list(self.pointings.keys()))
        for j in range(npointings):
            i = s[j]
            hp.mollview(exposures[i],
                        title='Detector '+list(self.pointings.keys())[i],
                        sub=[np.round(npointings/3.+0.5), 3, int(str(j+1))])
        cmap_skewed = colormap_skewed(self.fs_det)
            
        hp.mollview(self.fs_det, title='Overlap of Detectors',
                    cmap=cmap_skewed)

    def grb_exposures(self, ra, dec):

        """Compute the exposure for a group of GRBs with coordinates ra and dec.

        Parameters
        ---------
        ra : numpy array
            Right ascension in degrees

        dec : numpy array
            Declination in degrees

        Returns
        -------
        randexposures: numpy array
            Exposures in GRB order.

        exposures : numpy array
            Exposures for each GRB in decending order.

        secondhighest : numpy array
            The second highest exposure value

        """

        ra = np.array(ra) - 180
        dec = np.array(dec)

        randexposures = np.array([[detector.exposure(r, dec[i], alt=-23.,
                                                     index=self.cosindex)
                                   for i, r in enumerate(ra)]
                                  for detector in self.detectors])

        # Order randgbmexposures into descending order
        for column in randexposures.T:
            newrand = -np.sort(-randexposures.T) 
        exposures = np.transpose(newrand)
    
        # Select the second highest exposure value. 
        # We will use this to ensure the second highest
        # exposure detector has a sig >4.5
        secondhighest = exposures[1, :]

        return randexposures, exposures, secondhighest
