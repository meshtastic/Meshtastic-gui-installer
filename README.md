# Meshtastic-gui-installer

[![Pylint](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/pylint.yml/badge.svg)](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/pylint.yml) 
[![codecov](https://codecov.io/gh/meshtastic/Meshtastic-gui-installer/branch/master/graph/badge.svg?token=CEnDhjIJFU)](https://codecov.io/gh/meshtastic/Meshtastic-gui-installer)
![PyPI - Downloads](https://img.shields.io/pypi/dm/meshtastic-flasher)

Cross Platform GUI for installing Meshtastic Firmware. It also checks and updates the RAK 4631 bootloader.


# Example showing a Heltec (esp32) device:
<img width="766" alt="Screen Shot 2022-02-01 at 4 34 24 PM" src="https://user-images.githubusercontent.com/2219838/152100775-3e0f5305-4ffb-4e8a-8dca-4b02f3c0ff14.png">

# Example showing a RAK WisBlock Core RAK4631:
<img width="766" alt="Screen Shot 2022-02-01 at 9 57 24 PM" src="https://user-images.githubusercontent.com/2219838/152100859-cb59d0cd-2ffa-49a1-9c8f-6ce75c625468.png">


# Installation

* For the single file executable see [Releases](https://github.com/meshtastic/Meshtastic-gui-installer/releases). There is a readme.txt that shows the steps to get started.

* Steps to install from PyPi (if you do not want the single executable method described above):

Linux/Mac:

```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install meshtastic-flasher
```

Windows command prompt: (assuming Python3 was installed from https://www.python.org/downloads/ and `python --version` reports 3.6+):

```
python -m venv venv
venv\Bin\Activate
pip install --upgrade pip
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
source venv/bin/activate
pip install --upgrade pip
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

# To test

```
pytest
```


# for more info

https://wiki.qt.io/Qt_for_Python

https://pygithub.readthedocs.io/en/latest/introduction.html

https://meshtastic.org/

https://github.com/meshtastic/Meshtastic-device

# Known Systems

* Ubuntu 20.04 (x86_64)
* Fedora 33 (x86_64)
* Manjaro 21.2.3 (x86_64)
* Linux Mint 20.3 (x86_64)
* MacOS (arm and x86)
* Windows 7 and 10 (may work on other versions)
* ArchlinuxArm with the following commands:

```
pacman -S qt6 pyside6
pip install meshtastic-flasher
```

# Known limitations

The following are known limitations:

* Raspberry Pi is not available, since it is arm-based and there are no pre-built libraries for PySide. There is an interesting link here: https://github.com/piwheels/packages/issues/4#issuecomment-772058821 . 

* Ubuntu 20.04 is the version used for testing, it may work with other versions (Known issue with Wayland https://github.com/meshtastic/Meshtastic-gui-installer/issues/8 )

* Many linux arm variations will work as Qt does not support arm. See https://doc.qt.io/qt-6/supported-platforms.html 

* If you just run the `pip install meshtastic-flasher` outside of a fresh python virtual environment (like say on a mac that has used `brew` to install things) you may get this error:

```
    from meshtastic_flasher.installer import main
  File "/usr/local/lib/python3.9/site-packages/meshtastic_flasher/installer.py", line 20, in <module>
    from meshtastic.util import detect_supported_devices, findPorts, detect_windows_needs_driver
```

If you get this error, then install in a python virtual environment as described in the Installation step above.

# Note to Devs

Please keep code as simple as possible. PyQT has a tendency to get complicated.


