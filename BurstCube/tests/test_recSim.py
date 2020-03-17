import numpy as np


def test_load_mission():

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

    from BurstCube.ReqSim.gammaray_proposal_tools import thetaphi2radec

    ra, dec = thetaphi2radec(1.5, 3.0)

    assert (np.abs(ra - 188.11266146075303) < 1e-7)
    assert (np.abs(dec - 4.056330730376516) < 1e-7)

    
