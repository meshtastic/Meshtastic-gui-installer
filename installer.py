#!/usr/bin/env python3
""" installer for Meshtastic firmware (aka "Meshtastic flasher")
"""

import os
import sys
import urllib
import ssl
import zipfile
import re

import esptool

from meshtastic.util import findPorts
from github import Github
from PySide6 import QtCore
from PySide6.QtGui import (QPixmap, QIcon, QPainter)
from PySide6.QtWidgets import (QPushButton, QApplication,
                               QVBoxLayout, QHBoxLayout, QDialog, QLabel,
                               QMessageBox, QComboBox, QProgressBar)
from qt_material import apply_stylesheet

VERSION="1.0.16"

MESHTASTIC_LOGO_FILENAME = "logo.png"
MESHTASTIC_COLOR_DARK = "#2C2D3C"
MESHTASTIC_COLOR_GREEN = "#67EA94"

MESHTATIC_REPO = 'meshtastic/Meshtastic-device'

# see https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def get_path(filename):
    """return the path to the logo file"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return filename

def populate_tag_in_firmware_dropdown(tag):
    """Populate this tag in the firmware dropdown?"""
    retval = False
    # TODO: better way?
    if re.search(r"v1.2.5[2-9]", tag):
        retval = True
    print(f'tag:{tag} populate in dropdown?:{retval}')
    return retval

class Form(QDialog):
    """Main application"""

    def __init__(self, parent=None):
        """constructor"""
        super(Form, self).__init__(parent)

        self.port = None
        self.speed = '921600'
        self.firmware_version = None
        self.firmware_versions = {}
        self.devices = None

        self.setWindowTitle("Meshtastic Flasher")

        # Create widgets
        self.select_firmware = QPushButton("Select Firmware")
        self.select_firmware.setToolTip("Click to check for more recent firmware.")

        self.select_firmware_version = QComboBox()
        self.select_firmware_version.setToolTip("Select which firmware to flash.")
        self.select_firmware_version.setMinimumContentsLength(18)
        self.select_firmware_version.hide()

        self.select_port = QPushButton("Select Port")
        self.select_port.setToolTip("Click to detect port.")

        self.select_device = QComboBox()
        self.select_device.setToolTip("You must Select firmware before you can select the device.")
        self.select_device.setMinimumContentsLength(17)

        self.select_flash = QPushButton("Flash")
        self.select_flash.setToolTip("Click to flash the firmware. If button is not enabled, need to click the buttons to the left.")
        self.select_flash.setEnabled(False)

        self.progress = QProgressBar()
        self.progress.setToolTip("Progress will be shown during the Flash step.")

        self.logo = QLabel(self)
        self.logo.setToolTip("This is the Meshtastic logo. It represents the starting packets used in LoRa transmissions.")
        pixmap = QPixmap(512, 512)
        pixmap.load(get_path(MESHTASTIC_LOGO_FILENAME))
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        
        # Create layout and add widgets
        main_layout = QVBoxLayout()
        
        if self.logo:
            main_layout.addWidget(self.logo)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_firmware)
        button_layout.addWidget(self.select_firmware_version)
        button_layout.addWidget(self.select_port)
        button_layout.addWidget(self.select_device)
        button_layout.addWidget(self.select_flash)

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progress)

        # Set layout
        main_layout.addLayout(button_layout)
        main_layout.addLayout(progress_layout)
        self.setLayout(main_layout)

        # Add button signals to slots
        self.select_firmware.clicked.connect(self.download_firmware_versions)
        self.select_port.clicked.connect(self.port_stuff)
        self.select_flash.clicked.connect(self.flash_stuff)

    def download_firmware_versions(self):
        """Download versions from GitHub"""

        # save first_tag in case we need to populate list with *some* value
        first_tag = None
        first_id = None

        if not self.select_firmware.isHidden():

            try:
                token = Github()
                repo = token.get_repo(MESHTATIC_REPO)
                releases = repo.get_releases()
                #print(f'releases:{releases}')
                count = 0
                for release in releases:
                    r = repo.get_release(release.id)
                    if not first_tag:
                        first_tag = r.tag_name
                        first_id = release.id
                    #print(f'r:{r} release.id:{release.id} tag_name:{r.tag_name} count:{count}')
                    if populate_tag_in_firmware_dropdown(r.tag_name):
                        # add tags to drop down
                        self.select_firmware_version.addItem(r.tag_name)
                        self.firmware_versions[r.tag_name] = release.id
                    count = count + 1
                    # simple check to make sure we don't get too many versions
                    if count > 5:
                        break

# get latest
#                asset_one = token.get_repo('meshtastic/Meshtastic-device').get_latest_release().get_assets()[1]
#                print(f'asset_one:{asset_one}')
#                latest_zip_file_url = asset_one.browser_download_url
#                print(f'latest_zip_file_url:{latest_zip_file_url}')
#                tmp = latest_zip_file_url.split('/')
#                zip_file_name = tmp[-1]
#                print(f'zip_file_name:{zip_file_name}')
            except Exception as e:
                print(e)

            # in development, hit this exception:
            #    github.GithubException.RateLimitExceededException: 403 {"message": "API rate limit exceeded for <IP redacted>. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)", "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"}
        else:
            self.select_device.setToolTip("Select your Meshtastic device.")

        if self.select_firmware_version.count() == 0:
            if first_tag:
                # huh, no versions are acceptable? check the populate method
                print('Warning: No versions pass our popluate check.')
                self.select_firmware_version.addItem(first_tag)
                self.firmware_versions[first_tag] = first_id
            else:
                # there was a problem, so just set it to this "latest" (at the time of writing)
                print('Warning: Had to fall back to a hard coded version/id.')
                fall_back_tag = 'v1.2.53.19c1f9f'
                self.select_firmware_version.addItem(fall_back_tag)
                self.firmware_versions[fall_back_tag] = '58155501'

        # if we checked for latest versions, so hide the "Firmware" button, and show the combo box to select version
        self.select_firmware.hide()
        self.select_firmware_version.show()

        # only enable Flash button if we have both values
        if self.port and self.firmware_version:
            self.select_flash.setEnabled(True)

    def port_stuff(self):
        """Detect port"""
        ports = findPorts()
        print(f"ports:{ports}")

        # also, see if we need to download the zip file

        # zip filename from tag
        tmp_tag = self.select_firmware_version.currentText()
        tmp_id = self.firmware_versions[tmp_tag]
        print(f'tmp_tag:{tmp_tag} tmp_id:{tmp_id}')
        zip_file_name = "firmware-"
        zip_file_name += tmp_tag[1:] # drop the leading "v"
        zip_file_name += ".zip"
        print(f'zip_file_name:{zip_file_name}')

        # this is really only for testing.. TODO: remove?
#        if not zip_file_name:
#            # look in current dir for zip files
#            # and set zip_file_name to first zip we find (just for testing)
#            filenames = next(os.walk("."), (None, None, []))[2]
#            for filename in filenames:
#                #print(f"filename:{filename}")
#                if filename.endswith(".zip"):
#                    zip_file_name = filename
#                    break

        if not zip_file_name:
            print("We should have a zip_file_name.")
            sys.exit(1)

        # TODO: can prob simplify this
        firmware_version = zip_file_name.replace("firmware-", "")
        firmware_version = firmware_version.replace(".zip", "")
        print(f"firmware_version:{firmware_version}")
        self.firmware_version = firmware_version

        # if the file is not already downloaded, download it
        if not os.path.exists(zip_file_name):
            print("Need to download...")

            # TODO: just found out you can get by tag... do not need the collection

            # get the url from the release
            # TODO: commented out because I'm tired of GitHub rate limiting me during development.
#            token = Github()
#            repo = token.get_repo(MESHTATIC_REPO)
#            r = repo.get_release(tmp_id)
#            print(f'r:{r}')
#            print(f'r.assets:{r.assets}')
#            print(f'r.assets[0]:{r.assets[0]}')
#            print(f'r.assets[0]["browser_download_url"]:{r.assets[0]["browser_download_url"]}')
#            # TODO: figure this out
#            zip_file_url = r.assets[0].browser_download_url
            # TODO: for now
            zip_file_url = 'https://github.com/meshtastic/Meshtastic-device/releases/download/v1.2.53.19c1f9f/firmware-1.2.53.19c1f9f.zip'
            print('zip_file_url:{zip_file_url}')

            if not zip_file_url:
                print("We should have a zip_file_url.")
                sys.exit(1)

            # TODO: do we care about ssl
            ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve(zip_file_url, zip_file_name)
            print("done downloading")

        # unzip into directory named the same name as the firmware_version
        if not os.path.exists(firmware_version):
            print("Unzipping files now...")
            with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
                zip_ref.extractall(firmware_version)
            print("done unzipping")

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

        # deal with weird TLora (single device connected, but shows up as 2 ports)
        # ports:['/dev/cu.usbmodem533C0052151', '/dev/cu.wchusbserial533C0052151']
        # ports:['/dev/cu.usbmodem11301', '/dev/cu.wchusbserial11301']
        if len(ports) == 2:
            first = ports[0].replace("usbmodem", "")
            second = ports[1].replace("wchusbserial", "")
            if first == second:
                self.port = ports[1]

        if len(ports) == 1:
            self.port = ports[0]

        if self.port:
            self.select_port.setText(f"Port:{self.port}")
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Port")
            dlg.setText("Plugin a device")
            dlg.exec()

        # only enable Flash button if we have both values
        if self.port and self.firmware_version:
            self.select_flash.setEnabled(True)
            self.select_flash.setToolTip('Click the Flash button to write to the device.')


    # do flash stuff
    def flash_stuff(self):
        """Do the flash parts"""
        proceed = False

        reply = QMessageBox.question(self, 'Flash', 'Are you sure you want to flash?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            proceed = True

        if proceed:
            QApplication.processEvents()

            command = ["--baud", self.speed, "--port", self.port, "erase_flash"]
            print(f"ESPTOOL Using command:{' '.join(command)}")
            esptool.main(command)
            self.progress.setValue(25)
            QApplication.processEvents()

            system_info_file = f"{self.firmware_version}/system-info.bin"
            command = ["--baud", self.speed, "--port", self.port, "write_flash", "0x1000", system_info_file]
            print(f"ESPTOOL Using command:{' '.join(command)}")
            esptool.main(command)
            self.progress.setValue(50)
            QApplication.processEvents()

            bin_file = f"{self.firmware_version}/spiffs-{self.firmware_version}.bin"
            command = ["--baud", self.speed, "--port", self.port, "write_flash", "0x00390000", bin_file]
            print(f"ESPTOOL Using command:{' '.join(command)}")
            esptool.main(command)
            self.progress.setValue(75)
            QApplication.processEvents()

            device_file = f"{self.firmware_version}/firmware-{self.select_device.currentText()}-{self.firmware_version}.bin"
            command = ["--baud", self.speed, "--port", self.port, "write_flash", "0x10000", device_file]
            print(f"ESPTOOL Using command:{' '.join(command)}")
            esptool.main(command)
            self.progress.setValue(100)
            QApplication.processEvents()

            # TODO: how to know if successful?
            esptool_successful = True

            if esptool_successful:
                dlg2 = QMessageBox(self)
                dlg2.setStyleSheet(f"background-color: {MESHTASTIC_COLOR_DARK}")
                dlg2.setWindowTitle("Flashed")
                dlg2.setText("Done")
                dlg2.exec()
            # TODO: there should be an else


if __name__ == '__main__':

    # Create the Qt Application
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_path(MESHTASTIC_LOGO_FILENAME)))
    apply_stylesheet(app, theme='dark_teal.xml')

    # Create and show the form
    form = Form()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec())
