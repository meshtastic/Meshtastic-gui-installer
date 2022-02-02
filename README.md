# Meshtastic-gui-installer

[![Pylint](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/pylint.yml/badge.svg)](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/pylint.yml) ![PyPI - Downloads](https://img.shields.io/pypi/dm/meshtastic-flasher)

Cross Platform GUI for installing Meshtastic Firmware. It also checks and updates the RAK 4631 bootloader.


# Example showing a Heltec (esp32) device:
<img width="766" alt="Screen Shot 2022-02-01 at 4 34 24 PM" src="https://user-images.githubusercontent.com/2219838/152100775-3e0f5305-4ffb-4e8a-8dca-4b02f3c0ff14.png">

# Example showing a RAK WisBlock Core RAK4631:
<img width="766" alt="Screen Shot 2022-02-01 at 9 57 24 PM" src="https://user-images.githubusercontent.com/2219838/152100859-cb59d0cd-2ffa-49a1-9c8f-6ce75c625468.png">



* For the single file executable see [Releases](https://github.com/meshtastic/Meshtastic-gui-installer/releases). There is a readme.txt that shows the steps to get started.

* Steps to install from PyPi (if you do not want the sigle executable method described above):

```
pip install meshtastic-flasher
```

To run, type in "meshtastic-flasher" from a command prompt.

# Advanced options

To go into the Advanced options page, press the "A" key. 

The options are:

* Update mode for esp32 devices
* RAK Bootloader update (for RAK4631 nrf52)

# Installation for Development

* Setup virtual environment and install required packages

```
python3 -m venv venv
venv/bin/activate
pip install -r requirements.txt
pip install .
```

# To lint

```
pylint *.py
```

or

```
make lint
```

# for more info

https://wiki.qt.io/Qt_for_Python

https://pygithub.readthedocs.io/en/latest/introduction.html

https://meshtastic.org/

https://github.com/meshtastic/Meshtastic-device


# Note to Devs

Please keep code as simple as possible. PyQT has a tendency to get complicated.
