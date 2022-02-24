readme.txt for single standalone installer zip files that can be
downloaded from https://github.com/meshtastic/Meshtastic-gui-installer/releases

ubuntu:
  chmod +x meshtastic-flasher-ubuntu
  # Note: If the user that runs this command is in the dialout group, you do not use "sudo" below.
  sudo ./meshtastic-flasher-ubuntu

mac:
  chmod +x meshtastic-flasher-mac
  ./meshtastic-flasher-mac
  # it will probably abort, go into System Preferences, Security & Privacy, General, Allow apps downloaded
  ./meshtastic-flasher-mac
  # it will probably warn you, click "Open"

windows:
  # Tip: Run from a command prompt so you can watch output as the command runs
  meshtastic-flasher.exe
