# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from setuptools import setup
from py2hwsw.scripts.py2hwsw_version import PY2HWSW_VERSION
import os
import subprocess
from setuptools.command.install import install


class CreateShortHashFile(install):
    """Create a shortHash.tex file in the package directory"""

    def run(self):
        # Get the current Git commit short hash
        try:
            short_hash = subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], universal_newlines=True
            ).strip()
        except (subprocess.CalledProcessError, OSError):
            short_hash = "unknown"

        # Create the shortHash.tex file in the package directory
        package_dir = os.path.join(os.path.dirname(__file__), "build/lib/py2hwsw")

        short_hash_file = os.path.join(package_dir, "shortHash.tex")
        with open(short_hash_file, "w") as f:
            f.write(short_hash)

        print(f"Created shortHash.tex file with Git commit short hash: {short_hash}")

        install.run(self)


setup(
    name="py2hwsw",
    version=PY2HWSW_VERSION,
    description="A Python framework for managing embedded HW/SW projects",
    url="https://github.com/IObundle/py2hwsw",
    author="IObundle",
    author_email="info@iobundle.com",
    license="MIT",
    packages=["py2hwsw"],
    # py_modules=["api"], # TODO: Figure out how to add py2hwsw api as an importable module
    entry_points={"console_scripts": ["py2hwsw = py2hwsw.main:main"]},
    package_data={"py2hwsw": ["**/*", ".*"]},
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        "install": CreateShortHashFile,
    },
)
