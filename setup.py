# Note: you shouldn't need to run this script manually.  It is run implicitly by the pip3 install command.
"""Setup script for meshtastic_flasher package."""

import pathlib
from setuptools import setup

from meshtastic_flasher.version import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# This call to setup() does all the work
# Note: Version is now in meshtastic_flasher/__version__.py
setup(
    name="meshtastic_flasher",
    version=f"{__version__}",
    description="Graphical user interface to flash Meshtastic firmware to devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meshtastic/Meshtastic-gui-installer",
    author="Kevin Hester",
    author_email="kevinh@geeksville.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["meshtastic_flasher"],
    include_package_data=True,
    package_data={
        '': ['logo.png', 'help.svg', 'info.svg', 'options.svg', 'cog.svg', 'meshtastic_theme.xml', 'fields.json'],
    },
    install_requires=["pyside6", "PyGithub", "esptool", "meshtastic>=1.3alpha.6", "qt-material",
                      "psutil", "adafruit-nrfutil", "pyserial", "geocoder"],
    extras_require={
    },
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "meshtastic-flasher=meshtastic_flasher.main:main",
        ]
    },
)
