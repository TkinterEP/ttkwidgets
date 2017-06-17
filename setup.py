# Copyright (c) RedFantom 2017
# For license see LICENSE
from setuptools import setup

setup(
    name="ttkwidgets",
    packages=["ttkwidgets"],
    version="0.1.0",
    description=" A collection of widgets for Tkinter's ttk extensions by various authors ",
    author="RedFantom and others",
    url="https://www.github.com/RedFantom/ttkwidgets",
    download_url="https://www.github.com/RedFantom/ttkwidgets/releases",
    license="AGPL",
    classifiers=["Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
    include_package_data=True,
    install_requires=["pillow"]
)
