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
