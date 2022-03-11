# Meshtastic-gui-installer

[![Pylint](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/pylint.yml/badge.svg)](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/pylint.yml)
[![codecov](https://codecov.io/gh/meshtastic/Meshtastic-gui-installer/branch/master/graph/badge.svg?token=CEnDhjIJFU)](https://codecov.io/gh/meshtastic/Meshtastic-gui-installer)
![PyPI - Downloads](https://img.shields.io/pypi/dm/meshtastic-flasher)

Cross Platform GUI for installing [Meshtastic](https://meshtastic.org/) [Firmware](https://github.com/meshtastic/Meshtastic-device). It also checks and updates the [RAK 4631](https://docs.rakwireless.com/Product-Categories/WisBlock/RAK4631/Overview/) and [LilyGo T-Echo](https://github.com/Xinyuan-LilyGO/LilyGO-T-Echo) bootloaders.


# Example showing esp32 device:
<img width="806" alt="Screen Shot 2022-02-24 at 12 39 59 PM" src="https://user-images.githubusercontent.com/2219838/155604278-4d56bf40-11b3-45a7-86b7-bff93b514c8b.png">


# Example showing a RAK WisBlock Core RAK4631:
<img width="806" alt="Screen Shot 2022-02-24 at 12 41 05 PM" src="https://user-images.githubusercontent.com/2219838/155604298-c45ff068-c63b-4e96-af1c-820f396f036c.png">

# Settings
<img width="1072" alt="Screen Shot 2022-02-24 at 12 41 51 PM" src="https://user-images.githubusercontent.com/2219838/155604372-64c087e9-104e-4397-94f0-7992391bca49.png">

# To install:

See https://meshtastic.org/docs/getting-started/meshtastic-flasher

Note: The "single executable" installation option has been deprecated as of March 10, 2022.

# Advanced options

To go into the Advanced Options page, press the "A" key or click on the "Advanced Options" in the top left of the main screen

Capabilities:

* Update mode for esp32 devices: Instead of doing a complete flash, you can do an "update"
* view the equivalent of `meshtastic --info`
* send a simple text message
* backup the connected device configuration to yaml file
* restore configuration from yaml file to the connected device

# Device Settings

* Click on the "Device Settings" at the top of the main screen to change settings.
* "Factory Reset" is availaable in the Admin tab
* "Hotkeys" and "Tips" are also options


# Installation for Development

* Steps to install from [PyPi](https://pypi.org/project/meshtastic-flasher/) - typically used for development

First clone repo and change into the Meshtastic-gui-installer directory.

```
python3 -m venv venv
source venv/bin/activate
# or if on windows: venv\scripts\activate
pip install --upgrade pip
pip install .
```

To run, type in "meshtastic-flasher"

# To lint (for developers)

```
pylint *.py
```

or

```
make lint
```

# To test (for developers)

```
pytest
```


# For more info

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
* Windows 7, 8.1, 10, and 11 (may work on other versions)
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

* Windows 10 will not work with python v3.8.0 due to issue https://stackoverflow.com/questions/56757044/pyside2-dll-load-failed-the-specified-procedure-could-not-be-found/70533728#70533728 . It has been tested on python 3.10 on Windows 10.

* User reported it does not run on MacOS High Sierra.

# Note to Developers

Please keep code as simple as possible.
