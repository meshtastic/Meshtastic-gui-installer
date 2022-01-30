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

from meshtastic.util import detect_supported_devices, findPorts, detect_windows_needs_driver
from meshtastic.supported_device import active_ports_on_supported_devices
from github import Github
from PySide6 import QtCore
from PySide6.QtGui import (QPixmap, QIcon)
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
        self.devices = None

        self.setWindowTitle("Meshtastic Flasher")

        # Create widgets
        self.select_firmware = QPushButton("SELECT FIRMWARE")
        self.select_firmware.setToolTip("Click to check for more recent firmware.")

        self.select_firmware_version = QComboBox()
        self.select_firmware_version.setToolTip("Select which firmware to flash.")
        self.select_firmware_version.setMinimumContentsLength(18)
        self.select_firmware_version.hide()

        self.select_detect = QPushButton("DETECT")
        self.select_detect.setToolTip("Click to detect supported device and port info.")
        # Note: The text of the buttons is done in the styles, need to override it
        self.select_detect.setStyleSheet("text-transform: none")

        self.select_port = QComboBox()
        self.select_port.setToolTip("Select which port to use.")
        self.select_port.setMinimumContentsLength(25)
        self.select_port.setDisabled(True)

        self.select_device = QComboBox()
        self.select_device.setToolTip("You must click SELECT FIRMWARE before you can select the device.")
        self.select_device.setMinimumContentsLength(17)
        self.select_device.setDisabled(True)

        self.select_flash = QPushButton("FLASH")
        self.select_flash.setToolTip("Click to flash the firmware. If button is not enabled, need to click the buttons to the left.")
        self.select_flash.setEnabled(False)

        self.progress = QProgressBar()
        self.progress.setToolTip("Progress will be shown during the Flash step.")
        self.progress.hide()

        self.logo = QLabel(self)
        self.logo.setToolTip("This is the Meshtastic logo. It represents the starting packets used in LoRa transmissions.")
        pixmap = QPixmap(get_path(MESHTASTIC_LOGO_FILENAME))
        self.logo.setPixmap(pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        style_for_logo = (f"background-color: {MESHTASTIC_COLOR_GREEN}; border-color: "
                          f"{MESHTASTIC_COLOR_GREEN}; border-radius: 0px; color: {MESHTASTIC_COLOR_DARK};")
        self.logo.setStyleSheet(style_for_logo)

        # Create layout and add widgets
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0)
        if self.logo:
            main_layout.addWidget(self.logo)
        main_layout.addStretch(1)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.select_firmware)
        button_layout.addWidget(self.select_firmware_version)
        button_layout.addWidget(self.select_detect)
        button_layout.addWidget(self.select_port)
        button_layout.addWidget(self.select_device)
        button_layout.addWidget(self.select_flash)
        button_layout.addStretch(1)
        button_layout.setContentsMargins(20, 20, 20, 20)

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progress)
        button_layout.addStretch(1)

        # Set layout
        main_layout.addLayout(button_layout)
        main_layout.addLayout(progress_layout)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        # Add button signals to slots
        self.select_firmware.clicked.connect(self.download_firmware_versions)
        self.select_detect.clicked.connect(self.detect)
        self.select_flash.clicked.connect(self.flash_stuff)

    def download_firmware_versions(self):
        """Download versions from GitHub"""

        # save first_tag in case we need to populate list with *some* value
        first_tag = None

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
                    #print(f'r:{r} release.id:{release.id} tag_name:{r.tag_name} count:{count}')
                    if populate_tag_in_firmware_dropdown(r.tag_name):
                        # add tags to drop down
                        self.select_firmware_version.addItem(r.tag_name)
                    count = count + 1
                    # simple check to make sure we don't get too many versions
                    if count > 5:
                        break

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
            else:
                # there was a problem, so just set it to this "latest" (at the time of writing)
                print('Warning: Had to fall back to a hard coded version/id.')
                fall_back_tag = 'v1.2.53.19c1f9f'
                self.select_firmware_version.addItem(fall_back_tag)

        # if we checked for latest versions, so hide the "Firmware" button, and show the combo box to select version
        self.select_firmware.hide()
        self.select_firmware_version.show()

        # only enable Flash button if we have both values
        if self.select_port.count() > 0 and self.firmware_version:
            self.select_flash.setEnabled(True)

    def detect(self):
        """Detect port, download zip file from github if we need to, and unzip it"""

        # detect supported devices
        supported_devices_detected = detect_supported_devices()
        if len(supported_devices_detected) == 0:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("No devices detected.")
            dlg.setText("Plugin a device?")
            dlg.exec()
            # TODO: enumerate devices from the files?
        else:
            if len(supported_devices_detected) > 0:
                self.select_device.clear()
                for device in supported_devices_detected:
                    self.select_device.addItem(device.for_firmware)

        # detect which ports and populate the dropdown
        ports = active_ports_on_supported_devices(supported_devices_detected)
        #print(f"from active_ports_on_supported_devices() ports:{ports}")
        ports_sorted = list(ports)
        ports_sorted.sort()
        for port in ports_sorted:
            self.select_port.addItem(port)

        # our auto-detect did not work
        if len(ports) == 0:
            print("Warning: Could not find any ports using the autodetection method.")

            # for now, use the Serial method to discover ports
            ports = findPorts()
            #print(f"from findPorts() ports:{ports}")
            if len(ports) == 0:
                print("Warning: Could not find any ports using the Serial library method.")

                for device in supported_devices_detected:
                    detect_windows_needs_driver(device, True)
            else:
                for port in ports:
                    self.select_port.addItem(port)

        # TODO: self.firmware_version and checking if we need to download should be in a "changed" method
        # also, see if we need to download the zip file
        self.firmware_version = self.select_firmware_version.currentText()[1:] # drop leading v
        print(f"self.firmware_version:{self.firmware_version}")

        # zip filename from tag
        zip_file_name = "firmware-"
        zip_file_name += self.firmware_version
        zip_file_name += ".zip"
        print(f'zip_file_name:{zip_file_name}')

        if not zip_file_name:
            print("We should have a zip_file_name.")
            sys.exit(1)

        # if the file is not already downloaded, download it
        if not os.path.exists(zip_file_name):
            print("Need to download...")

            # Note: Probably should use the browser_download_url
            zip_file_url = f'https://github.com/meshtastic/Meshtastic-device/releases/download/v{self.firmware_version}/firmware-{self.firmware_version}.zip'
            # This is in case we have to temp-disable GitHub during dev due to rate-limiting.
            #zip_file_url = 'https://github.com/meshtastic/Meshtastic-device/releases/download/v1.2.53.19c1f9f/firmware-1.2.53.19c1f9f.zip'
            print(f'zip_file_url:{zip_file_url}')

            if not zip_file_url:
                print("We should have a zip_file_url.")
                sys.exit(1)

            # TODO: do we care about ssl
            print("downloading...")
            ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve(zip_file_url, zip_file_name)
            print("done downloading")

        # unzip into directory named the same name as the firmware_version
        if not os.path.exists(self.firmware_version):
            print("Unzipping files now...")
            with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
                zip_ref.extractall(self.firmware_version)
            print("done unzipping")

        # populate the devices
        if not self.devices:
            filenames = next(os.walk(self.firmware_version), (None, None, []))[2]
            filenames.sort()
#            self.select_device.clear()
#            for filename in filenames:
#                #print(f"filename:{filename}")
#                if filename.startswith("firmware-") and filename.endswith(".bin"):
#                    device = filename.replace("firmware-", "")
#                    device = device.replace(f"-{self.firmware_version}", "")
#                    device = device.replace(".bin", "")
#                    self.select_device.addItem(device)

        # deal with weird TLora (single device connected, but shows up as 2 ports)
        # ports:['/dev/cu.usbmodem533C0052151', '/dev/cu.wchusbserial533C0052151']
        # ports:['/dev/cu.usbmodem11301', '/dev/cu.wchusbserial11301']
        # TODO: add this back in later
#        if len(ports) == 2:
#            first = ports[0].replace("usbmodem", "")
#            second = ports[1].replace("wchusbserial", "")
#            if first == second:
#                self.port = ports[1]

        # only enable Flash button and Device dropdown if we have firmware and ports
        if self.select_port.count() > 0 and self.firmware_version:
            self.select_flash.setEnabled(True)
            self.select_flash.setToolTip('Click the Flash button to write to the device.')
            self.select_detect.hide()
            self.select_port.setDisabled(False)
            self.select_device.setDisabled(False)


    # do flash stuff
    def flash_stuff(self):
        """Do the flash parts"""
        proceed = False

        # TODO: what happens if they change version after DETECT was pressed?

        self.port = self.select_port.currentText()

        confirm_msg = f'Are you sure you want to flash:\n{self.firmware_version}\n'
        confirm_msg += f'{self.port}\n{self.select_device.currentText()}?'
        reply = QMessageBox.question(self, 'Flash', confirm_msg,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            proceed = True

        if proceed:
            QApplication.processEvents()
            self.progress.show()
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
    app.setApplicationName("Meshtastic Flasher")
    apply_stylesheet(app, theme='meshtastic_theme.xml')

    # Create and show the form
    form = Form()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec())
