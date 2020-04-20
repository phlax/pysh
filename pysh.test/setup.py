# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_namespace_packages

from pysh.test.command import PyshCommand


REQUIREMENTS = [
    "termcolor"]

TEST_REQUIREMENTS = [
    'flake8==2.4.1',
    'pytest',
    'pytest-cov',
    'codecov']

README = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'README.md')
with open(README, encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='pysh.test',
    version="0.0.1",
    license='GPL3',
    url='https://github.com/phlax/pysh.test',
    description=(''),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Ryan Northey',
    author_email='ryan@synca.io',
    project_urls={
        'Source': 'https://github.com/phlax/pysh.test',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_namespace_packages(include=["pysh.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    extras_require={
        "install": REQUIREMENTS,
        "test": TEST_REQUIREMENTS},
    entry_points={
        'console_scripts': [
            'pysh = pysh.test.command:main',
        ],
    },
)
