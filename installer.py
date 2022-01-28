#!/usr/bin/env python3

import os
import sys
import time
import urllib
from github import Github
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog, QLabel, QMessageBox)

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.setWindowTitle("Meshtastic Installer")

        # Create widgets
        self.select_firmware = QPushButton("Select firmware")
        self.select_dest = QPushButton("Select destination")
        self.select_flash = QPushButton("Flash")

        logo_filename = "logo.png"

        try:
            with open(logo_filename):
                self.logo = QLabel(self)
                pixmap = QPixmap(logo_filename)
                self.logo.setPixmap(pixmap)
        except FileNotFoundError:
            print(f"Logo not found {logo_filename}")

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.logo)
        layout.addWidget(self.select_firmware)
        layout.addWidget(self.select_dest)
        layout.addWidget(self.select_flash)

        # Set dialog layout
        self.setLayout(layout)

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

        # if the file is not already downloaded, download it
        if not os.path.exists(zip_file_name):
            urllib.request.urlretrieve(latest_zip_file_url, zip_file_name)

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Firmware")
        dlg.setText("hello from firmware")
        dlg.exec()

    # do dest stuff
    def dest_stuff(self):
        print(f"in dest_stuff")

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Destination")
        dlg.setText("hello from destination")
        dlg.exec()

    # do flash stuff
    def flash_stuff(self):
        print(f"in flash_stuff")

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Flash")
        dlg.setText("hello from flash")
        dlg.exec()

if __name__ == '__main__':

    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec())
