import numpy as np


def test_load_mission():

    """Test the load_mission function.  For each mission in the list it
    checks that the effective area is correct, checks that the number of
    detectors match and checks that the indices match the expectation.
    This will not know if a new mission is adeed.  Does not check the
    detector pointings.

    """
    
    from BurstCube.ReqSim.gammaray_proposal_tools import load_mission

    missions = ('Bia', 'GBM', 'Fermi', 'HAM', 'Nimble', 'BATSE', 'BurstCube')
    Aeffs = (320., 132., 132., 132., 132., 1500., 61.)
    nDets = (7, 12, 12, 7, 7, 8, 4)
    indices = (0.6, 0.78, 0.78, 0.78, 0.78, 1.0, 0.6)
    
    for i, mission in enumerate(missions):
        sc, Aeff, index = load_mission(mission, 0., 260.)

        assert (np.abs(Aeffs[i] - Aeff) < 1e-7)
        assert nDets[i] == len(sc.pointings)
        assert (np.abs(indices[i] - index) < 1e-7)

    
def test_thetaphi2radec():

    """Tests the thetaphi2radec function."""
    
    from BurstCube.ReqSim.gammaray_proposal_tools import thetaphi2radec

    ra, dec = thetaphi2radec(1.5, 3.0)

    assert (np.abs(ra - 188.11266146075303) < 1e-7)
    assert (np.abs(dec - 4.056330730376516) < 1e-7)

    
def test_plot_exposures():

    """Tests the plot_exposures function.  Uses the Bia as the baseline."""

    import json
    from BurstCube.ReqSim.gammaray_proposal_tools import load_mission,\
        plot_exposures

    scA, Aeff, index = load_mission('Bia')

    scB, fs, ep, exp = plot_exposures(scA.pointings, Aeff, doplot=False)

    scA_str = json.dumps(scA.pointings, sort_keys=True)
    scB_str = json.dumps(scB.pointings, sort_keys=True)

    assert scA_str == scB_str
    assert (np.abs(fs.sum() - 6549119.434179142) < 1e-7)

    ep_B = [2.20608000e+06, -2.91038305e-11]
    np.testing.assert_allclose(ep.sum(axis=1), ep_B, rtol=1e-5, atol=0)

    exp_B = [2894.58578979, 2891.30008698, 2894.54420279, 2902.86230489,
             2907.83154417, 2902.90220647, 3071.9720967]
    np.testing.assert_allclose(exp.sum(axis=1), exp_B, rtol=1e-5, atol=0)

def test_num_detectors():

    """Tests the num_detectors function. Uses Bia as the baseline."""

    from BurstCube.ReqSim.gammaray_proposal_tools import num_detectors,\
        load_mission, plot_exposures
    
    sc, Aeff, index = load_mission('Bia')
    sc, fs, ep, exp = plot_exposures(sc.pointings, Aeff, doplot=False)

    fs_det = num_detectors(sc, ep)
    
    assert (np.sum(fs_det) == 21430.0)


def test_num_detectors_frac():

    """Tests the num_detectors function. Uses Bia as the baseline."""

    fracs_test = [0.3151041666666667,
                  0.12980143229166666,
                  0.269287109375,
                  0.09611002604166667,
                  0.16731770833333334,
                  0.0185546875,
                  0.0015462239583333333]
    
    from BurstCube.ReqSim.gammaray_proposal_tools import num_detectors,\
        load_mission, plot_exposures, num_detectors_frac

    sc, Aeff, index = load_mission('Bia')
    sc, fs, ep, exp = plot_exposures(sc.pointings, Aeff, doplot=False)
    fs_det = num_detectors(sc, ep)

    fracs = num_detectors_frac(fs_det)

    np.testing.assert_allclose(fracs, fracs_test, rtol=1e-5, atol=0)

def test_colormap_skewed():

    from BurstCube.ReqSim.gammaray_proposal_tools import load_mission,\
        plot_exposures, colormap_skewed

    sc, Aeff, index = load_mission('Bia')
    sc, fs, ep, exp = plot_exposures(sc.pointings, Aeff, doplot=False)

    cmap = colormap_skewed(exp)

    assert (cmap.name == 'skewed')

def test_random_sky():

    """Tests the random sky function.  Just makes sure that the ra, dec
    pairs are in the right range. """
    
    from BurstCube.ReqSim.gammaray_proposal_tools import random_sky
    
    ra, dec = random_sky(20)

    for pos in zip(ra, dec):
        assert(pos[0] <= 360. and pos[0] >= 0.)
        assert(pos[1] <= 90. and pos[1] >= -90.)

        
def test_separation():

    """Tests the separation function against the astropy SkyCoords
    function.  The tolerance on this seems a bit high.  In the future we
    should replace this function with the astropy one. """

    from BurstCube.ReqSim.gammaray_proposal_tools import random_sky, separation
    from astropy.coordinates import SkyCoord

    ra1, dec1 = random_sky(20)
    ra2, dec2 = random_sky(20)

    c1 = SkyCoord(ra1, dec1, unit="deg")
    c2 = SkyCoord(ra2, dec2, unit="deg")

    for i, ra in enumerate(ra1):
        sep1 = separation(ra1[i], dec1[i], ra2[i], dec2[i])
        sep2 = c1[i].separation(c2[i])
        assert(np.abs(sep1 - sep2.degree) < 1e-13)


def test_loginterpol():

    """Tests the loginterpol function"""

    from BurstCube.ReqSim.gammaray_proposal_tools import loginterpol
    
    x = np.array([50., 75.1462, 112.939, 169.739, 255.105, 383.404, 576.227,
                  866.025, 1301.57, 1956.16, 2939.97, 4418.55, 6640.74,
                  9980.54, 15000.], dtype=np.float32)

    y = np.array([56.0057, 60.1213, 61.7605, 61.7576, 54.1984, 42.0248,
                  33.3321, 27.8825, 22.6889, 19.9883, 18.7626, 18.1448,
                  18.8384, 20.1002, 20.9645], dtype=np.float32)
    
    eng = np.logspace(np.log10(50), np.log10(300), 100)

    bcaeff = loginterpol(x, y, eng)

    assert(np.abs(5885.900562958536 - bcaeff.sum()) < 1e-7)
    
    
