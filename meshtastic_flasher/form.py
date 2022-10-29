"""Form for meshtastic-flasher"""

import os
import sys
import shutil
import ctypes
import glob
import platform
import urllib
import ssl
import re
import subprocess
import webbrowser
import zipfile
import psutil

import serial

from PySide6 import QtCore
from PySide6.QtGui import QPixmap, QCursor, QIcon
from PySide6.QtWidgets import (QPushButton, QApplication,
                               QVBoxLayout, QHBoxLayout, QDialog, QLabel,
                               QMessageBox, QComboBox, QProgressBar)

import meshtastic
import meshtastic.serial_interface
import meshtastic.util

from meshtastic_flasher.version import __version__
from meshtastic_flasher.advanced_form import AdvancedForm
from meshtastic_flasher.esptool_form import EsptoolForm
from meshtastic_flasher.settings import Settings
from meshtastic_flasher.radio_picker_form import RadioPickerForm
import meshtastic_flasher.util
from meshtastic_flasher.util import load_fields

MESHTASTIC_LOGO_FILENAME = "logo.png"
COG_FILENAME = "cog.svg"
OPTIONS_ICON_FILENAME = "options.svg"
HELP_FILENAME = "help.svg"
INFO_FILENAME = "info.svg"
BUTTON_ICON_SIZE = QtCore.QSize(24, 24)
BUTTON_ICON_SIZE_SMALL = QtCore.QSize(20, 20)

# windows does not like this one
if platform.system() == "Linux":
    import grp
    import getpass


MESHTASTIC_COLOR_DARK = "#2C2D3C"
MESHTASTIC_COLOR_GREEN = "#67EA94"


class Form(QDialog):
    """Main application"""

    def __init__(self, parent=None, lang='en'):
        """constructor"""
        super(Form, self).__init__(parent)
        self.parent = None
        self.main = self
        self.lang = lang
        self.port = None
        self.firmware_version = None
        self.nrf = False
        self.device = None
        self.update_only = None
        self.device_file = None
        self.ble_ota_file = None
        self.littlefs_file = None
        self.detected_meshtastic_version = None
        self.detected_list = []
        self.device_from_picker = None

        self.fields = load_fields()
        self.pixel_mult = 12

        self.advanced_form = AdvancedForm(self)
        self.esptool_form = EsptoolForm(self)
        self.settings = Settings(self)
        self.radio_picker_form = RadioPickerForm(self)

        update_available = ''
        if meshtastic_flasher.util.check_if_newer_version():
            update_available = f' *{self.main.text("update_available")}*'
        self.setWindowTitle(f"Meshtastic Flasher v{__version__}{update_available}")

        # Create widgets
        self.get_versions_button = QPushButton(f"1. {self.main.text('get_versions')}")
        self.get_versions_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.get_versions_button.setToolTip(self.main.tooltip('get_versions'))

        self.select_firmware_version = QComboBox()
        self.select_firmware_version.setToolTip(self.main.tooltip('select_firmware_version'))
        self.select_firmware_version.setMinimumContentsLength(18)
        self.select_firmware_version.setDisabled(True)

        self.select_detect = QPushButton(f"2. {self.main.text('select_detect')}")
        self.select_detect.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.select_detect.setToolTip(self.main.tooltip('select_detect'))
        # Note: The text of the buttons is done in the styles, need to override it
        self.select_detect.setStyleSheet("text-transform: none")

        self.select_language = QComboBox()
        self.select_language.setToolTip(self.main.tooltip('select_language'))
        self.select_language.setMinimumContentsLength(25)

        self.select_language.addItem("English", "en")
        self.populate_languages()

        self.help_button = QPushButton()
        help_icon = QIcon(meshtastic_flasher.util.get_path(HELP_FILENAME))
        self.help_button.setIcon(help_icon)
        self.help_button.setIconSize(BUTTON_ICON_SIZE_SMALL)
        self.help_button.setFixedSize(BUTTON_ICON_SIZE_SMALL)
        self.help_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.help_button.setStyleSheet("border:none")
        self.help_button.setToolTip(self.main.tooltip('help_button'))

        self.about_button = QPushButton()
        info_icon = QIcon(meshtastic_flasher.util.get_path(INFO_FILENAME))
        self.about_button.setIcon(info_icon)
        self.about_button.setIconSize(BUTTON_ICON_SIZE_SMALL)
        self.about_button.setFixedSize(BUTTON_ICON_SIZE_SMALL)
        self.about_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.about_button.setStyleSheet("border:none")
        self.about_button.setToolTip(self.main.tooltip('about_button'))

        self.select_port = QComboBox()
        self.select_port.setToolTip(self.main.tooltip('select_port'))
        self.select_port.setMinimumContentsLength(30)
        self.select_port.setDisabled(True)
        self.select_port.setDuplicatesEnabled(False)

        self.select_device = QComboBox()
        self.select_device.setToolTip(self.main.tooltip('select_device'))
        self.select_device.setMinimumContentsLength(17)
        self.select_device.setDisabled(True)

        self.select_flash = QPushButton("3. FLASH")
        self.select_flash.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.select_flash.setToolTip(self.main.tooltip('select_flash'))
        self.select_flash.setEnabled(False)

        self.progress = QProgressBar()
        self.progress.setToolTip(self.main.tooltip('progress'))
        self.progress.hide()

        self.logo = QLabel(self)
        pixmap = QPixmap(meshtastic_flasher.util.get_path(MESHTASTIC_LOGO_FILENAME))
        self.logo.setPixmap(pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        style_for_logo = (f"background-color: {MESHTASTIC_COLOR_GREEN}; border-color: "
                          f"{MESHTASTIC_COLOR_GREEN}; border-radius: 0px; color: {MESHTASTIC_COLOR_DARK};")
        self.logo.setStyleSheet(style_for_logo)

        # labels for over the drop downs/combo boxes
        #link_style = "color:#67EA94; font-weight: bold; text-decoration: underline"
        # this link_style gets added to tool tip too, which we do not want
        self.label_version = QLabel(self)
        self.label_version.setText(self.main.text('version'))
        #self.label_version.setStyleSheet(link_style)
        self.label_version.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.label_version.setToolTip(self.main.tooltip('label_version'))

        self.label_port = QLabel(self)
        self.label_port.setText(self.main.text('port'))

        self.label_device = QLabel(self)
        self.label_device.setText(self.main.text('device'))
        #self.label_device.setStyleSheet(link_style)
        self.label_device.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.label_device.setToolTip(self.main.tooltip('label_device'))

        self.label_detected_meshtastic_version = QLabel(self)
        self.label_detected_meshtastic_version.setText("")

        self.device_settings_button = QPushButton(self.main.text('device_settings'))
        cog_icon = QIcon(meshtastic_flasher.util.get_path(COG_FILENAME))
        self.device_settings_button.setIcon(cog_icon)
        self.device_settings_button.setIconSize(BUTTON_ICON_SIZE_SMALL)
        self.device_settings_button.setFixedHeight(20)
        self.device_settings_button.setStyleSheet("border:none")
        self.device_settings_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.device_settings_button.setToolTip(self.main.tooltip('device_settings_button'))

        self.advanced_options_button = QPushButton(self.main.text('advanced_options'))
        options_icon = QIcon(meshtastic_flasher.util.get_path(OPTIONS_ICON_FILENAME))
        self.advanced_options_button.setIcon(options_icon)
        self.advanced_options_button.setIconSize(BUTTON_ICON_SIZE_SMALL)
        self.advanced_options_button.setFixedHeight(20)
        self.advanced_options_button.setStyleSheet("border:none")
        self.advanced_options_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.advanced_options_button.setToolTip(self.main.tooltip('advanced_options'))

        # Create layout and add widgets
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        info_layout = QHBoxLayout()
        info_layout.addWidget(self.advanced_options_button, alignment=QtCore.Qt.AlignRight)
        info_layout.addStretch(1)
        info_layout.addWidget(self.device_settings_button, alignment=QtCore.Qt.AlignLeft)
        info_layout.addWidget(self.select_language, alignment=QtCore.Qt.AlignLeft)
        info_layout.addStretch(1)
        info_layout.addWidget(self.about_button)
        info_layout.addWidget(self.help_button)
        info_layout.setContentsMargins(0, 10, 10, 0)

        logo_layout = QVBoxLayout()
        if self.logo:
            logo_layout.addWidget(self.logo)

        detect_layout = QHBoxLayout()
        detect_layout.addStretch(1)
        detect_layout.addWidget(self.get_versions_button)
        detect_layout.addWidget(self.select_detect)
        detect_layout.setContentsMargins(0, 0, 0, 0)
        detect_layout.addStretch(1)

        label_layout = QHBoxLayout()
        label_layout.addWidget(self.label_version)
        label_layout.addStretch(1)
        label_layout.addWidget(self.label_port)
        label_layout.addStretch(1)
        label_layout.addWidget(self.label_device)
        label_layout.setContentsMargins(60, 0, 90, 0)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.select_firmware_version)
        button_layout.addWidget(self.select_port)
        button_layout.addWidget(self.select_device)
        button_layout.addStretch(1)
        button_layout.setContentsMargins(20, 0, 20, 0)

        flash_layout = QHBoxLayout()
        flash_layout.addStretch(1)
        flash_layout.addWidget(self.select_flash)
        flash_layout.addStretch(1)
        flash_layout.setContentsMargins(20, 0, 20, 20)

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progress)
        button_layout.addStretch(1)

        # Set layout
        main_layout.addLayout(info_layout)
        main_layout.addLayout(logo_layout)
        main_layout.addLayout(detect_layout)
        main_layout.addLayout(label_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(flash_layout)
        main_layout.addLayout(progress_layout)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        # move version
        self.label_detected_meshtastic_version.move(30, 300)
        self.label_detected_meshtastic_version.show()

        # Add button signals to slots
        self.get_versions_button.clicked.connect(self.get_versions)
        self.help_button.clicked.connect(self.help_message)
        self.about_button.clicked.connect(self.about_message)
        self.label_version.mousePressEvent = self.label_version_clicked
        self.label_device.mousePressEvent = self.label_device_clicked
        self.select_detect.clicked.connect(self.detect)
        self.select_flash.clicked.connect(self.flash_stuff)
        self.select_firmware_version.currentTextChanged.connect(self.on_select_firmware_changed)
        self.device_settings_button.mousePressEvent = self.run_device_settings
        self.advanced_options_button.mousePressEvent = self.run_advanced_options
        self.select_language.currentTextChanged.connect(self.on_select_language_changed)

        # pre-populate the versions that have already been downloaded and unzipped
        self.get_versions_from_disk()


    def get_field(self, field, key):
        """Return the value for a field"""
        retval = ""
        if self.fields:
            if field in self.fields:
                if key in self.fields[field]:
                    tmp = self.fields[field][key]
                    if isinstance(tmp, str):
                        # there are no translations
                        retval = self.fields[field][key]
                    else:
                        if self.lang in self.fields[field][key]:
                            # use their lang
                            retval = self.fields[field][key][self.lang]
                        else:
                            # fall back to english
                            retval = self.fields[field][key]['en']
        return retval

    def populate_languages(self):
        """Populate the languages dropdown.
           When adding a new language:
             1) add to and run: ./bin/translate_entries.py
             2) run "pip install ."
             3) add language to this list
        """
        self.select_language.addItem("Deutsch - German", "de")
        self.select_language.addItem("Español - Spanish", "es")
        self.select_language.addItem("Eesti - Estonian", "et")
        self.select_language.addItem("Français - French", "fr")
        self.select_language.addItem("Italiano - Italian", "it")
        self.select_language.addItem("Polski - Polish", "pl")
        self.select_language.addItem("中国 - Simplified Chinese", "zh")
        self.select_language.addItem("русский - Russian", "ru")
        self.select_language.addItem("日本語 - Japanese", "ja")
        self.select_language.addItem("Română - Romanian", "ro")
        index = self.select_language.findData(self.lang)
        self.select_language.setCurrentIndex(index)


    def text(self, field):
        """Return the text for a field"""
        return self.get_field(field, 'text')


    def tooltip(self, field):
        """Return the tooltip for a field"""
        return self.get_field(field, 'tooltip')


    def label(self, field):
        """Return the label for a field"""
        return self.get_field(field, 'label')


    def description(self, field):
        """Return the description for a field"""
        return self.get_field(field, 'description')


    def doc_url(self, field):
        """Return the doc_url enriched with html for a field"""
        retval = ""
        if self.fields:
            if field in self.fields:
                if 'doc_url' in self.fields[field]:
                    doc_url = self.fields[field]['doc_url']
                    retval = f"<a href='{doc_url}' style='color:#67EA94'>More info</a>"
        return retval


    def max_size(self, field):
        """Return the max_size for a field"""
        retval = 0
        if self.fields:
            if field in self.fields:
                if 'max_size' in self.fields[field]:
                    retval = self.fields[field]['max_size']
        return retval


    def keyPressEvent(self, event):
        """Deal with a key press"""
        if event.key() == QtCore.Qt.Key_A:
            print("A was pressed... showing advanced options form")
            self.advanced_form.show()
        elif event.key() == QtCore.Qt.Key_D:
            print("D was pressed...")
            self.detect()
        elif event.key() == QtCore.Qt.Key_G:
            print("G was pressed...")
            self.get_versions()
        elif event.key() == QtCore.Qt.Key_H:
            print("H was pressed...")
            self.hotkeys()
        elif event.key() == QtCore.Qt.Key_Q:
            print("Q was pressed... so quitting")
            self.accept()
        elif event.key() == QtCore.Qt.Key_T:
            print("T was pressed... so showing help message")
            self.help_message()
        elif event.key() == QtCore.Qt.Key_S:
            print("S was pressed... showing device settings form")
            self.run_device_settings(None)


    # pylint: disable=unused-argument
    def run_device_settings(self, event):
        """Run the device_settings form"""
        self.settings.run()


    # pylint: disable=unused-argument
    def run_advanced_options(self, event):
        """Run the advanced options form"""
        self.advanced_form.show()


    # pylint: disable=unused-argument
    def closeEvent(self, event):
        """Override the close event so the user can just click the close window in corner."""
        self.accept()


    def on_select_language_changed(self, value):
        """When the select_language drop down value is changed."""
        lang = self.select_language.currentData()
        #print(f'lang:{lang}')
        #print(f'sys.argv:{sys.argv}')
        if len(sys.argv) == 1:
            sys.argv.append(lang)
        else:
            sys.argv[1] = lang
        self.reject()


    def on_select_firmware_changed(self, value):
        """When the select_firmware drop down value is changed."""
        if value:
            QApplication.processEvents()
            self.progress.setValue(0)
            self.progress.show()

            self.firmware_version = meshtastic_flasher.util.tag_to_version(self.select_firmware_version.currentText())
            zip_file_name = meshtastic_flasher.util.zip_file_name_from_version(self.firmware_version)

            self.progress.setValue(20)
            QApplication.processEvents()

            meshtastic_flasher.util.download_if_zip_does_not_exist(zip_file_name, self.firmware_version)

            self.progress.setValue(80)
            QApplication.processEvents()

            # Note: unzip into directory named the same name as the firmware_version
            meshtastic_flasher.util.unzip_if_necessary(self.firmware_version, zip_file_name)

            if self.select_port.count() > 0 and self.firmware_version:
                self.select_flash.setEnabled(True)

            self.progress.setValue(100)
            QApplication.processEvents()


    def sort_firmware_versions(self):
        """Sort the firmware versions
          Note: There is an InsertPolicy but could not get it to work.
        """
        items = []
        for i in range(0, self.select_firmware_version.count()):
            items.append(self.select_firmware_version.itemText(i))
        items = sorted(set(items), reverse=True)

        self.select_firmware_version.clear()
        if len(items) > 0:
            for item in items:
                self.select_firmware_version.addItem(item)
            
        self.select_firmware_version.setCurrentIndex(0)


    def get_versions_from_disk(self):
        """Populate the versions from the directories on disk, "newest" first"""
        directories = glob.glob('2.*.*.*')
        for directory in sorted(directories, reverse=True):
            self.select_firmware_version.addItem(directory)
        self.sort_firmware_versions()
        if self.select_firmware_version.count() > 0:
            self.select_firmware_version.setEnabled(True)


    def get_versions(self):
        """Get versions: populate the drop down of available versions from Github tagged releases"""
        print("start of get_versions")
        tags = []
        tags = meshtastic_flasher.util.get_tags()
        for tag in tags:
            #print(f'tag:{tag}')
            self.select_firmware_version.addItem(meshtastic_flasher.util.tag_to_version(tag))
        self.firmware_version = meshtastic_flasher.util.tag_to_version(self.select_firmware_version.currentText())

        self.select_firmware_version.setEnabled(True)
        self.select_firmware_version.setToolTip(self.main.tooltip('select_firmware_version_populated'))
        self.sort_firmware_versions()

        # only enable Flash button if we have both values
        if self.select_port.count() > 0 and self.firmware_version:
            self.select_flash.setEnabled(True)
        print("got versions")


    def all_devices(self):
        """Show all devices from zip file"""
        if self.firmware_version:
            if os.path.exists(self.firmware_version):
                self.select_device.insertSeparator(self.select_device.count())
                self.select_device.addItem(self.main.text('all'))
                count = self.select_device.count() - 1
                # make the label 'All' un-selectable
                self.select_device.model().item(count).setEnabled(False)
                filenames = glob.glob(f'{self.firmware_version}/firmware-*.bin')
                print(f'filenames:{filenames}')
                filenames = sorted(filenames)
                for filename in filenames:
                    device = filename.replace(f"{self.firmware_version}/", "")
                    device = device.replace(f"{self.firmware_version}\\", "")
                    device = device.replace("firmware-", "")
                    device = device.replace(f"-{self.firmware_version}", "")
                    device = device.replace(".bin", "")
                    self.select_device.addItem(device)


    def help_message(self):
        """Show help message"""
        print("help_message")
        msg_box = QMessageBox()
        msg_box.setWindowTitle(self.main.text('help'))
        msg_box.setTextFormat(QtCore.Qt.RichText)  # this is what makes the links clickable
        msg_box.setText(self.main.text('help_text'))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def about_message(self):
        """Show info about_message"""
        print("about_message")
        msg_box = QMessageBox()
        msg_box.setWindowTitle(self.main.text('about'))
        msg_box.setTextFormat(QtCore.Qt.RichText)
        msg_box.setText(self.main.text('about_text'))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()


    # pylint: disable=unused-argument
    def label_version_clicked(self, event):
        """label version clicked"""
        print("label version clicked")
        webbrowser.open('https://github.com/meshtastic/Meshtastic-device/releases')


    # pylint: disable=unused-argument
    def label_device_clicked(self, event):
        """label device clicked"""
        print("label device clicked")
        webbrowser.open('https://meshtastic.org/docs/hardware')


    def do_esptool(self):
        """do_esptool"""
        print(f"do esptool update_only:{self.update_only}")
        # if they do another session, clear contents of prior session
        self.esptool_form.text.clear()
        self.esptool_form.show()

        if self.update_only is not None:
            self.esptool_form.start(update_only=self.update_only, port=self.port, device_file=self.device_file, ble_ota_file=self.ble_ota_file, main=self.main, littlefs_file=self.littlefs_file)


    def hotkeys(self):
        """Show hotkeys"""
        print("hotkeys")
        QMessageBox.information(self, self.main.text('hotkeys'), self.main.text('hotkeys_text'))


    def detect_devices(self):
        """Detect devices"""
        supported_devices_detected = meshtastic_flasher.util.wrapped_detect_supported_devices()
        if len(supported_devices_detected) > 0:
            self.select_device.clear()
            self.select_device.addItem('Detected')
            # not make the label 'Detected' selectable
            self.select_device.model().item(0).setEnabled(False)
            for device in supported_devices_detected:
                print(f'Detected {device.name}')
                # If not already in the list, add it
                if self.select_device.findText(device.for_firmware) == -1:
                    self.select_device.addItem(device.for_firmware)
                    self.detected_list.append(device.for_firmware)
            if self.select_device.count() > 1:
                self.select_device.setCurrentIndex(1)
        else:
            print("No devices detected")
        return supported_devices_detected


    # Note: Disabled this check as users would get this and report it as a problem.
    def warn_if_cannot_open_serial_exclusively(self):
        """Warn if the we cannot open the serial port exclusively"""
        exclusive = False
        try:
            ser = serial.Serial(self.select_port.currentText(), baudrate=115200, exclusive=True, timeout=0.5)
            ser.close()
            exclusive = True
        except:
            pass
        if not exclusive:
            print("Warning: Cannot open the serial port exclusively.")
            # TODO: should this be warning and not information?
            QMessageBox.information(self, self.main.text('info'), self.main.text('warning_cannot_open_port_exclusively'))
        return exclusive


    def warn_windows_users_if_not_administrator(self):
        """Need to warn Windows users if the process running is not run as Administrator
           on Windows 11 and later
        """
        is_admin = None
        if meshtastic.util.is_windows11():
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print("Warning: This process is not running as Administrator.")
                # TODO: Should this be warning instead of information?
                QMessageBox.information(self, self.main.text('info'), self.main.text('warning_not_admin'))
        return is_admin


    def warn_linux_users_if_not_in_dialout_group(self):
        """Need to warn Linux users if the logged in user is not in the dialout group?"""
        system = platform.system()
        if system == 'Linux':
            username = getpass.getuser()
            groups = grp.getgrall()
            group_to_search = 'dialout'
            found_dialout_group = False
            for group in groups:
                if group.gr_name == 'dialout':
                    found_dialout_group = True
                    break
            if not found_dialout_group:
                group_to_search = 'uucp'
            print(f'group_to_search:{group_to_search}')
            is_member = False
            for group in groups:
                if group.gr_name == group_to_search:
                    if username in group.gr_mem:
                        is_member = True
                        break
            if not is_member:
                print(f"user is not in {group_to_search} group")
                print(f"  sudo usermod -a -G {group_to_search} {username}")
                print("Then logout. And re-login.")
                # Let the user know that they should be in the appropriate group
                # TODO: migrate to fields.json
                QMessageBox.information(self, self.main.text('info'),
                                        (f'Warning: The user ({username}) is not in the ({group_to_search}) group. Either:\n'
                                        'a) run this command as "sudo", or\n'
                                        'b) add this user to the dialout group using this command:\n'
                                        f"     sudo usermod -a -G {group_to_search} {username}\n"
                                        "  After running that command, log out and re-login for it to take effect.\n"))


    def detect_ports_using_find_ports(self, ports, supported_devices_detected):
        """Detect ports using the find ports method in Meshtastic python library"""
        ports = []
        if len(ports) == 0:
            print("Warning: Could not find any ports using the Meshtastic python autodetection method.")

            ports = meshtastic_flasher.util.wrapped_findPorts()
            if len(ports) == 0:
                print("Warning: Could not find any ports using the Meshtastic python autodetection method.")
                for device in supported_devices_detected:
                    meshtastic_flasher.util.wrapped_detect_windows_needs_driver(device, True)
            else:
                for port in ports:
                    if self.select_port.findText(port) == -1:
                        self.select_port.addItem(port)
        return ports


    def detect_ports_on_supported_devices(self, supported_devices_detected):
        """Detect ports on supported devices."""
        ports = meshtastic_flasher.util.wrapped_active_ports_on_supported_devices(supported_devices_detected)
        ports_sorted = list(ports)
        ports_sorted.sort()
        for port in ports_sorted:
            self.select_port.addItem(port)
        return ports


    def detect_nrf(self, supported_devices_detected):
        """See if nrf device"""
        # NRF52 devices
        for device in supported_devices_detected:
            if device.for_firmware in ['rak4631_5005', 'rak4631_19003', 't-echo']:
                print('nrf52 device detected')
                self.nrf = True

    def detect_nrf_stuff(self):
        """Do nrf stuff in detection"""
        if self.nrf:
            self.select_port.clear()

            partitions = psutil.disk_partitions()
            #print(f'partitions:{partitions}')
            search_for_partition = ['FTHR840BOOT', 'TECHOBOOT', 'NRF52BOOT', 'RAK4631']
            found_partition = False

            if platform.system() == "Windows":
                # need to run some power shell
                _, gv_output = subprocess.getstatusoutput('powershell.exe "[Console]::OutputEncoding = [Text.UTF8Encoding]::UTF8; Get-Volume"')
                for search in search_for_partition:
                    if re.search(search, str(gv_output), re.MULTILINE):
                        print('found partition on windows!')
                        found_partition = True
                        # for each line of output
                        lines = str(gv_output).split('\n')
                        print(f'lines:{lines}')
                        for line in lines:
                            parts = line.split(' ')
                            #print(f'parts:{parts}')
                            if search in line:
                                self.select_port.addItem(f"{parts[0]}:/")
                                self.select_port.setEnabled(True)
                                break
            else: # Linux or Darwin
                for partition in partitions:
                    print(f'partition:{partition}')
                    for search in search_for_partition:
                        if search in partition.mountpoint:
                            print(f'*** found {search}')
                            self.select_port.addItem(partition.mountpoint)
                            self.select_port.setEnabled(True)
                            found_partition = True
                            break

            if found_partition:
                rak_bootloader_date = "Date: Dec  1 2021"
                techo_bootloader_date = "Date: Oct 13 2021"
                techo_uf2_line = "Model: LilyGo T-Echo"
                is_techo = False
                rak_bootloader_current = False
                techo_bootloader_current = False

                # check the bootloder version
                with open(f"{self.select_port.currentText()}/INFO_UF2.TXT", encoding='utf-8') as f:
                    lines = f.readlines()
                print('Bootloader info:')
                print(f'lines:{lines}')
                for line in lines:
                    line = line.replace('\n', '')
                    if line == techo_uf2_line:
                        is_techo=True
                        print('definitely a T-Echo')
                    if line == techo_bootloader_date:
                        techo_bootloader_current = True
                        print('t-echo bootloader is current')
                        QMessageBox.information(self, "Info", "The T-Echo bootloader is current.")
                    if line == rak_bootloader_date:
                        #print(line)
                        rak_bootloader_current = True
                        print('rak bootloader is current')
                        QMessageBox.information(self, "Info", "The RAK bootloader is current.")

                # the 19003 reports same as 5005, so we cannot really trust it
                # for now add both 5005 and 19003 to devices
                # if we found the t-echo line, then swap
                self.select_device.clear()
                self.select_device.addItem(self.main.text('detected'))
                if is_techo:
                    # do not make the label 'Detected' selectable
                    self.select_device.model().item(0).setEnabled(False)
                    self.select_device.addItem('t-echo')
                    self.detected_list.append('t-echo')
                    self.select_device.insertSeparator(self.select_device.count())
                    self.select_device.addItem(self.main.text('other'))
                    count = self.select_device.count() - 1
                    self.select_device.model().item(count).setEnabled(False)
                    self.select_device.addItem('rak4631_5005')
                    self.select_device.addItem('rak4631_19003')
                    self.select_device.setCurrentIndex(1)
                    self.select_device.setEnabled(True)
                else:
                    # do not make the label 'Detected' selectable
                    self.select_device.model().item(0).setEnabled(False)
                    self.select_device.addItem('rak4631_5005')
                    self.select_device.addItem('rak4631_19003')

                    self.detected_list.append('rak4631_5005')
                    self.detected_list.append('rak4631_19003')

                    self.select_device.insertSeparator(self.select_device.count())
                    self.select_device.addItem(self.main.text('other'))
                    count = self.select_device.count() - 1
                    self.select_device.model().item(count).setEnabled(False)
                    self.select_device.addItem('t-echo')
                    self.select_device.setCurrentIndex(1)
                    self.select_device.setEnabled(True)

                if is_techo:
                    if not techo_bootloader_current:
                        print("t-echo bootloader is not current")
                        if self.confirm_update_bootloader('T-Echo'):
                            bootloader_zip_url = "https://github.com/lyusupov/SoftRF/blob/master/software/firmware/binaries/nRF52840/Adafruit_nRF52_Bootloader/LilyGO_TEcho_bootloader-0.6.1.zip?raw=true"
                            bootloader_zip_filename = "LilyGO_TEcho_bootloader-0.6.1.zip"
                            utf_filename = "update-lilygo_techo_bootloader-0.6.1_nosd.uf2"
                            if not os.path.exists(utf_filename):
                                print(f'do not have the {utf_filename} locally')
                                # we do not have the extracted filename, see if we have the zip file
                                if not os.path.exists(bootloader_zip_filename):
                                    print(f"Need to download the {bootloader_zip_filename} downloading...")
                                    ssl._create_default_https_context = ssl._create_unverified_context
                                    urllib.request.urlretrieve(bootloader_zip_url, bootloader_zip_filename)
                                    print("done downloading")
                                    with zipfile.ZipFile(bootloader_zip_filename, 'r') as zip_ref:
                                        # extract one file
                                        zip_ref.extract(utf_filename)
                            if not os.path.exists(utf_filename):
                                print(f'Warning: Still do not have the {utf_filename} locally.')
                                QMessageBox.warning(self, self.main.text('warning'), self.main.text('warning_issue_downloading'))
                            else:
                                dest = f'{self.select_port.currentText()}/{utf_filename}'
                                print(f'copying file:{utf_filename} to dest:{dest}')
                                shutil.copyfile(utf_filename, dest)
                                print('done copying')
                                QMessageBox.information(self, self.main.text('info'), self.main.text('techo_bootloader_updated'))
                else:
                    if self.select_device.currentText().startswith('rak'):
                        if not rak_bootloader_current:
                            print('rak bootloader is not current')
                        if self.confirm_update_bootloader('RAK'):
                            print('Checking boot loader version')
                            # instructions https://github.com/RAKWireless/WisBlock/tree/master/bootloader/RAK4630
                            bootloader_zip_url = "https://github.com/RAKWireless/WisBlock/releases/download/0.4.2/WisCore_RAK4631_Board_Bootloader.zip"
                            bootloader_zip_filename = "WisCore_RAK4631_Board_Bootloader.zip"
                            if not os.path.exists(bootloader_zip_filename):
                                print(f"Need to download the {bootloader_zip_filename} downloading...")
                                ssl._create_default_https_context = ssl._create_unverified_context
                                urllib.request.urlretrieve(bootloader_zip_url, bootloader_zip_filename)
                                print("done downloading")

                            query_ports_again = meshtastic_flasher.util.wrapped_findPorts()
                            if len(query_ports_again) == 1:
                                port_to_use = query_ports_again[0]
                                command = f"adafruit-nrfutil --verbose dfu serial --package {bootloader_zip_filename} -p {port_to_use} -b 115200 --singlebank --touch 1200"
                                _, nrfutil_output = subprocess.getstatusoutput(command)
                                print(nrfutil_output)

                                QMessageBox.information(self, self.main.text('info'), self.main.text('done_updating_bootloader'))

            else:
                print("Could not find the partition")
                QMessageBox.information(self, self.main.text('info'), self.main.text('could_not_find_partition'))


    def version_and_device_from_info(self, ports):
        """Get firmware version and "for firmware" device info from meshtastic python lib
           returns True if detected device is nrf (so we do not continue the detection path)
        """
        is_nrf = False
        if len(ports) > 0:
            use_port = list(ports)[0]
            print("Getting version and hwModel from Meshtastic python library")
            try:
                iface = meshtastic.serial_interface.SerialInterface(devPath=use_port)
                if iface:
                    if iface.myInfo:
                        self.detected_meshtastic_version = iface.myInfo.firmware_version
                        self.label_detected_meshtastic_version.setText(f'{self.main.text("detected")}:\n{self.detected_meshtastic_version}')
                    hwModel = None
                    if iface.nodes:
                        for n in iface.nodes.values():
                            if n['num'] == iface.myInfo.my_node_num:
                                hwModel = n['user']['hwModel']
                                break
                    iface.close()
                    if self.is_hwModel_nrf(hwModel):
                        # this is an NRF device but not in boot mode
                        is_nrf = True
                        QMessageBox.information(self, self.main.text('info'), self.main.text('nrf_detected'))
                    else:
                        device = self.hwModel_to_device(hwModel)
                        self.update_device_dropdown(device)
            except Exception as e:
                print(f'Exception:{e}')
                QMessageBox.warning(self, self.main.text('warning'), self.main.text('warning_talking_to_device'))
        return is_nrf


    def update_device_dropdown(self, device):
        """Update the device drop down with the device detected"""
        if device:
            self.select_device.clear()
            self.select_device.addItem(self.main.text('detected'))
            # do not make the label 'Detected' selectable
            self.select_device.model().item(0).setEnabled(False)
            self.select_device.addItem(device)
            self.detected_list.append(device)
            if self.select_device.count() > 1:
                self.select_device.setCurrentIndex(1)


    def hwModel_to_device(self, hwModel):
        """Convert the hwModel from python lib to device for drop downlist"""
        device = None
        if hwModel == 'HELTEC_V1':
            device = 'heltec-v1'
        elif hwModel == 'HELTEC_V2_1':
            device = 'heltec-v2.1'
        elif hwModel == 'HELTEC_V2_0':
            device = 'heltec-v2.0'
        elif hwModel == 'DIY_V1':
            device = 'meshtastic-diy-v1'
        elif hwModel == 'RAK4631':
            # NOTE: *still* could be 19003
            device = 'rak4631_5005'
        elif hwModel == 'T_ECHO':
            device = 't-echo'
        elif hwModel == 'TBEAM':
            device = 'tbeam'
        elif hwModel == 'TBEAM_V07':
            device = 'tbeam0.7'
        elif hwModel == 'TLORA_V1':
            device = 'tlora-v1'
        elif hwModel == 'TLORA_V2':
            device = 'tlora-v2'
        elif hwModel == 'TLORA_V2_1_16':
            device = 'tlora-v2-1-1.6'
        elif hwModel == 'TLORA_V1_3':
            device = 'tlora_v1_3'
        elif hwModel == 'RAK11200':
            device = 'rak11200'
        elif hwModel == 'NANO_G1':
            device = 'nano-g1'
        return device

    def is_hwModel_nrf(self, hwModel):
        """Return True if hwModel is nrf"""
        is_nrf = False
        if hwModel in ['RAK4631', 'T_ECHO']:
            is_nrf = True
        return is_nrf


    def reset_for_detect(self):
        """Reset the devices and ports when you hit DETECT."""
        self.port = None
        self.nrf = False
        self.device = None
        self.device_file = None
        self.ble_ota_file = None
        self.littlefs_file = None
        self.update_only = None
        self.select_device.clear()
        self.select_port.clear()
        self.select_flash.setEnabled(False)
        self.select_port.setEnabled(False)
        self.select_device.setEnabled(False)
        self.detected_meshtastic_version = None
        self.label_detected_meshtastic_version.setText('')
        self.detected_list.clear()
        self.device_from_picker = None


    def enable_at_end_of_detect(self):
        """Set combo boxes and flash button if appropriate."""
        if self.select_port.count() > 0:
            self.select_port.setToolTip(self.main.text('select_port_populated'))
            self.select_port.setEnabled(True)
        else:
            self.select_port.setEnabled(False)

        if self.select_device.count() > 0:
            self.select_device.setToolTip(self.main.text('select_device_populated'))
            self.select_device.setEnabled(True)
        else:
            self.select_device.setEnabled(False)

        # only enable Flash button and Device dropdown if we have firmware and ports
        if self.select_port.count() > 0 and self.firmware_version:
            self.select_flash.setEnabled(True)
            self.select_flash.setToolTip(self.main.tooltip('select_flash_populated'))


    def is_rak11200(self, supported_devices):
        """See if the rak11200 was detected."""
        is_it_a_rak11200 = False
        for supported_device in supported_devices:
            if supported_device.for_firmware == 'rak11200':
                is_it_a_rak11200 = True
        return is_it_a_rak11200


    def detect(self):
        """Detect port, download zip file from github if we need to, and unzip it"""
        print("start of detect")

        self.reset_for_detect()

        QApplication.processEvents()
        self.progress.setValue(0)
        self.progress.show()

        self.warn_linux_users_if_not_in_dialout_group()
        self.warn_windows_users_if_not_administrator()

        self.progress.setValue(10)
        QApplication.processEvents()

        supported_devices_detected = self.detect_devices()

        self.progress.setValue(30)
        QApplication.processEvents()

        ports = self.detect_ports_on_supported_devices(supported_devices_detected)

        self.progress.setValue(50)
        QApplication.processEvents()

        self.detect_nrf(supported_devices_detected)
        if self.nrf:
            # we must be in boot mode
            self.detect_nrf_stuff()
        else:
            use_meshtastic_check = self.confirm_check_using_meshtastic()
            if use_meshtastic_check:
                self.select_port.clear()
                self.detected_list.clear()
                ports = self.detect_ports_using_find_ports(ports, supported_devices_detected)
                print(f'from find_ports ports:{ports}')

            is_rak11200 = self.is_rak11200(supported_devices_detected)
            if is_rak11200:
                print("Looks like a RAK 11200, ensure in boot mode (single red solid light, no green nor blue lights).")
                print("See https://docs.rakwireless.com/assets/images/wisblock/rak11200/quickstart/rak11200-Boot0-for-flashing.png")
                QMessageBox.information(self, self.main.text('info'), self.main.text('rak_11200_detected'))

            else:
                if use_meshtastic_check:
                    # probably not in boot mode, see if this device is an nrf device
                    is_nrf = self.version_and_device_from_info(ports)
                    if not is_nrf:

                        if self.select_port.count() > 0:
                            self.all_devices()
                        else:
                            print("No devices detected")
                            QMessageBox.information(self, self.main.text('info'), self.main.text('no_devices_detected'))

                        self.progress.setValue(80)
                        QApplication.processEvents()
                else:
                    if self.select_port.count() > 0:
                        self.all_devices()

        print(f'self.detected_list:{self.detected_list}')
        if len(self.detected_list) > 1:
            self.radio_picker_form.run(self.detected_list)
            print(f'self.device_from_picker:{self.device_from_picker}')
            if self.device_from_picker is not None:
                index = self.select_device.findText(self.device_from_picker)
                print(f'index:{index}')
                self.select_device.setCurrentIndex(index)

        self.enable_at_end_of_detect()

        self.progress.setValue(100)
        QApplication.processEvents()
        print("end of detect")


    def flash_nrf52(self):
        """Flash nrf52 devices"""
        print("Flash nrf52")
        uf2_file = f"{self.firmware_version}/firmware-{self.device}-{self.firmware_version}.uf2"
        dest = f'{self.port}/firmware-{self.device}-{self.firmware_version}.uf2'
        print(f'copying file:{uf2_file} to dest:{dest}')
        shutil.copyfile(uf2_file, dest)
        print('done copying')


    def check_update_only(self):
        """Check if the user selected the advanced options "update only" option.
           Sets self.update_only based on the form value.
           Returns text for confirmation dialog
        """
        self.update_only = self.advanced_form.update_only_cb.isChecked()
        update_only_message = ""
        if self.update_only:
            print('update only is checked')
            update_only_message = f"**{self.main.text('update_only')}** "
        else:
            print('update only is not checked')
        return update_only_message


    def confirm_update_bootloader(self, name='T-Echo'):
        """Prompt the user to confirm if they want to proceed with the updating the {name} bootloader.
           Returns True if user answered Yes, otherwise returns False
        """
        want_to_proceed = False
        confirm_msg = self.main.text('confirm_update_bootloader')
        reply = QMessageBox.question(self, self.main.text('update'), confirm_msg, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            want_to_proceed = True
            print(f"User confirmed they want to update the {name} bootloader")
        else:
            print(f"User does not want to update the {name} bootloader")
        return want_to_proceed


    def confirm_flash_question(self, update_only_message):
        """Prompt the user to confirm if they want to proceed with the flashing.
           Returns True if user answered Yes, otherwise returns False
        """
        want_to_proceed = False
        verb = self.main.text('flash')
        all_settings_msg = ''
        if update_only_message == '':
            all_settings_msg = self.main.text('note_all_settings_will_be_erased')
        if self.nrf:
            verb = self.main.text('copy')
            update_only_message = ''
            all_settings_msg = ''
        confirm_msg = f'{self.main.text("confirm_flash_first_part")} {update_only_message}{verb}\n{self.firmware_version}\n'
        confirm_msg += f'{self.port}\n{self.device}?\n\n{all_settings_msg}'
        reply = QMessageBox.question(self, 'Flash', confirm_msg, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            want_to_proceed = True
            print("User confirmed they want to flash")
        else:
            print("User does not want to flash")
        return want_to_proceed


    def confirm_check_using_meshtastic(self):
        """Prompt the user to confirm if they want to use the Meshtastic python method to detect device/port.
           Returns True if user answered Yes, otherwise returns False
        """
        want_to_check = False
        msg = self.main.text('device_has_meshtastic')
        reply = QMessageBox.question(self, self.main.text('question'), msg, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            want_to_check = True
            print("User confirmed the device has Meshtastic so we will check using the Meshtastic python method")
        else:
            print("User said no to device having Meshtastic on the device so no detection using the Meshtastic python method")
        return want_to_check


    def flash_stuff(self):
        """Flash to the device."""
        print("Flash was clicked.")

        QApplication.processEvents()
        self.progress.setValue(0)
        self.progress.show()

        #self.warn_if_cannot_open_serial_exclusively()

        self.firmware_version = meshtastic_flasher.util.tag_to_version(self.select_firmware_version.currentText())
        self.port = self.select_port.currentText()
        self.device = self.select_device.currentText()

        update_only_message = self.check_update_only()

        proceed = self.confirm_flash_question(update_only_message)

        if proceed:
            if self.nrf:
                # nrf52 devices
                self.flash_nrf52()
                print("nrf52 file was copied")
                QMessageBox.information(self, self.main.text('info'), self.main.text('file_was_copied'))
            else:
                # esp32 devices
                self.device_file = f"{self.firmware_version}/firmware-{self.device}-{self.firmware_version}.bin"
                if self.update_only:
                    self.do_esptool()
                else:
                    self.ble_ota_file = f"{self.firmware_version}/bleota.bin"
                    self.littlefs_file = f"{self.firmware_version}/littlefs-{self.firmware_version}.bin"
                    self.do_esptool()
