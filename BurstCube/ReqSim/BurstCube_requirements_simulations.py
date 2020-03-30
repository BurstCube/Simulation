import numpy as np
import BurstCube.ReqSim.grb_catalogs as grb_catalogs
#  from BurstCube.LocSim.Detector import *
#  from BurstCube.LocSim.Spacecraft import *
#  from gammaray_proposal_tools import *
from BurstCube.ReqSim.gammaray_proposal_tools import loginterpol,\
    random_sky, load_GBM_catalogs
from BurstCube.ReqSim.Mission import Mission


def getSGRBs(ea_dir=''):

    """Loads the GBM catalog and pulls out the short GRBs. Get shorty!

    Parameters
    ----------
    Please press the tab key twice.

    Returns
    --------
    sgbm : Unknown
        Short GRBs from the GBM catalog.

    """

    trig, gbm = load_GBM_catalogs(ea_dir=ea_dir)
    s = np.where(gbm['T90'] <= 2.0)[0]
    sgbm = gbm[s]
    return sgbm


def init(ea_dir='', nsims=10000):

    burstcube = Mission('BurstCube', ea_dir=ea_dir)
    fermi = Mission('Fermi', ea_dir=ea_dir)
    burstcube.loadAeff()
    fermi.loadAeff()

    # Aeff on same energy points
    eng = np.logspace(np.log10(50), np.log10(300), 100)
    bcaeff = loginterpol(burstcube.Aeff_full['keV'],
                         burstcube.Aeff_full['aeff'], eng)
    gbmaeff = loginterpol(fermi.Aeff_full['energy'],
                          fermi.Aeff_full['aeff'], eng)

    ra, dec = random_sky(nsims)
    randbcexposures, bcexposures, secondhighestbc =\
        burstcube.grb_exposures(ra, dec)
    randgbmexposures, gbmexposures, secondhighestgbm = \
        fermi.grb_exposures(ra, dec)
    
    return bcaeff, gbmaeff, secondhighestbc, secondhighestgbm, eng


def run(ea_dir='', nsims=10000, minflux=0.5, interval=1.0, bgrate=300.):

    """Run the full simulation to get the number of GRBs BurstCube will detect.

    Parameters
    ----------
    dir : string
        Location of the effective area curves and catalogs.  Defaults to the 
        package data directory.

    nsims : int
        Number of simulations to run (defualt 10000)

    minflux : float
        Unknown (dfault 0.5)

    interval : float
        The interval in seconds (default 1.0)

    bgrate : float
        Background rate in cts/s over 50 - 300 keV (default 300)

        """

    RecSimDict = {}
    
    bcaeff, gbmaeff, secondhighestbc, secondhighestgbm, eng = init(ea_dir,
                                                                   nsims)

    sgbm = getSGRBs(ea_dir=ea_dir)
    print("Number of short GRBs detected by GBM: " + str(len(sgbm)))
    
    gbmflux2counts, bcflux2counts, realpf = grb_spectra(sgbm, gbmaeff,
                                                        bcaeff, eng)

    pf = logNlogS(minflux=minflux, nsims=nsims)
    
    r = np.array(np.round(np.random.rand(nsims)*(len(realpf)-1)).astype('int'))

    simgbmcr = pf*gbmflux2counts[r]
    simbccr = pf*bcflux2counts[r]
    simgbmpfsample = pf
    simbcpfsample = pf

    pf = simgbmpfsample

    detectbc, detectgbm = calcSignificance(simbccr, simgbmcr, secondhighestbc,
                                           secondhighestgbm, bcaeff, gbmaeff,
                                           nsims, bgrate, pinterval=1.)

    ratiobc = detectionFrac(detectbc)
    ratiogbm = detectionFrac(detectgbm)
    print(ratiogbm)
    print(ratiobc)

    print('fraction of GBM sGRBs BC will detect = %0.2f' % (ratiobc/ratiogbm))
    #  number of bursts BurstCube will see a year
    bcbursts = numberSeen(ratiobc, ratiogbm)
    print('bc rate = %.2f' % bcbursts+' sGRBs/yr')

    #  Duty Cycle to detect 20 sGRBs/yr
    gbmduty = 0.85
    duty = 20./(bcbursts/gbmduty)
    print("duty cycle to detect 20 sGRBs/yr = %.2f" % duty)
    duty = 10./(bcbursts/gbmduty)
    print("duty cycle to detect 10 sGRBs/yr = %.2f" % duty)

    #  Creating plot of peak flux versus counts for real and simulated GBM
    # w = np.where(pf > 0)[0]
    wg = np.where(simgbmcr*detectgbm > 0.)[0]
    wbc = np.where(simbccr*detectbc > 0.)[0] 
    # Min sensitivity to detect 10 per year
    nbursts10 = bcbursts-10.
    nbursts20 = bcbursts-20.
    so = np.argsort(simbcpfsample[wbc])
    #  gso = np.argsort(simgbmpfsample[wg])
    c = np.cumsum(np.ones(len(wbc)))/len(wbc)*bcbursts
    fluxlim10 = loginterpol(c, simbcpfsample[wbc[so]], nbursts10)
    fluxlim20 = loginterpol(c, simbcpfsample[wbc[so]], nbursts20)

    print("flux limit to detect 10 sGRBs/yr = %.2f" % fluxlim10 + ' ph/cm2/s')
    print("flux limit to detect 20 sGRBs/yr = %.2f" % fluxlim20+' ph/cm2/s')
    print('expected minimum flux = '+"%.2f" %
          min(simbcpfsample[wbc[so]])+' ph/cm2/s')
    print('expected maximum flux = '+"%.2f" %
          max(simbcpfsample[wbc[so]])+' ph/cm2/s')
    print('expected 5% maximum flux = '+"%.2f" %
          simbcpfsample[wbc[so[int(0.05*len(so))]]]+' ph/cm2/s')
    print('expected 10% maximum flux = '+"%.2f" %
          simbcpfsample[wbc[so[int(0.1*len(so))]]]+' ph/cm2/s')
    print('expected 90% maximum flux = '+"%.2f" %
          simbcpfsample[wbc[so[int(0.9*len(so))]]]+' ph/cm2/s')
    print('expected 95% maximum flux = '+"%.2f" %
          simbcpfsample[wbc[so[int(0.95*len(so))]]]+' ph/cm2/s')

    #  FoV - adjusted exposure alt until total reached 20
    #  BCFoVrad = 90-0.  # deg radius
    #  BCFoV = (1-np.cos(np.radians(BCFoVrad)))/2.*4.*np.pi
    #  print("FoV for "+"%.1f" % BCFoV+' ster')

    #  max distance of GW170817
    mpc2cm = 3.086e24
    fgw = 3.7  # ph/cm2/s
    fmax = min(simgbmpfsample[wg])
    dgw = 42.9*mpc2cm
    dmax = np.sqrt(fgw*dgw**2/fmax)
    f = 80.*mpc2cm/dmax
    print("%.2f" % (dmax/mpc2cm*f)+' Mpc - distance GBM for GW170817')

    fmax = min(simbcpfsample[wbc])
    dmax = np.sqrt(fgw*dgw**2/fmax)
    print("%.2f" % (dmax/mpc2cm*f)+' Mpc - distance BC for GW170817')

    #  mission lifetime to detect 10 sGRBs
    print("Mission Duration to detect 10 sGRBs = " + "%.1f" %
          (10./bcbursts*12.)+' months')

    RecSimDict["realpf"] = realpf
    RecSimDict["wg"] = wg
    RecSimDict["wbc"] = wbc
    RecSimDict["nbursts10"] = nbursts10
    RecSimDict["nbursts20"] = nbursts20
    RecSimDict["so"] = so
    RecSimDict["c"] = c
    RecSimDict["fluxlim10"] = fluxlim10
    RecSimDict["fluxlim20"] = fluxlim20
    RecSimDict["simgbmcr"] = simbccr
    RecSimDict["simbccr"] = simbccr
    RecSimDict["simgbmpfsample"] = simgbmpfsample
    RecSimDict["simbcpfsample"] = simbcpfsample
    
    return RecSimDict
    
    #  return realgbmflux,simgbmpfsample

    
def plotRun(RecSimDict):

    import matplotlib.pylab as plot

    realgbmflux = RecSimDict["realpf"]
    simgbmcr = RecSimDict["simgbmcr"]
    simbccr = RecSimDict["simbccr"]
    wg = RecSimDict["wg"]
    wbc = RecSimDict["wbc"]
    simgbmpfsample = RecSimDict["simgbmpfsample"]
    simbcpfsample = RecSimDict["simbcpfsample"]
    so = RecSimDict["so"]
    c = RecSimDict["c"]
    fluxlim10 = RecSimDict["fluxlim10"]
    fluxlim20 = RecSimDict["fluxlim20"]
    nbursts10 = RecSimDict["nbursts10"]
    nbursts20 = RecSimDict["nbursts20"]
    
    wreal = np.where(realgbmflux > 0)[0]

    plot.subplot(2, 2, 1)
    plot.hist(simgbmcr[wg], label='GBM',
              bins=np.logspace(1, 6, 40), alpha=0.7, color='blue')
    plot.hist(simbccr[wbc], label='BurstCube',
              bins=np.logspace(1, 6, 40), alpha=0.7, color='green')
    plot.xlabel('Count Rate (50-300 keV; cts/s)')
    plot.xscale('log')
    plot.yscale('log')
    plot.xlim([10, 5e4])
    plot.ylabel('N Simulated  sGRBs')

    plot.legend()
    plot.subplot(2, 2, 2)
    plot.hist(simgbmpfsample, label='Simulated total',
              bins=np.logspace(-1, 4, 40), alpha=1.0, color='C3')
    plot.hist(realgbmflux[wreal], label='real GBM',
              bins=np.logspace(-1, 4, 40), color='orange', alpha=0.7)
    #  this is the simulated GBM
    plot.hist(simgbmpfsample[wg], label='GBM',
              bins=np.logspace(-1, 4, 40), alpha=0.5, color='blue')
    plot.hist(simbcpfsample[wbc], label='BC',
              bins=np.logspace(-1, 4, 40), alpha=0.5, color='green')
    plot.xlabel('Peak Flux (50-300 keV; ph/cm2/s)')
    #  plot.hist(flux[w],label='BC',bins=np.logspace(-1,2,40),alpha=0.7,color='red')
    plot.xscale('log')
    plot.yscale('log')
    plot.xlim([.1, 300])
    plot.legend()
    plot.ylabel('N Simulated  sGRBs')

    # plot.show()

    plot.subplot(2, 2, 3)
    plot.plot(simbcpfsample[wbc[so]], c)
    plot.xlabel(r'BurstCube 50-300 keV Peak Flux (ph cm$^{-2}$ s$^{-1}$)')
    plot.ylabel('Cumulative Number')
    plot.xscale('log')
    
    plot.plot([fluxlim10, fluxlim10], [nbursts10, nbursts10],
              marker='*', label='Limit for 10 sGRBs')
    plot.plot([fluxlim20, fluxlim20], [nbursts20, nbursts20],
              marker='*', label='Limit for 20 sGRBs')
    plot.xlim([1, 100])

    plot.legend()
    plot.show()

    
def logNlogS(minflux=0.5, nsims=10000):

    # 1 sec 50-300 keV peak flux ph/cm2/s
    # time = interval  # 1.0#0.064 # s
    f = np.logspace(np.log10(minflux), 2.2, 50)
    p = f**-0.9  # 1.5 # comes from fitting GBM sGRB logN-log peak flux
    pnorm = p/np.sum(p)
    r = np.random.choice(f, p=pnorm, size=nsims)
    
    # bg_gbm=bgrate*time
    # scaling from GBM average background rate
    # bg_bc=bgrate*np.max(aeff_bc)/np.max(aeff_gbm)*time
    
    # src_bc = r*np.max(aeff_bc)*time
    # src_gbm = r*np.max(aeff_gbm)*time
    
    # simgbmpfsample = np.array(r)
    # simgbmcr = np.array(src_gbm/time)
    # simbcpfsample = np.array(r)
    # simbccr = np.array(src_bc/time)
    
    return r  # simgbmcr,simbccr,simgbmpfsample,simbcpfsample


def grb_spectra(gbmbursts, gbmaeff, bcaeff, eng):

    """Integrating the best fit spectrum for each GRB in the energy range
       of 50-300 keV to get max. observed photon flux.  Doing the same
       but also folding in the effective area in order to get count
       rate.

       This will give us the photon flux in units of ph/cm^2/s.

    Parameters
    ----------
    gbmbursts : astropy.io.fits.fitsrec.FITS_rec
        Short bursts seen by GBM

    gbmaeff : numpy array
        GBM effective area

    bcaeff : numpy array
        BurstCbue effective area

    eng : numpy array
        Energy range in keV
    
    Returns
    -----------
    gbmflux2counts : unknown
        unknown

    bcflux2counts : unknown
        unknown

    realpf : unknown
        unknown
    """

    mo = gbmbursts['PFLX_BEST_FITTING_MODEL']
    pf = np.zeros(len(mo))
    gbmcr = np.zeros(len(mo))
    bccr = np.zeros(len(mo))
    pflux_interval = np.zeros(len(mo))
    realpf = np.zeros(len(mo))

    for i, grb in enumerate(gbmbursts):
        # this should give us an array of the maximum
        # observed photon flux for GBM
        if mo[i] == 'PFLX_PLAW':
            gbmcr[i] = np.trapz(grb['PFLX_PLAW_AMPL'] *
                                grb_catalogs.pl(eng,
                                                grb['PFLX_PLAW_INDEX']) *
                                gbmaeff, eng)
            pf[i] = np.trapz(grb['PFLX_PLAW_AMPL'] *
                             grb_catalogs.pl(eng,
                                             grb['PFLX_PLAW_INDEX']), eng)
            bccr[i] = np.trapz(grb['PFLX_PLAW_AMPL'] *
                               grb_catalogs.pl(eng,
                                               grb['PFLX_PLAW_INDEX']) *
                               bcaeff, eng)
            realpf[i] = grb['PFLX_PLAW_PHTFLUXB']

        if mo[i] == 'PFLX_COMP':
            gbmcr[i] = np.trapz(grb['PFLX_COMP_AMPL'] *
                                grb_catalogs.comp(eng, grb['PFLX_COMP_INDEX'],
                                                  grb['PFLX_COMP_EPEAK']) *
                                gbmaeff, eng)
            pf[i] = np.trapz(grb['PFLX_COMP_AMPL'] *
                             grb_catalogs.comp(eng, grb['PFLX_COMP_INDEX'],
                                               grb['PFLX_COMP_EPEAK']), eng)
            bccr[i] = np.trapz(grb['PFLX_COMP_AMPL'] *
                               grb_catalogs.comp(eng, grb['PFLX_COMP_INDEX'],
                                                 grb['PFLX_COMP_EPEAK']) *
                               bcaeff, eng)
            realpf[i] = grb['PFLX_COMP_PHTFLUXB']

        if mo[i] == 'PFLX_BAND':
            gbmcr[i] = np.trapz(grb['PFLX_BAND_AMPL'] *
                                grb_catalogs.band(eng, grb['PFLX_BAND_ALPHA'],
                                                  grb['PFLX_BAND_EPEAK'],
                                                  grb['PFLX_BAND_BETA']) *
                                gbmaeff, eng)
            pf[i] = np.trapz(grb['PFLX_BAND_AMPL'] *
                             grb_catalogs.band(eng, grb['PFLX_BAND_ALPHA'],
                                               grb['PFLX_BAND_EPEAK'],
                                               grb['PFLX_BAND_BETA']), eng)
            bccr[i] = np.trapz(grb['PFLX_BAND_AMPL'] *
                               grb_catalogs.band(eng, grb['PFLX_BAND_ALPHA'],
                                                 grb['PFLX_BAND_EPEAK'],
                                                 grb['PFLX_BAND_BETA']) *
                               bcaeff, eng)
            realpf[i] = grb['PFLX_BAND_PHTFLUXB']

        if mo[i] == 'PFLX_SBPL':
            gbmcr[i] = np.trapz(grb['PFLX_SBPL_AMPL'] *
                                grb_catalogs.sbpl(eng, grb['PFLX_SBPL_INDX1'],
                                                  grb['PFLX_SBPL_BRKEN'],
                                                  grb['PFLX_SBPL_INDX2']) *
                                gbmaeff, eng)
            pf[i] = np.trapz(grb['PFLX_SBPL_AMPL'] *
                             grb_catalogs.sbpl(eng,
                                               grb['PFLX_SBPL_INDX1'],
                                               grb['PFLX_SBPL_BRKEN'],
                                               grb['PFLX_SBPL_INDX2']), eng)
            bccr[i] = np.trapz(grb['PFLX_SBPL_AMPL'] *
                               grb_catalogs.sbpl(eng,
                                                 grb['PFLX_SBPL_INDX1'],
                                                 grb['PFLX_SBPL_BRKEN'],
                                                 grb['PFLX_SBPL_INDX2']) *
                               bcaeff, eng)
            realpf[i] = grb['PFLX_SBPL_PHTFLUXB']

        pflux_interval[i] = grb['PFLX_SPECTRUM_STOP'] -\
            grb['PFLX_SPECTRUM_START']

    # flux = gbmbursts['FLUX_BATSE_1024']

    gbmflux2counts = np.divide(gbmcr, pf)
    bcflux2counts = np.divide(bccr, pf)
    # fluxwrong=flux/pf#*pflux_interval
    # r = np.array(np.round(np.random.rand(nsims)*(len(mo)-1)).astype('int'))
    # simgbmcr = gbmcr[r]*interval #*fluxwrong[r]#*pflux_interval[r]
    # simbccr = bccr[r]*interval #*fluxwrong[r]#*pflux_interval[r]
    # simpf = pf[r]*interval #*fluxwrong[r]#*pflux_interval[r]
    # pinterval = pflux_interval[r]
    # realflux = flux[r]

    return gbmflux2counts, bcflux2counts, realpf
    # simgbmcr,simbccr,simpf,simpf,realpf,pinterval

    
def calcSignificance(simbccr, simgbmcr, secondhighestbc, secondhighestgbm,
                     bcaeff, gbmaeff, nsims=10000, bgrate=300., pinterval=1.):
    
    """Calculates the significance of bursts by looking at the counts over
    background in some interval.  If the significance is over 4.5 sigma
    then it is returned.

    Parameters
    ----------
    simbccr :

    simgbmcr : 

    secondhighestbc : 

    secondhighestgbm : 

    bcaeff : 

    gbmaeff : 

    nsims : int

    bgrate : float

    pinterval : float

    Retruns 
    -----------

    detectbc : 

    detectgbm : 

    """

    # Solve for the number of detected counts
    # which will equal our source photons
    sourcegbm = simgbmcr*secondhighestgbm*pinterval
    sourcebc = simbccr*secondhighestbc*pinterval
    #  randomize background rate around typical
    # background of 300 cts/s (50-300 keV, GBM)
    bckgrd = np.random.poisson(bgrate, nsims)
    scaledgbmbckgrd = bckgrd*pinterval
    scaledbcbckgrd = bckgrd*np.median(bcaeff/gbmaeff)*pinterval
    #  creating an array of zeros that I can manipulate
    # to create an array of detected GRBs
    detectgbm = np.zeros(len(sourcegbm))
    detectbc = np.zeros(len(sourcebc))

    #  calculate the significance of the second highest
    # exposure detector. If the significance is greater
    # than 4.5 sigma than the burst is detectable.
    for u in range(len(sourcegbm)):
        if sourcegbm[u] > 0:
            sig = sourcegbm[u] / (np.sqrt(sourcegbm[u] +
                                          scaledgbmbckgrd[u]))
            if sig > 4.5:
                detectgbm[u] = 1.0
            else:
                detectgbm[u] = 0.0

    for j in range(len(sourcebc)):
        if sourcebc[j] > 0:
            sig = sourcebc[j] / (np.sqrt(sourcebc[j] + scaledbcbckgrd[j]))
            if sig > 4.5:
                detectbc[j] = 1.0
            else:
                detectbc[j] = 0.0
        else:
            sig = 0

    return detectbc, detectgbm


def detectionFrac(detect):

    """Calculates the fraction of detections by looking at an array of 1
    or 0 and seeing which ones are 1.

    Parameters
    ----------
    detect : numpy.ndarray
        An array of 1 or 0 that shows detections

    Returns 
    ----------
    ratio : float
        The fraciton of detect that is 1.

    """
    
    if type(detect) != np.ndarray:
        raise TypeError("Must be numpy ndarray")

    det = np.where(detect == 1)[0]
    ratio = float(len(det)) / float(len(detect))

    return(ratio)


def numberSeen(ratiobc, ratiogbm):

    return ratiobc/ratiogbm * 40.

