import numpy as np


def test_mission():

    """Test the mission object."""

    from BurstCube.ReqSim.Mission import Mission

    missions = Mission.Missions
    Aeffs = (320., 132., 132., 132., 132., 1500., 61.)
    nDets = (7, 12, 12, 7, 7, 8, 4)
    indices = (0.6, 0.78, 0.78, 0.78, 0.78, 1.0, 0.6)

    for i, mission in enumerate(missions):
        m = Mission(mission)

        assert (np.abs(Aeffs[i] - m.Aeff) < 1e-7)
        assert nDets[i] == len(m.pointings)
        assert (np.abs(indices[i] - m.cosindex) < 1e-7)

        
def test_calcExposures():

    from BurstCube.ReqSim.Mission import Mission

    bia = Mission('Bia')

    bia.calcExposures()

    assert (np.abs(bia.fs.sum() - 8029553.595252864) < 1e-7)

    ep_B = [2.20608000e+06, -2.91038305e-11]
    np.testing.assert_allclose(bia.exposure_positions.sum(axis=1),
                               ep_B, rtol=1e-5, atol=0)

    exp_B = [3535.58505609, 3530.8280102, 3535.51524954, 3547.52652658,
             3554.32882863, 3547.59446776, 3840.97684637]
    
    np.testing.assert_allclose(bia.exposures.sum(axis=1),
                               exp_B, rtol=1e-5, atol=0)


def test_fs_det():

    from BurstCube.ReqSim.Mission import Mission

    bia = Mission('Bia')
    bia.calcExposures()

    assert(bia.fs_det.sum() == 21430.0)

    
def test_fs_det_frac():

    from BurstCube.ReqSim.Mission import Mission

    fracs_test = [0.3151041666666667,
                  0.12980143229166666,
                  0.269287109375,
                  0.09611002604166667,
                  0.16731770833333334,
                  0.0185546875,
                  0.0015462239583333333]

    bia = Mission('Bia')
    bia.calcExposures()

    np.testing.assert_allclose(bia.fs_det_frac, fracs_test, rtol=1e-5, atol=0)
        

def test_grb_exposures():

    from BurstCube.ReqSim.Mission import Mission

    bc = Mission('BurstCube')
    ra = [54.38851436, 253.03282371, 285.83469231, 231.44380048, 252.94589971,
          270.92354825, 166.44750484, 95.82935811, 129.83344903, 210.25884342]
    dec = [28.53096934, -24.84064642, -5.08471427, 25.0625712, 42.71293351,
           52.92523815, 26.60425591, 37.761506, -70.07064967, 66.42455829]

    r_b_sum = 14.515707814840491
    e_b_sum = 14.515707814840491
    s_b = [0., 0.65322979, 0., 0.81069429, 0.76365778, 0.59805962,
           0.85381265, 0.64610835, 0.5226085, 0.56436512]
    
    r_a, e_a, s_a = bc.grb_exposures(ra, dec)

    assert(np.abs(r_a.sum() - r_b_sum) < 1e-7)
    assert(np.abs(e_a.sum() - e_b_sum) < 1e-7)
    np.testing.assert_allclose(s_a, s_b, rtol=1e-7, atol=0)
