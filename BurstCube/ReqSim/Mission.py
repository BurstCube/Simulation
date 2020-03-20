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

    
    def __init__(self, mission, lat=0., lon=np.radians(260.), ea_dir=''):

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
        
    def calcExposures(self, Earth=True, antiEarth=False, NSIDE=32):

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

        exposure_positions_hp = np.arange(hp.nside2npix(NSIDE))
        exposure_positions_pix = hp.pix2ang(NSIDE, exposure_positions_hp,
                                            lonlat=True)
        self.exposure_positions = np.vstack(exposure_positions_pix)
        self.exposures = np.array([[detector.exposure(position[0], position[1],
                                                      alt=-90.,
                                                      index=self.cosindex)
                                    for position in self.exposure_positions.T]
                                   for detector in self.detectors])

        exps = self.exposures.sum(axis=0)*self.Aeff
        self.fs = exps  # -min(gbm_exps))/max(gbm_exps)

        if Earth:
            vec = hp.ang2vec(180, 0, lonlat=True)
            i = hp.query_disc(NSIDE, vec, 67*np.pi/180.)
            self.fs[i] = 0
            self.exposures[:, i] = 0
        if antiEarth:
            vec = hp.ang2vec(np.degrees(self.lon)-260.+180., 0, lonlat=True)
            i = hp.query_disc(NSIDE, vec, 67*np.pi/180.)
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
    
