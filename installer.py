#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # Create widgets
        self.select_firmware = QPushButton("Select firmware")
        self.select_dest = QPushButton("Select destination")
        self.select_flash = QPushButton("Flash")

        # Create layout and add widgets
        layout = QVBoxLayout()
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

    # do dest stuff
    def dest_stuff(self):
        print(f"in dest_stuff")

    # do flash stuff
    def flash_stuff(self):
        print(f"in flash_stuff")

if __name__ == '__main__':

    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the form
    form = Form()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec())
