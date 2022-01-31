# Meshtastic-gui-installer

Cross Platform GUI for installing Meshtastic Firmware

* Steps to install from PyPi

```
python3 -m venv venv
venv/bin/activate
pip install meshtastic-flasher
```

To run, type in "meshtastic-flasher" from a command prompt.



# Installation for Development

* Setup virtual environment and install required packages

```
python3 -m venv venv
venv/bin/activate
pip install -r requirements.txt
pip install .
```

# Setup

* Ensure the file is executable:
```
chmod +x installer.py
```

* Run the application
```
./installer.py
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
