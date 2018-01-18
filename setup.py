#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os import path

from setuptools import setup

if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 5):
    sys.exit('Error: Python 3.x is required.')

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='automergetool',
    version='0.3.0',
    description='A tool to simplify the process of solving conflicts after a git merge, rebase or cherry-pick.',
    long_description=readme,
    author='Xavier F. Gouchet',
    author_email='python@xgouchet.fr',
    url='https://github.com/xgouchet/AutoMergeTool',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control :: Git',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['git merge conflicts'],
    packages=['automergetool', 'automergetool.solvers'],
    # install_requires=['peppercorn'],
    extras_require={'test': ['nose2', 'coverage'], },
    entry_points={'console_scripts': ['amt = automergetool.amt:run_main', ], }, )
