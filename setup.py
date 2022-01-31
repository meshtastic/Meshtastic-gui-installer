# Note: you shouldn't need to run this script manually.  It is run implicitly by the pip3 install command.
"""Setup script for meshtastic_flasher package."""

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setup(
    name="meshtastic_flasher",
    version="1.0.39",
    description="Graphical user interface to flash Meshtastic firmware to devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meshtastic/Meshtastic-gui-installer",
    author="Kevin Hester",
    author_email="kevinh@geeksville.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
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
        '': ['logo.png', 'meshtastic_theme.xml'],
    },
    install_requires=["pyside6", "PyGithub", "esptool", "meshtastic", "qt-material",
                      "psutil"],
    extras_require={
    },
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "meshtastic-flasher=meshtastic_flasher.installer:main",
        ]
    },
)
