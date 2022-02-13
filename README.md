# Meshtastic-gui-installer

[![Pylint](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/pylint.yml/badge.svg)](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/pylint.yml) 
[![codecov](https://codecov.io/gh/meshtastic/Meshtastic-gui-installer/branch/master/graph/badge.svg?token=CEnDhjIJFU)](https://codecov.io/gh/meshtastic/Meshtastic-gui-installer)
![PyPI - Downloads](https://img.shields.io/pypi/dm/meshtastic-flasher)

Cross Platform GUI for installing [Meshtastic](https://meshtastic.org/) [Firmware](https://github.com/meshtastic/Meshtastic-device). It also checks and updates the [RAK 4631](https://docs.rakwireless.com/Product-Categories/WisBlock/RAK4631/Overview/) bootloader. The [LilyGo T-Echo](https://github.com/Xinyuan-LilyGO/LilyGO-T-Echo) bootloader is also checked.


# Example showing a [Heltec](https://meshtastic.org/docs/hardware/supported/heltec) (esp32) device:
<img width="766" alt="Screen Shot 2022-02-01 at 4 34 24 PM" src="https://user-images.githubusercontent.com/2219838/152100775-3e0f5305-4ffb-4e8a-8dca-4b02f3c0ff14.png">

# Example showing a RAK WisBlock Core RAK4631:
<img width="766" alt="Screen Shot 2022-02-01 at 9 57 24 PM" src="https://user-images.githubusercontent.com/2219838/152100859-cb59d0cd-2ffa-49a1-9c8f-6ce75c625468.png">


# Installation

* For the single file executable see [Releases](https://github.com/meshtastic/Meshtastic-gui-installer/releases). There is a readme.txt that shows the steps to get started.

* Steps to install from [PyPi](https://pypi.org/project/meshtastic-flasher/) (if you do not want the single executable method described above):

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
venv\Scripts\Activate
pip install --upgrade pip
pip install meshtastic-flasher
```


To run, type in "meshtastic-flasher" from a command prompt.


# Updating

To update a pip-installed installation, run the following commands:

Linux/Mac:

```
source venv/bin/activate
pip install --upgrade meshtastic-flasher
```

Windows command prompt:

```
venv\Scripts\Activate
pip install --upgrade meshtastic-flasher
```


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
# or if on windows: venv\scripts\activate
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

# Tested on

* Ubuntu 20.04, 21.04, and 22.04 (x86_64)

If you get this error:

```
qt.qpa.plugin: Could not load the Qt platform "xcb" in "" even though it was found.
This application failed to start because not Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vkkrrdisplay, vnc, wayland-egl, wayland, xcb.
Aborted.
```

Then this might solve the issue:

```
sudo apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev
```

* Fedora 33 (x86_64)
* Manjaro 21.2.3 (x86_64)
* Linux Mint 20.3 (x86_64)
* MacOS (arm and x86)
* Windows 7, 10, and 11 (may work on other versions)
* ArchlinuxArm with the following commands:

```
pacman -S qt6 pyside6
pip install meshtastic-flasher
```

# Known limitations

The following are known limitations:

* Raspberry Pi is not available, since it is arm-based and there are no pre-built libraries for PySide. There is an interesting link here: https://github.com/piwheels/packages/issues/4#issuecomment-772058821 . 

* Ubuntu 20.04 is the version used for testing, it may work with other versions (Known issue with Wayland https://github.com/meshtastic/Meshtastic-gui-installer/issues/8 )

* Ubuntu 18.04 will not work as PySide6/Qt6 libraries are not available.

* Many linux arm variations will work as Qt does not support arm. See https://doc.qt.io/qt-6/supported-platforms.html 

* If you just run the `pip install meshtastic-flasher` outside of a fresh python virtual environment (like say on a mac that has used `brew` to install things) you may get this error:

```
    from meshtastic_flasher.installer import main
  File "/usr/local/lib/python3.9/site-packages/meshtastic_flasher/installer.py", line 20, in <module>
    from meshtastic.util import detect_supported_devices, findPorts, detect_windows_needs_driver
```

If you get this error, then install in a python virtual environment as described in the Installation step above.

* Windows 11 works with CP210x Universal Windows Driver, and you must start the command prompt as Administrator

# Note to Devs

Please keep code as simple as possible. PyQT has a tendency to get complicated.
