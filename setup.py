#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "Combox",
    version = "0.1",
    description = "Easily deploy and manage local development environments on your own system.",
    packages = find_packages(),
    author = "Laurent Eschenauer",
    author_email = "laurent.eschenauer@comodit.com",
    scripts = ["combox"],
)
