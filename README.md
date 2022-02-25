# Meshtastic-gui-installer

[![Pylint](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/pylint.yml/badge.svg)](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/pylint.yml) 
[![codecov](https://codecov.io/gh/meshtastic/Meshtastic-gui-installer/branch/master/graph/badge.svg?token=CEnDhjIJFU)](https://codecov.io/gh/meshtastic/Meshtastic-gui-installer)
![PyPI - Downloads](https://img.shields.io/pypi/dm/meshtastic-flasher)

Cross Platform GUI for installing [Meshtastic](https://meshtastic.org/) [Firmware](https://github.com/meshtastic/Meshtastic-device). It also checks and updates the [RAK 4631](https://docs.rakwireless.com/Product-Categories/WisBlock/RAK4631/Overview/) and [LilyGo T-Echo](https://github.com/Xinyuan-LilyGO/LilyGO-T-Echo) bootloaders.


# Example showing esp32 device:
<img width="806" alt="Screen Shot 2022-02-24 at 12 39 59 PM" src="https://user-images.githubusercontent.com/2219838/155604278-4d56bf40-11b3-45a7-86b7-bff93b514c8b.png">


# Example showing a RAK WisBlock Core RAK4631:
<img width="806" alt="Screen Shot 2022-02-24 at 12 41 05 PM" src="https://user-images.githubusercontent.com/2219838/155604298-c45ff068-c63b-4e96-af1c-820f396f036c.png">

# Advanced Options
<img width="485" alt="Screen Shot 2022-02-24 at 12 41 12 PM" src="https://user-images.githubusercontent.com/2219838/155604337-3d0632e5-941e-4a3e-832c-71e1e80adff4.png">

# Settings
<img width="1072" alt="Screen Shot 2022-02-24 at 12 41 51 PM" src="https://user-images.githubusercontent.com/2219838/155604372-64c087e9-104e-4397-94f0-7992391bca49.png">


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
venv\Scripts\activate
python -m pip install --upgrade pip
pip install meshtastic-flasher
```


To run, type in "meshtastic-flasher" from a command prompt.


Here is are two screen shots showing an installation on windows after starting a "command prompt":


<img width="1010" alt="Screen Shot 2022-02-22 at 11 11 22 AM" src="https://user-images.githubusercontent.com/2219838/155202401-07cedfb4-21bf-46c7-a5fc-a204bac4747d.png">

<img width="1134" alt="Screen Shot 2022-02-22 at 11 11 03 AM" src="https://user-images.githubusercontent.com/2219838/155202427-2ac72d08-f4dd-461b-a4c3-614751eeb818.png">

And the same session (but showing the text):

```
c:\>mkdir some_dir

c:\>cd some_dir

c:\some_dir>python --version
Python 3.9.9

c:\some_dir>python -m venv venv

c:\some_dir>venv\Scripts\activate

(venv) c:\some_dir>python -m pip install --upgrade pip
Requirement already satisfied: pip in .\venv\lib\site-packages (21.2.4)
Collecting pip
  Using cached pip-22.0.3-py3-none-any.whl (2.1 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 21.2.4
    Uninstalling pip-21.2.4:
      Successfully uninstalled pip-21.2.4
Successfully installed pip-22.0.3

(venv) c:\some_dir>pip install meshtastic-flasher
Collecting meshtastic-flasher
  Downloading meshtastic_flasher-1.0.75-py3-none-any.whl (81 kB)
     ---------------------------------------- 81.5/81.5 KB 2.3 MB/s eta 0:00:00
Collecting pyside6
  Using cached PySide6-6.2.3-6.2.3-cp36.cp37.cp38.cp39.cp310-none-win_amd64.whl (156.6 MB)
Collecting PyGithub
  Using cached PyGithub-1.55-py3-none-any.whl (291 kB)
Collecting psutil
  Using cached psutil-5.9.0-cp39-cp39-win_amd64.whl (245 kB)
Collecting meshtastic>=1.2.85
  Using cached meshtastic-1.2.85-py3-none-any.whl (70 kB)
Collecting adafruit-nrfutil
  Using cached adafruit-nrfutil-0.5.3.post16.tar.gz (49 kB)
  Preparing metadata (setup.py) ... done
Collecting pyserial
  Using cached pyserial-3.5-py2.py3-none-any.whl (90 kB)
Collecting qt-material
  Using cached qt_material-2.8.19-py3-none-any.whl (1.7 MB)
Collecting esptool
  Using cached esptool-3.2.tar.gz (206 kB)
  Preparing metadata (setup.py) ... done
Collecting protobuf>=3.13.0
  Using cached protobuf-3.19.4-cp39-cp39-win_amd64.whl (895 kB)
Collecting pyqrcode>=1.2.1
  Using cached PyQRCode-1.2.1.zip (41 kB)
  Preparing metadata (setup.py) ... done
Collecting dotmap>=1.3.14
  Using cached dotmap-1.3.26-py3-none-any.whl (11 kB)
Collecting pypubsub>=4.0.3
  Using cached Pypubsub-4.0.3-py3-none-any.whl (61 kB)
Collecting tabulate>=0.8.9
  Using cached tabulate-0.8.9-py3-none-any.whl (25 kB)
Collecting timeago>=1.0.15
  Using cached timeago-1.0.15.tar.gz (26 kB)
  Preparing metadata (setup.py) ... done
Collecting pyyaml
  Using cached PyYAML-6.0-cp39-cp39-win_amd64.whl (151 kB)
Collecting pexpect>=4.6.0
  Using cached pexpect-4.8.0-py2.py3-none-any.whl (59 kB)
Collecting click>=5.1
  Using cached click-8.0.4-py3-none-any.whl (97 kB)
Collecting ecdsa>=0.13
  Using cached ecdsa-0.17.0-py2.py3-none-any.whl (119 kB)
Collecting bitstring>=3.1.6
  Using cached bitstring-3.1.9-py3-none-any.whl (38 kB)
Collecting cryptography>=2.1.4
  Using cached cryptography-36.0.1-cp36-abi3-win_amd64.whl (2.2 MB)
Collecting reedsolo<=1.5.4,>=1.5.3
  Using cached reedsolo-1.5.4.tar.gz (271 kB)
  Preparing metadata (setup.py) ... done
Collecting requests>=2.14.0
  Using cached requests-2.27.1-py2.py3-none-any.whl (63 kB)
Collecting pynacl>=1.4.0
  Using cached PyNaCl-1.5.0-cp36-abi3-win_amd64.whl (212 kB)
Collecting deprecated
  Using cached Deprecated-1.2.13-py2.py3-none-any.whl (9.6 kB)
Collecting pyjwt>=2.0
  Using cached PyJWT-2.3.0-py3-none-any.whl (16 kB)
Collecting shiboken6==6.2.3
  Using cached shiboken6-6.2.3-6.2.3-cp36.cp37.cp38.cp39.cp310-none-win_amd64.whl (2.3 MB)
Collecting Jinja2
  Using cached Jinja2-3.0.3-py3-none-any.whl (133 kB)
Collecting colorama
  Using cached colorama-0.4.4-py2.py3-none-any.whl (16 kB)
Collecting cffi>=1.12
  Using cached cffi-1.15.0-cp39-cp39-win_amd64.whl (180 kB)
Collecting six>=1.9.0
  Using cached six-1.16.0-py2.py3-none-any.whl (11 kB)
Collecting ptyprocess>=0.5
  Using cached ptyprocess-0.7.0-py2.py3-none-any.whl (13 kB)
Collecting charset-normalizer~=2.0.0
  Downloading charset_normalizer-2.0.12-py3-none-any.whl (39 kB)
Collecting urllib3<1.27,>=1.21.1
  Using cached urllib3-1.26.8-py2.py3-none-any.whl (138 kB)
Collecting certifi>=2017.4.17
  Using cached certifi-2021.10.8-py2.py3-none-any.whl (149 kB)
Collecting idna<4,>=2.5
  Using cached idna-3.3-py3-none-any.whl (61 kB)
Collecting wrapt<2,>=1.10
  Using cached wrapt-1.13.3-cp39-cp39-win_amd64.whl (34 kB)
Collecting MarkupSafe>=2.0
  Downloading MarkupSafe-2.1.0-cp39-cp39-win_amd64.whl (16 kB)
Collecting pycparser
  Using cached pycparser-2.21-py2.py3-none-any.whl (118 kB)
Using legacy 'setup.py install' for adafruit-nrfutil, since package 'wheel' is not installed.
Using legacy 'setup.py install' for esptool, since package 'wheel' is not installed.
Using legacy 'setup.py install' for pyqrcode, since package 'wheel' is not installed.
Using legacy 'setup.py install' for reedsolo, since package 'wheel' is not installed.
Using legacy 'setup.py install' for timeago, since package 'wheel' is not installed.
Installing collected packages: timeago, tabulate, reedsolo, pyserial, pyqrcode, ptyprocess, dotmap, certifi, bitstring, wrapt, urllib3, six, shiboken6, pyyaml, pypubsub, pyjwt, pycparser, psutil, protobuf, pexpect, MarkupSafe, idna, colorama, charset-normalizer, requests, pyside6, meshtastic, Jinja2, ecdsa, deprecated, click, cffi, qt-material, pynacl, cryptography, adafruit-nrfutil, PyGithub, esptool, meshtastic-flasher
  Running setup.py install for timeago ... done
  Running setup.py install for reedsolo ... done
  Running setup.py install for pyqrcode ... done
  Running setup.py install for adafruit-nrfutil ... done
  Running setup.py install for esptool ... done
Successfully installed Jinja2-3.0.3 MarkupSafe-2.1.0 PyGithub-1.55 adafruit-nrfutil-0.5.3.post16 bitstring-3.1.9 certifi-2021.10.8 cffi-1.15.0 charset-normalizer-2.0.12 click-8.0.4 colorama-0.4.4 cryptography-36.0.1 deprecated-1.2.13 dotmap-1.3.26 ecdsa-0.17.0 esptool-3.2 idna-3.3 meshtastic-1.2.85 meshtastic-flasher-1.0.75 pexpect-4.8.0 protobuf-3.19.4 psutil-5.9.0 ptyprocess-0.7.0 pycparser-2.21 pyjwt-2.3.0 pynacl-1.5.0 pypubsub-4.0.3 pyqrcode-1.2.1 pyserial-3.5 pyside6-6.2.3 pyyaml-6.0 qt-material-2.8.19 reedsolo-1.5.4 requests-2.27.1 shiboken6-6.2.3 six-1.16.0 tabulate-0.8.9 timeago-1.0.15 urllib3-1.26.8 wrapt-1.13.3

(venv) c:\some_dir>meshtastic-flasher
```

If you close that command prompt, but want to run `meshtastic-flasher` again:

<img width="1052" alt="Screen Shot 2022-02-22 at 11 16 51 AM" src="https://user-images.githubusercontent.com/2219838/155203288-19744db6-6718-4b52-b18a-0659f8863cda.png">


```
Microsoft Windows [Version 10.0.19041.1415]
(c) Microsoft Corporation. All rights reserved.

C:\Users\YOURUSERNAME>cd c:\

c:\>cd some_dir

c:\some_dir>venv\Scripts\activate

(venv) c:\some_dir>meshtastic-flasher
```


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

# Other options

* The ability to change Device Settings has been added.
* The ability to do a "factory reset" is an options in the Settings page (Admin tab).
* "Hotkeys" and "Tips" are also options
* Advanced options has several capabilities: view the equivalent of `meshtastic --info`, backup Device configuration to yaml file, restore Device configuration from yaml file, and send a simple text message

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

# Note to Devs

Please keep code as simple as possible. PyQT has a tendency to get complicated.
