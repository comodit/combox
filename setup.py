#!/usr/bin/env python

from setuptools import setup, find_packages

requires = []
with open('requirements.txt', 'r') as f:
    requires = f.readlines()

setup(
    name = 'comodit-combox',
    version = '0.1',
    description = "Easily deploy and manage local development environments "
                  "on your own system.",
    author = 'ComodIT',
    author_email = 'support@comodit.com',
    packages = find_packages(),
    install_requires=[requires],
    scripts = ['bin/combox'],
)
