# import os
from setuptools import setup

with open("README.md", 'r') as readme:
    long_description = readme.read()

setup(
    name='vivarium-tellurium',
    version='0.0.1',
    packages=[
        'vivarium_tellurium',
        'vivarium_tellurium.composites',
        'vivarium_tellurium.experiments',
        'vivarium_tellurium.library',
        'vivarium_tellurium.processes',
    ],
    author='Eran Agmon, Alexander Patrie',
    author_email='',
    url='https://github.com/vivarium-collective/vivarium-tellurium',
    license='',
    description='A Vivarium interface for Tellurium',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'vivarium-core',
        'tellurium',
        'pytest',
    ],
)