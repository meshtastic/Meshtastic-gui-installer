#!/usr/bin/env python3

import os
import sys
import time
import urllib
import subprocess
import zipfile

import esptool

from meshtastic.util import findPorts
from github import Github
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QHBoxLayout, QDialog, QLabel, QMessageBox)

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.port = None
        self.speed = '921600'
        self.firmware_version = None

        self.setWindowTitle("Meshtastic Installer")

        # Create widgets
        self.select_firmware = QPushButton("Select firmware")
        self.select_dest = QPushButton("Select destination")
        self.select_flash = QPushButton("Flash")
        self.select_flash.setEnabled(False)

        logo_filename = "logo.png"

        try:
            with open(logo_filename):
                self.logo = QLabel(self)
                pixmap = QPixmap(logo_filename)
                self.logo.setPixmap(pixmap)
        except FileNotFoundError:
            print(f"Logo not found {logo_filename}")

        # Create layout and add widgets
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.logo)

        buttonLayout = QHBoxLayout()

        buttonLayout.addWidget(self.select_firmware)
        buttonLayout.addWidget(self.select_dest)
        buttonLayout.addWidget(self.select_flash)

        # Set layout
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        # Add button signals to slots
        self.select_firmware.clicked.connect(self.firmware_stuff)
        self.select_dest.clicked.connect(self.dest_stuff)
        self.select_flash.clicked.connect(self.flash_stuff)

    # do firmware stuff
    def firmware_stuff(self):
        print(f"in firmware_stuff")

        token = Github()
        asset_one = token.get_repo('meshtastic/Meshtastic-device').get_latest_release().get_assets()[1]
        print(f'asset_one:{asset_one}')

        latest_zip_file_url = asset_one.browser_download_url
        print(f'latest_zip_file_url:{latest_zip_file_url}')
        tmp = latest_zip_file_url.split('/')
        zip_file_name = tmp[-1]
        print(f'zip_file_name:{zip_file_name}')
        firmware_version = zip_file_name.replace("firmware-", "")
        firmware_version = firmware_version.replace(".zip", "")
        print(f"firmware_version:{firmware_version}")
        self.firmware_version = firmware_version

        # if the file is not already downloaded, download it
        if not os.path.exists(zip_file_name):
            print(f"Need to download...")
            urllib.request.urlretrieve(latest_zip_file_url, zip_file_name)
            print(f"done downloading")

        # unzip into directory named the same name as the firmware_version
        if not os.path.exists(firmware_version):
            print(f"Unzipping files now...")
            with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
                zip_ref.extractall(firmware_version)
            print(f"done unzipping")

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Firmware")
        dlg.setText("Downloaded latest firmware.")
        dlg.exec()

        # only enable Flash button if we have both values
        if self.port and self.firmware_version:
            self.select_flash.setEnabled(True)

    # do dest stuff
    def dest_stuff(self):
        print(f"in dest_stuff")

        ports = findPorts()
        print(f"ports:{ports}")
        if len(ports) == 1:
            self.port = ports[0]

            dlg = QMessageBox(self)
            dlg.setWindowTitle("Destination")
            dlg.setText(f"Will write to port:{self.port}")
            dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Destination")
            dlg.setText(f"Plugin a device")
            dlg.exec()

        # only enable Flash button if we have both values
        if self.port and self.firmware_version:
            self.select_flash.setEnabled(True)


    # do flash stuff
    def flash_stuff(self):
        print(f"in flash_stuff")

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Flash")
        dlg.setText("Going to flash you now")
        # TODO: change to OK/Cancel?
        dlg.exec()

        command = ["--baud", self.speed, "--port", self.port, "erase_flash"]
        print('ESPTOOL Using command %s' % ' '.join(command))
        esptool.main(command)

        system_info_file = f"{self.firmware_version}/system-info.bin"
        command = ["--baud", self.speed, "--port", self.port, "write_flash", "0x1000", system_info_file]
        print('ESPTOOL Using command %s' % ' '.join(command))
        esptool.main(command)

        bin_file = f"{self.firmware_version}/spiffs-{self.firmware_version}.bin"
        command = ["--baud", self.speed, "--port", self.port, "write_flash", "0x00390000", bin_file]
        print('ESPTOOL Using command %s' % ' '.join(command))
        esptool.main(command)

        # TODO: other command
        #return_value, out = subprocess.getstatusoutput('python3 -m esptool write_flash 0x10000 {TODO_filename}')

        # TODO: how to know if successful?
        esptool_successful = True

        if esptool_successful:
            dlg2 = QMessageBox(self)
            dlg2.setWindowTitle("Flashed")
            dlg2.setText("Done")
            dlg2.exec()
        # TODO: there should be an else


if __name__ == '__main__':

    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec())
