#!/usr/bin/env python

from astropy.tests.helper import pytest

try:
    from bcSim import bcSim
except ImportError:
    pass


@pytest.fixture(scope='module')
def create_burstcube_analysis(request, tmpdir_factory):

    from os import path

    testdir = path.expandvars('$BURSTCUBE/Simulation/MEGAlib/test/')
    bcs = bcSim(testdir+'test.inc1.id1.sim',testdir+'FarFieldPointSource_test.source')
    return bcs

def test_bcSim_setup(create_burstcube_analysis):
    bcs = create_burstcube_analysis
    bcs.printDetails()


