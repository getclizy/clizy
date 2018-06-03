#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 6):
    raise RuntimeError("Python < 3.6 is not supported!")

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='clizy',
    version='0.0.2',
    description="Command-line interface creation for lazy people using type hints.",
    long_description=long_description,
    url='https://github.com/prokopst/clizy',
    packages=find_packages(include=['clizy']),
    author="Stan Prokop",
    license='Apache 2 License',
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
    ]
)
