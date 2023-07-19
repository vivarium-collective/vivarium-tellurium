import os
import glob
import setuptools
from distutils.core import setup

with open("README.md", 'r') as readme:
    long_description = readme.read()

setup(
    name='vivarium-tellurium',  
    version='0.0.1',
    packages=[
        'vivarium_tellurium',
        'vivarium_tellurium.processes',
        'vivarium_tellurium.composites',
        'vivarium_tellurium.experiments',
    ],
    author='Alex Patrie, Eran Agmon',  
    author_email='', 
    url='https://github.com/vivarium-collective/vivarium-tellurium',  
    license='',  
    entry_points={
        'console_scripts': [],
        },
    short_description='A Vivarium interface for Tellurium', 
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_data={},
    include_package_data=True,
    install_requires=[
        'tellurium',
        'vivarium-core',
        'biosimulators-utils',
        'pytest',
    ],
)
