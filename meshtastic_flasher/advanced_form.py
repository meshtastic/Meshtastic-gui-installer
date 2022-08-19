"""class for the Advanced options form"""

import datetime
import glob
import os
import shutil
import sys

from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox, QFormLayout, QFileDialog, QMessageBox

from meshtastic.__main__ import main

from meshtastic_flasher.info_form import InfoForm
from meshtastic_flasher.send_text_form import SendTextForm


class AdvancedForm(QDialog):
    """Advanced options form"""

    def __init__(self, parent=None):
        """constructor"""
        super(AdvancedForm, self).__init__(parent)

        self.parent = parent
        self.main = parent.main
        self.info_form = InfoForm(self)
        self.send_text_form = SendTextForm(self)

        width = 240
        height = 120
        self.setMinimumSize(width, height)
        self.setWindowTitle(self.main.text('advanced_options'))

        # Create widgets
        self.update_only_cb = QCheckBox()
        self.update_only_cb.setToolTip(self.main.tooltip('update_only'))
        self.info_button = QPushButton(self.main.text('information'))
        self.info_button.clicked.connect(self.info)
        self.send_text_button = QPushButton(self.main.text("send_text"))
        self.send_text_button.clicked.connect(self.send_text)
        # self.configure_from_file_button = QPushButton(self.main.text('configure_from_file'))
        # self.configure_from_file_button.clicked.connect(self.configure_from_file)
        # self.export_configuration_button = QPushButton(self.main.text('export_configuration'))
        # self.export_configuration_button.clicked.connect(self.export_configuration)
        self.clear_firmware_files_button = QPushButton(self.main.text('clear_firmware_files'))
        self.clear_firmware_files_button.clicked.connect(self.clear_firmware_files)

        self.ok_button = QPushButton("OK")

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.main.text('update_only'), self.update_only_cb)
        form_layout.addRow("", self.info_button)
        form_layout.addRow("", self.send_text_button)
        # form_layout.addRow("", self.export_configuration_button)
        # form_layout.addRow("", self.configure_from_file_button)
        form_layout.addRow("", self.clear_firmware_files_button)
        form_layout.addRow("", self.ok_button)
        self.setLayout(form_layout)

        self.ok_button.clicked.connect(self.close_advanced_options)


    def close_advanced_options(self):
        """Close the advanced options form"""
        print('OK button was clicked in advanced options')
        self.close()


    def configure_from_file(self):
        """Configure from file"""
        print('configure from file clicked')
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "YAML Files (*.yaml *.yml);;" "All Files (*.*)")
        if filename:
            old_sys_argv = sys.argv
            sys.argv = ['', '--configure', filename]
            main()
            sys.argv = old_sys_argv
            QMessageBox.information(self, self.main.text('info'), self.main.text('device_configured_from_file'))


    def export_configuration(self):
        """Export configuration"""
        print('export configuration clicked')
        now = datetime.datetime.now()
        now_formatted = now.strftime("%Y%m%d_%H%M%S")
        filename = f'{now_formatted}_backup.yaml'
        print(f'filename:{filename}')
        old_sys_argv = sys.argv
        old_sys_stdout = sys.stdout
        # pylint: disable=consider-using-with
        sys.stdout = open(filename, 'w', encoding='utf-8')
        sys.argv = ['', '--export-config']
        try:
            main()
        except SystemExit:
            pass
        sys.stdout.close()
        sys.argv = old_sys_argv
        sys.stdout = old_sys_stdout
        QMessageBox.information(self, self.main.text('info'), self.main.text('device_backed_up_to_file'))


    def send_text(self):
        """send_text clicked"""
        self.send_text_form.run()


    def info(self):
        """meshtastic --info"""
        print('info clicked')
        self.info_form.text.clear()
        old_sys_argv = sys.argv
        old_sys_stdout = sys.stdout
        sys.stdout = self.info_form
        sys.argv = ['', '--info']
        try:
            main()
        except SystemExit:
            pass
        sys.argv = old_sys_argv
        sys.stdout = old_sys_stdout
        self.info_form.show()


    def clear_firmware_files(self):
        """clear firmware files"""
        print('clear firmware files')
        confirm_msg = self.main.text('confirm_remove_firmware_files')
        reply = QMessageBox.question(self, self.main.text('confirm'), confirm_msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("User confirmed they want remove the firmware files")
            directories = glob.glob('1.*.*.*')
            for directory in directories:
                print(f'removing directory:{directory}')
                shutil.rmtree(directory)
            files = glob.glob('firmware-*.zip')
            for file in files:
                print(f'removing file:{file}')
                os.remove(file)
            # clean up the firmware dropdown
            if self.parent:
                self.parent.firmware_version = None
                self.parent.select_firmware_version.clear()
                self.parent.select_firmware_version.setDisabled(True)
        else:
            print("User does not want remove the firmware files")
