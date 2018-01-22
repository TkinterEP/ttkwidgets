# Copyright (c) RedFantom 2017
# For license see LICENSE
from setuptools import setup

setup(
    name="ttkwidgets",
    packages=["ttkwidgets", "ttkwidgets.frames", "ttkwidgets.font", "ttkwidgets.autocomplete", "ttkwidgets.color"],
    py_modules=["ttkwidgets"],
    package_data={"ttkwidgets": ["assets/*"]},
    version="0.9.0",
    description=" A collection of widgets for Tkinter's ttk extensions by various authors ",
    author="The ttkwidgets authors",
    url="https://www.github.com/RedFantom/ttkwidgets",
    download_url="https://www.github.com/RedFantom/ttkwidgets/releases",
    license="AGPL",
    classifiers=["Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
    install_requires=["pillow"]
)
