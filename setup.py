# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

from setuptools import setup

setup(name='py2hwsw',
	version='0.1',
	description='A Python framework for managing embedded HW/SW projects',
	url='https://github.com/IObundle/py2hwsw',
	author='IObundle',
	author_email='some_email@some.provider',
	license='Some license',
	packages=['py2hwsw'],
	entry_points={
		'console_scripts': ['py2hwsw = py2hwsw.main:main']
	},
	package_data={
		'py2hwsw': ['**', '.*']
	},
	include_package_data=True,
	zip_safe=False
)
