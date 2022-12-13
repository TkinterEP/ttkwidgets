"""
Author: See AUTHORS.md
License: GNU GPLv3
Copyright (c) 2018-2020 The ttkwidgets authors
"""
from setuptools import setup


def read(file_name: str):
    with open(file_name) as fi:
        return fi.read()

setup(
    name="ttkwidgets",
    packages=["ttkwidgets", "ttkwidgets.frames", "ttkwidgets.font", "ttkwidgets.autocomplete", "ttkwidgets.color", "ttkwidgets.validated_entries"],
    py_modules=["ttkwidgets"],
    package_data={"ttkwidgets": ["assets/*"]},
    version="0.13.0",
    description=" A collection of widgets for Tkinter's ttk extensions by various authors ",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="The ttkwidgets authors",
    url="https://www.github.com/RedFantom/ttkwidgets",
    download_url="https://www.github.com/RedFantom/ttkwidgets/releases",
    license="AGPL",
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
    python_requires=">=3.6",
    install_requires=["pillow"]
)
