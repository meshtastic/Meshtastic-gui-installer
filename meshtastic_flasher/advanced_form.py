"""class for the Advanced options form"""

import datetime
import sys

from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox, QFormLayout, QFileDialog, QMessageBox

from meshtastic.__main__ import main

from meshtastic_flasher.info_form import InfoForm


class AdvancedForm(QDialog):
    """Advanced options form"""

    def __init__(self, parent=None):
        """constructor"""
        super(AdvancedForm, self).__init__(parent)

        self.info_form = InfoForm()

        width = 240
        height = 120
        self.setMinimumSize(width, height)
        self.setWindowTitle("Advanced Options")

        # Create widgets
        self.update_only_cb = QCheckBox()
        self.update_only_cb.setToolTip("If enabled, the device will be updated (not completely erased).")
        self.rak_bootloader_cb = QCheckBox()
        self.rak_bootloader_cb.setToolTip("If enabled, the NRF52 bootloader on RAK devices will be checked and updated in DETECT step.")
        self.info_button = QPushButton("INFO")
        self.info_button.clicked.connect(self.info)
        self.configure_from_file_button = QPushButton("Configure From File")
        self.configure_from_file_button.clicked.connect(self.configure_from_file)
        self.export_configuration_button = QPushButton("Export Configuration")
        self.export_configuration_button.clicked.connect(self.export_configuration)

        self.ok_button = QPushButton("OK")

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("&Update only"), self.update_only_cb)
        form_layout.addRow(self.tr("&RAK Bootloader Update"), self.rak_bootloader_cb)
        form_layout.addRow(self.tr(""), self.info_button)
        form_layout.addRow(self.tr(""), self.export_configuration_button)
        form_layout.addRow(self.tr(""), self.configure_from_file_button)
        form_layout.addRow(self.tr(""), self.ok_button)
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
            QMessageBox.information(self, "Info", f"Device configured from:{filename}")


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
        QMessageBox.information(self, "Info", f"Device configuration backed up to:{filename}")


    def info(self):
        """meshtastic --info"""
        print('info clicked')
        old_sys_argv = sys.argv
        old_sys_stdout = sys.stdout
        sys.stdout = self.info_form
        sys.argv = ['', '--info']
        try:
            main()
        except SystemExit:
            pass
        sys.argv = old_sys_argv
        #self.info_form.text.appendPlainText("hello")
        sys.stdout = old_sys_stdout
        self.info_form.show()
