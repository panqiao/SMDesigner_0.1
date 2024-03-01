from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import os
from glob import glob





setup(
    name='SMDesigner',
    version='1.0.0',
    packages=find_packages(),
    package_data={
        'SMDesigner': ['test/demo/*', 'R2R_install.sh','test/r2r_test/*'],
    },
    
    install_requires=[
        # List your Python dependencies here
    ],
    entry_points={
        'console_scripts': [
            'SMDesigner=SMDesigner.SMDsigner3_test_r2r:starter_function',
            #'r2r_drawing=SMDesigner.r2r_drawing_flag_test:main_r2r'
        ],
    },
    #package_data=package_data,
    
    
)



