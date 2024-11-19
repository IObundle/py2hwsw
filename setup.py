# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

from setuptools import setup
from py2hwsw.scripts.py2hwsw_version import PY2HWSW_VERSION

setup(
    name="py2hwsw",
    version=PY2HWSW_VERSION,
    description="A Python framework for managing embedded HW/SW projects",
    url="https://github.com/IObundle/py2hwsw",
    author="IObundle",
    author_email="some_email@some.provider",
    license="Some license",
    packages=["py2hwsw"],
    entry_points={"console_scripts": ["py2hwsw = py2hwsw.main:main"]},
    package_data={"py2hwsw": ["**", ".*"]},
    include_package_data=True,
    zip_safe=False,
)
