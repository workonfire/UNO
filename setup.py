#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='UNO',
    version='ALPHA',
    description='A simple Python implementation of the UNO game',
    author='workonfire',
    author_email='kolucki62@gmail.com',
    url='https://workonfi.re/',
    packages=find_packages(exclude='tests')
)
