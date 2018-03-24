#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 6):
    raise RuntimeError("Python < 3.6 is not supported!")

setup(
    name='clizy',
    version='0.0.1',
    description="Command-line interface creation for lazy people using type hints.",
    long_description="",
    url='https://github.com/prokopst/clizy',
    packages=find_packages(include=['clizy']),
    author="Stanislav Prokop",
    license='Apache 2 License',
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
    ]
)
