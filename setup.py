# Copyright (c) RedFantom 2017
# For license see LICENSE
from setuptools import setup

long_description = """
ttkwidgets
==========

|Travis| |Appveyor| |Codecov| |Pypi| |License|

A collection of widgets for Tkinter's ttk extensions by various authors


License
-------

ttkwidgets: A collection of widgets for Tkinter's ttk extensions by various authors 
Copyright (C) RedFantom 2017
Copyright (C) The Python Team
Copyright (C) Mitja Martini 2008
Copyright (C) Russell Adams 2011
Copyright (C) Juliette Monsel 2017

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.



.. |Travis| image:: https://travis-ci.org/RedFantom/ttkwidgets.svg?branch=master
    :alt: Travis CI Build Status
    :target: https://travis-ci.org/RedFantom/ttkwidgets

.. |Appveyor| image:: https://ci.appveyor.com/api/projects/status/c6j6td273u3y6rw7/branch/master?svg=true
    :alt: Appveyor Build Status
    :target: https://ci.appveyor.com/project/RedFantom/ttkwidgets/branch/master

.. |Codecov| image:: https://codecov.io/gh/RedFantom/ttkwidgets/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/RedFantom/ttkwidgets
    
.. |Pypi| image:: https://badge.fury.io/py/ttkwidgets.svg
    :alt: PyPI version
    :target: https://badge.fury.io/py/ttkwidgets
    
.. |License| image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :alt: License: GPL v3
    :target: http://www.gnu.org/licenses/gpl-3.0
    
"""

setup(
    name="ttkwidgets",
    packages=["ttkwidgets", "ttkwidgets.frames", "ttkwidgets.font", "ttkwidgets.autocomplete", "ttkwidgets.color"],
    py_modules=["ttkwidgets"],
    package_data={"ttkwidgets": ["assets/*"]},
    version="0.10.0",
    description=" A collection of widgets for Tkinter's ttk extensions by various authors ",
    long_description=long_description,
    author="The ttkwidgets authors",
    url="https://www.github.com/RedFantom/ttkwidgets",
    download_url="https://www.github.com/RedFantom/ttkwidgets/releases",
    license="AGPL",
    classifiers=["Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
    install_requires=["pillow"]
)
