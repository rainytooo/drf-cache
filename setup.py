#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import re
from io import open

from setuptools import find_packages, setup


def read(f):
    return open(f, "r", encoding="utf-8").read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version("drf_cache")

setup(
    name="drf-cache",
    version=version,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    url="http://www.xsudo.com",
    license="MIT",
    author="vincent wantchalk",
    author_email="ohergal@gmail.com",
    description="A Caching Tools for Django Rest Framework",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    # What does your project relate to?
    keywords="cache drf redis",
    install_requires=[],
    python_requires=">=3.5",
    zip_safe=False,
    classifiers=[
        # How mature is this project? Common values are
        # Development Status:: 1 - Planning
        # Development Status:: 2 - Pre - Alpha
        # Development Status:: 3 - Alpha
        # Development Status:: 4 - Beta
        # Development Status:: 5 - Production / Stable
        # Development Status:: 6 - Mature
        # Development Status:: 7 - Inactive
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        # OS
        "Operating System :: OS Independent",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
    ],

)
