#!/usr/bin/env python3

import sys
import time
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
        asset_one = token.get_repo('meshtastic/Meshtastic-device').get_latest_release().get_assets()[0]
        print(f'asset_one:{asset_one}')


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
