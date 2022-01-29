readme.txt for single standalone installer zip files that can be
downloaded from https://github.com/meshtastic/Meshtastic-gui-installer/releases

ubuntu:
  unzip
  chmod +x meshtastic-flasher
  # Note: If the user that runs this command is in the dialout group, you do not use "sudo" below.
  sudo ./meshtastic-flasher

mac:
  unzip
  chmod +x meshtastic-flasher
  ./meshtastic-flasher
  # it will probably abort, go into System Preferences, Security & Privacy, General, Allow apps downloaded
  ./meshtastic-flasher
  # it will probably warn you, click "Open"

windows:
  unzip
  .\meshtastic-flasher.exe
