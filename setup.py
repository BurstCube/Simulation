#!/usr/bin/env python

from setuptools import setup
from BurstCube.version import get_git_version

setup(name='BurstCube',
      version=get_git_version(),
      author='Jeremy Perkins',
      author_email='jsperki1@umd.edu',
      url='https://github.com/BurstCube',
      include_package_data=True,
      packages=['BurstCube', 'BurstCube.LocSim',
                'BurstCube.NoahSim', 'BurstCube.ReqSim'],
      scripts=['BurstCube/scripts/runSims'],
      package_data={
          'BurstCube': ['data/*.sim',
                        'data/*.source',
                        'data/BurstCube_1Cylinder.geo.setup',
                        'data/config.yaml',
                        'data/gbm_effective_area.dat',
                        'data/BC_eff_area_curves.ecsv',
                        'data/gbmtrigcat.fits',
                        'data/gbmgrbcat.fits',
                        'data/*.gz']
          }
      )

