#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import os
from distutils.core import setup
from setuptools import find_packages

PACKAGE_DIR = 'src'
NAME='protocol-diagrams'

setup(
    name=NAME,
    version='0.1',
    url='https://github.com/tpmanley/protocol-diagrams',
    description='Make nice-looking network protocol diagrams',
    author='Tom Manley',
    author_email='tom.manley@gmail.com',
    long_description='',
    package_dir={'': PACKAGE_DIR},
    packages=find_packages(PACKAGE_DIR),
    #py_modules=['ordereddict'],
	install_requires=[
		'pyparsing',
		'flask',
		],
)
