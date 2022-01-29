#!/usr/bin/env python3

import os
import sys
import time
import urllib
import ssl
import subprocess
import zipfile
import time

import esptool

from meshtastic.util import findPorts
from github import Github
from PySide6.QtGui import (QPixmap, QIcon)
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QHBoxLayout, QDialog, QLabel,
                               QMessageBox, QComboBox, QProgressBar)
from qt_material import apply_stylesheet

version="1.0.6"

meshtastic_logo_filename = "logo.png"
meshtastic_color_dark = "#2C2D3C"
meshtastic_color_green = "#67EA94"

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.port = None
        self.speed = '921600'
        self.firmware_version = None
        self.devices = None

        #self.setStyleSheet(f"background-color: {meshtastic_color_dark};")
        self.setWindowTitle("Meshtastic Installer")


        # Create widgets
        self.select_firmware = QPushButton("Select firmware")

        self.select_port = QPushButton("Port")

        self.select_device = QComboBox()

        self.select_flash = QPushButton("Flash")
        self.select_flash.setEnabled(False)

        self.progress = QProgressBar()


        self.logo = None
        try:
            with open(meshtastic_logo_filename):
                self.logo = QLabel(self)
                pixmap = QPixmap(meshtastic_logo_filename)
                self.logo.setPixmap(pixmap)
            self.setWindowIcon(QIcon(meshtastic_logo_filename))

        except FileNotFoundError:
            print(f"Logo not found {meshtastic_logo_filename}")

        # Create layout and add widgets
        mainLayout = QVBoxLayout()

        if self.logo:
            mainLayout.addWidget(self.logo)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.select_firmware)
        buttonLayout.addWidget(self.select_port)
        buttonLayout.addWidget(self.select_device)
        buttonLayout.addWidget(self.select_flash)

        progressLayout = QHBoxLayout()
        progressLayout.addWidget(self.progress)

        # Set layout
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(progressLayout)
        self.setLayout(mainLayout)

        # Add button signals to slots
        self.select_firmware.clicked.connect(self.firmware_stuff)
        self.select_port.clicked.connect(self.port_stuff)
        self.select_flash.clicked.connect(self.flash_stuff)


    def aboutAction(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("About")
        dlg.setText("This is info about this program.")
        dlg.exec()

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

        if not zip_file_name:
            print("We should have a zip_file_name.")
            sys.exit(1)

        firmware_version = zip_file_name.replace("firmware-", "")
        firmware_version = firmware_version.replace(".zip", "")
        print(f"firmware_version:{firmware_version}")
        self.firmware_version = firmware_version

        # if the file is not already downloaded, download it
        if not os.path.exists(zip_file_name):
            print(f"Need to download...")
            # TODO: do we care about ssl
            ssl._create_default_https_context = ssl._create_unverified_context
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
            self.select_device.clear()
            for filename in filenames:
                #print(f"filename:{filename}")
                if filename.startswith("firmware-") and filename.endswith(".bin"):

                    device = filename.replace("firmware-", "")
                    device = device.replace(f"-{self.firmware_version}", "")
                    device = device.replace(".bin", "")
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

        dlg = QMessageBox(self)
        dlg.setStyleSheet(f"background-color: {meshtastic_color_green}")
        dlg.setWindowTitle("Destination")

        # deal with weird TLora (single device connected, but shows up as 2 ports)
        # ports:['/dev/cu.usbmodem533C0052151', '/dev/cu.wchusbserial533C0052151']
        # ports:['/dev/cu.usbmodem11301', '/dev/cu.wchusbserial11301']
        if len(ports) == 2:
            a = ports[0].replace("usbmodem", "")
            b = ports[1].replace("wchusbserial", "")
            if a == b:
                self.port = ports[1]

        if len(ports) == 1:
            self.port = ports[0]

        if self.port:
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

        proceed = False

        reply = QMessageBox.question(self, 'Flash', 'Are you sure you want to flash?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            proceed = True

        if proceed:
            QApplication.processEvents()

            command = ["--baud", self.speed, "--port", self.port, "erase_flash"]
            print('ESPTOOL Using command %s' % ' '.join(command))
            esptool.main(command)
            self.progress.setValue(25)
            QApplication.processEvents()

            system_info_file = f"{self.firmware_version}/system-info.bin"
            command = ["--baud", self.speed, "--port", self.port, "write_flash", "0x1000", system_info_file]
            print('ESPTOOL Using command %s' % ' '.join(command))
            esptool.main(command)
            self.progress.setValue(50)
            QApplication.processEvents()

            bin_file = f"{self.firmware_version}/spiffs-{self.firmware_version}.bin"
            command = ["--baud", self.speed, "--port", self.port, "write_flash", "0x00390000", bin_file]
            print('ESPTOOL Using command %s' % ' '.join(command))
            esptool.main(command)
            self.progress.setValue(75)
            QApplication.processEvents()

            device_file = f"{self.firmware_version}/firmware-{self.select_device.currentText()}-{self.firmware_version}.bin"
            command = ["--baud", self.speed, "--port", self.port, "write_flash", "0x10000", device_file]
            print('ESPTOOL Using command %s' % ' '.join(command))
            esptool.main(command)
            self.progress.setValue(100)
            QApplication.processEvents()

            # TODO: how to know if successful?
            esptool_successful = True

            if esptool_successful:
                dlg2 = QMessageBox(self)
                dlg2.setStyleSheet(f"background-color: {meshtastic_color_dark}")
                dlg2.setWindowTitle("Flashed")
                dlg2.setText("Done")
                dlg2.exec()
            # TODO: there should be an else


if __name__ == '__main__':

    # Create the Qt Application
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')

    # Create and show the form
    form = Form()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec())
