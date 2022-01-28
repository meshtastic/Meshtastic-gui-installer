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
    QVBoxLayout, QHBoxLayout, QDialog, QLabel, QMessageBox, QComboBox)

version="1.0.3"

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.port = None
        self.speed = '921600'
        self.firmware_version = None
        self.devices = None

        self.setWindowTitle("Meshtastic Installer")

        # Create widgets
        self.select_firmware = QPushButton("Select firmware")

        self.select_port = QPushButton("Port")

        self.select_device = QComboBox()
        self.select_device.currentIndexChanged.connect(self.selection_change)

        self.select_flash = QPushButton("Flash")
        self.select_flash.setEnabled(False)

        logo_filename = "./logo.png"

        self.logo = None
        try:
            with open(logo_filename):
                self.logo = QLabel(self)
                pixmap = QPixmap(logo_filename)
                self.logo.setPixmap(pixmap)
        except FileNotFoundError:
            print(f"Logo not found {logo_filename}")

        # Create layout and add widgets
        mainLayout = QVBoxLayout()

        if self.logo:
            mainLayout.addWidget(self.logo)

        buttonLayout = QHBoxLayout()

        buttonLayout.addWidget(self.select_firmware)
        buttonLayout.addWidget(self.select_port)
        buttonLayout.addWidget(self.select_device)
        buttonLayout.addWidget(self.select_flash)

        # Set layout
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        # Add button signals to slots
        self.select_firmware.clicked.connect(self.firmware_stuff)
        self.select_port.clicked.connect(self.port_stuff)
        self.select_flash.clicked.connect(self.flash_stuff)

    # for combo box
    def selection_change(self, i):
        print(f"Devices are:")
        for count in range(self.select_device.count()):
            print(f"{self.select_device.itemText(count)}")
        print(f"Current index:{i} current:{self.select_device.currentText()}")

    # do firmware stuff
    def firmware_stuff(self):
        print(f"in firmware_stuff")

        zip_file_name = None
        try:
            token = Github()
            asset_one = token.get_repo('meshtastic/Meshtastic-device').get_latest_release().get_assets()[1]
            print(f'asset_one:{asset_one}')
            latest_zip_file_url = asset_one.browser_download_url
            print(f'latest_zip_file_url:{latest_zip_file_url}')
            tmp = latest_zip_file_url.split('/')
            zip_file_name = tmp[-1]
            print(f'zip_file_name:{zip_file_name}')
        except:
            pass

        # in development, hit this exception:
        #    github.GithubException.RateLimitExceededException: 403 {"message": "API rate limit exceeded for <IP redacted>. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)", "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"}

        if not zip_file_name:
            # look in current dir for zip files
            # and set zip_file_name to first zip we find (just for testing)
            filenames = next(os.walk("."), (None, None, []))[2]
            for filename in filenames:
                #print(f"filename:{filename}")
                if filename.endswith(".zip"):
                    zip_file_name = filename
                    break

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

        # populate the devices
        if not self.devices:
            filenames = next(os.walk(self.firmware_version), (None, None, []))[2]
            filenames.sort()
            for filename in filenames:
                #print(f"filename:{filename}")
                if filename.startswith("firmware-") and filename.endswith(".bin"):
                    print(f"firmware only filename:{filename}")

                    device = filename.replace("firmware-", "")
                    device = device.replace(f"-{self.firmware_version}", "")
                    device = device.replace(".bin", "")
                    print(f"device:{device}")
                    self.select_device.addItem(device)

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Firmware")
        dlg.setText("Downloaded latest firmware.")
        dlg.exec()

        # only enable Flash button if we have both values
        if self.port and self.firmware_version:
            self.select_flash.setEnabled(True)

    # do port stuff
    def port_stuff(self):
        print(f"in port_stuff")

        ports = findPorts()
        print(f"ports:{ports}")
        if len(ports) == 1:
            self.port = ports[0]

            dlg = QMessageBox(self)
            dlg.setWindowTitle("Port")
            dlg.setText(f"Will write to port:{self.port}")
            dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Port")
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

        device_file = f"{self.firmware_version}/firmware-{self.select_device.currentText()}-{self.firmware_version}.bin"
        command = ["--baud", self.speed, "--port", self.port, "write_flash", "0x10000", device_file]
        print('ESPTOOL Using command %s' % ' '.join(command))
        esptool.main(command)

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
