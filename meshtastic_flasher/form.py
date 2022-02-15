"""Form for meshtastic-flasher"""

import os
import shutil
import ctypes
import glob
import platform
import urllib
import ssl
import re
import subprocess
import webbrowser
import psutil

import serial

from PySide6 import QtCore
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtWidgets import (QPushButton, QApplication,
                               QVBoxLayout, QHBoxLayout, QDialog, QLabel,
                               QMessageBox, QComboBox, QProgressBar)

import meshtastic
import meshtastic.serial_interface

from meshtastic_flasher.version import __version__
from meshtastic_flasher.advanced_form import AdvancedForm
from meshtastic_flasher.esptool_form import EsptoolForm
import meshtastic_flasher.util
import meshtastic_flasher.yes_no

MESHTASTIC_LOGO_FILENAME = "logo.png"

# windows does not like this one
if platform.system() == "Linux":
    import grp
    import getpass


MESHTASTIC_COLOR_DARK = "#2C2D3C"
MESHTASTIC_COLOR_GREEN = "#67EA94"



class Form(QDialog):
    """Main application"""

    def __init__(self, parent=None):
        """constructor"""
        super(Form, self).__init__(parent)

        self.port = None
        self.firmware_version = None
        self.nrf = False
        self.device = None
        self.update_only = None
        self.device_file = None
        self.system_info_file = None
        self.bin_file = None
        self.detected_meshtastic_version = None

        self.advanced_form = AdvancedForm()
        self.esptool_form = EsptoolForm()

        update_available = ''
        if meshtastic_flasher.util.check_if_newer_version():
            update_available = ' *update available*'
        self.setWindowTitle(f"Meshtastic Flasher v{__version__}{update_available}")

        # Create widgets
        self.get_versions_button = QPushButton("GET VERSIONS")
        self.get_versions_button.setToolTip("Click to check for more recent firmware.")

        self.select_firmware_version = QComboBox()
        self.select_firmware_version.setToolTip("Click GET VERSIONS for the list of firmware versions.")
        self.select_firmware_version.setMinimumContentsLength(18)
        self.select_firmware_version.setDisabled(True)

        self.select_detect = QPushButton("DETECT DEVICE")
        self.select_detect.setToolTip("Click to detect supported device and port info.")
        # Note: The text of the buttons is done in the styles, need to override it
        self.select_detect.setStyleSheet("text-transform: none")

        self.help_button = QPushButton("?")
        self.help_button.setToolTip("Click for help.")

        self.select_port = QComboBox()
        self.select_port.setToolTip("Click GET VERSIONS and DETECT DEVICE before you can select the port.")
        self.select_port.setMinimumContentsLength(25)
        self.select_port.setDisabled(True)
        self.select_port.setDuplicatesEnabled(False)

        self.select_device = QComboBox()
        self.select_device.setToolTip("Click GET VERSIONS and DETECT DEVICE before you can select the device.")
        self.select_device.setMinimumContentsLength(17)
        self.select_device.setDisabled(True)

        self.select_flash = QPushButton("FLASH")
        self.select_flash.setToolTip("Click to flash the firmware.\nIf this button is not enabled, need to click the GET VERSIONS and DETECT DEVICE \nbuttons to populate the available options.")
        self.select_flash.setEnabled(False)

        self.progress = QProgressBar()
        self.progress.setToolTip("Progress will be shown during the FLASH step.")
        self.progress.hide()

        self.logo = QLabel(self)
        self.logo.setToolTip("This is the Meshtastic logo. Click to visit Meshtastic.org.")
        pixmap = QPixmap(meshtastic_flasher.util.get_path(MESHTASTIC_LOGO_FILENAME))
        self.logo.setPixmap(pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        style_for_logo = (f"background-color: {MESHTASTIC_COLOR_GREEN}; border-color: "
                          f"{MESHTASTIC_COLOR_GREEN}; border-radius: 0px; color: {MESHTASTIC_COLOR_DARK};")
        self.logo.setStyleSheet(style_for_logo)
        self.logo.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        # labels for over the drop downs/combo boxes
        self.label_version = QLabel(self)
        self.label_version.setText("                         Version")
        #self.label_version.setStyleSheet("background-color: white; color: #0000FF")
        self.label_version.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.label_version.setToolTip("Click to see more about firmare releases")

        self.label_port = QLabel(self)
        self.label_port.setText("                           Port")

        self.label_device = QLabel(self)
        self.label_device.setText("                        Device")
        self.label_device.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.label_device.setToolTip("Click to see more about Meshtastic supported devices")

        self.label_detected_meshtastic_version = QLabel(self)
        self.label_detected_meshtastic_version.setText("")

        # Create layout and add widgets
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        if self.logo:
            main_layout.addWidget(self.logo)

        main_layout.addStretch(1)

        detect_layout = QHBoxLayout()
        detect_layout.addStretch(1)
        detect_layout.addWidget(self.get_versions_button)
        detect_layout.addWidget(self.select_detect)
        detect_layout.addWidget(self.help_button)
        detect_layout.setContentsMargins(0, 0, 0, 0)
        detect_layout.addStretch(1)

        label_layout = QHBoxLayout()
        label_layout.addWidget(self.label_version)
        label_layout.addWidget(self.label_port)
        label_layout.addWidget(self.label_device)
        label_layout.setContentsMargins(0, 0, 0, 0)

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
        main_layout.addLayout(detect_layout)
        main_layout.addLayout(label_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(flash_layout)
        main_layout.addLayout(progress_layout)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        # move version
        self.label_detected_meshtastic_version.move(45, 270)
        self.label_detected_meshtastic_version.show()

        # Add button signals to slots
        self.logo.mousePressEvent = self.logo_clicked
        self.get_versions_button.clicked.connect(self.get_versions)
        self.help_button.clicked.connect(self.hotkeys)
        self.label_version.mousePressEvent = self.label_version_clicked
        self.label_device.mousePressEvent = self.label_device_clicked
        self.select_detect.clicked.connect(self.detect)
        self.select_flash.clicked.connect(self.flash_stuff)
        self.select_firmware_version.currentTextChanged.connect(self.on_select_firmware_changed)

        # pre-populate the versions that have already been downloaded and unzipped
        self.get_versions_from_disk()


    def keyPressEvent(self, event):
        """Deal with a key press"""
        if event.key() == QtCore.Qt.Key_A:
            print("A was pressed... showing advanced options form")
            self.show_advanced_options()
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
            QApplication.quit()
        elif event.key() == QtCore.Qt.Key_T:
            print("T was pressed... so quitting")
            self.tips()


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

            #self.all_devices()

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
        for item in items:
            self.select_firmware_version.addItem(item)
        self.select_firmware_version.setCurrentIndex(0)


    def get_versions_from_disk(self):
        """Populate the versions from the directories on disk, "newest" first"""
        directories = glob.glob('1.*.*.*')
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
        self.select_firmware_version.setToolTip("Select desired firmware version to flash.")
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
                self.select_device.addItem('All')
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



    def tips(self):
        """Show tips"""
        print("tips")
        QMessageBox.information(self, "Info", ("Tips:\n\n"
                                "If having issues flashing the device, be sure there is only one device connected\n"
                                "and no other applications are using that communications port.\n\n"
                                "If still having problems, unplug the device, then re-plugin the device.\n\n"
                                "If still having problems, try rebooting the pc.\n\n"
                                "If you get a 'Critical Fault #6' on a T-Beam, it probably means you need to use\n"
                                "v1.1 or v2.1.1.6 firmware.\n\n"))


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
            self.esptool_form.start(update_only=self.update_only, port=self.port, device_file=self.device_file, system_info_file=self.system_info_file, bin_file=self.bin_file)


    def hotkeys(self):
        """Show hotkeys"""
        print("hotkeys")
        QMessageBox.information(self, "Info", ("Hotkeys:\n"
                                "A - Advanced options\n"
                                "D - Detect\n"
                                "G - Get versions\n"
                                "H - Hotkeys\n"
                                "T - Tips\n"
                                "Q - Quit\n"))


    def show_advanced_options(self):
        """Advanced Options"""
        print("advanced options")
        self.advanced_form.show()


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
            ser = serial.Serial(self.select_port.currentText(), baudrate=921600, exclusive=True, timeout=0.5)
            ser.close()
            exclusive = True
        except:
            pass
        if not exclusive:
            print("Warning: Cannot open the serial port exclusively.")
            QMessageBox.information(self, "Info",
                                    ("Warning: Cannot open the serial port exclusively.\n"
                                    "Please close any other programs that might be using that port and re-try."))
        return exclusive


    def warn_windows_users_if_not_administrator(self):
        """Need to warn Windows users if the process running is not run as Administrator
           on Windows 11 and later
        """
        is_admin = None
        if meshtastic_flasher.util.is_windows11():
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print("Warning: This process is not running as Administrator.")
                QMessageBox.information(self, "Info",
                                        ("Warning: This process is not running as Administrator.\n"
                                        "Please close and re-run as Administrator."))
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
                QMessageBox.information(self, "Info",
                                        (f'Warning: The user ({username}) is not in the ({group_to_search}) group. Either:\n'
                                        'a) run this command as "sudo", or\n'
                                        'b) add this user to the dialout group using this command:\n'
                                        f"     sudo usermod -a -G {group_to_search} {username}\n"
                                        "  After running that command, log out and re-login for it to take effect.\n"))


    def update_ports_for_weird_tlora(self):
        """Deal with weird T-Lora device (single device connected, but shows up as 2 ports)"""
        ports = []
        # ports:['/dev/cu.usbmodem11301', '/dev/cu.wchusbserial11301']
        tmp_ports = meshtastic_flasher.util.wrapped_findPorts()
        if len(tmp_ports) == 2:
            if 'wchusbserial' in tmp_ports[1]:
                first = tmp_ports[0].replace("usbmodem", "")
                second = tmp_ports[1].replace("wchusbserial", "")
                print(f'first:{first} second:{second}')
                if first == second:
                    print('We are dealing with a weird TLora port situation.')
                    self.select_port.clear()
                    self.select_port.addItem(tmp_ports[1])
                    self.select_port.addItem(tmp_ports[0]) # delete this one?
                    ports = tmp_ports
        return ports


    def detect_ports_using_find_ports(self, ports, supported_devices_detected):
        """Detect ports using the find ports method in Meshtastic python library"""
        ports = []
        if len(ports) == 0:
            print("Warning: Could not find any ports using the Meshtstic python autodetection method.")

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
        possible_weird = False
        for port in ports_sorted:
            if 'usbmodem' in port:
                possible_weird = True
            self.select_port.addItem(port)
        if possible_weird:
            ports = self.update_ports_for_weird_tlora()
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
            search_for_partition = ['FTHR840BOOT', 'TECHOBOOT', 'RAK4631']
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
                self.select_device.addItem('Detected')
                if is_techo:
                    # do not make the label 'Detected' selectable
                    self.select_device.model().item(0).setEnabled(False)
                    self.select_device.addItem('t-echo')
                    self.select_device.insertSeparator(self.select_device.count())
                    self.select_device.addItem('Other')
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
                    self.select_device.insertSeparator(self.select_device.count())
                    self.select_device.addItem('Other')
                    count = self.select_device.count() - 1
                    self.select_device.model().item(count).setEnabled(False)
                    self.select_device.addItem('t-echo')
                    self.select_device.setCurrentIndex(1)
                    self.select_device.setEnabled(True)

                if is_techo:
                    if not techo_bootloader_current:
                        print("t-echo bootloader is not current")
                else:
                    if (not rak_bootloader_current) and (not self.advanced_form.rak_bootloader_cb.isChecked()):
                        print('rak bootloader is not current')
                        QMessageBox.information(self, "Info", ('The RAK bootloader is not current.\n'
                                                'If you want to udpate the bootlader,\n'
                                                'go into advanced options by pressing the letter "A" at the main screen,\n'
                                                'and check the update RAK bootloader then press DETECT again.'))

                    if (not rak_bootloader_current) and self.advanced_form.rak_bootloader_cb.isChecked() and self.select_device.currentText().startswith('rak'):
                        QMessageBox.information(self, "Info", ("Update RAK bootloader was requested.\n"
                                                "Press the RST button ONCE to get out of bootloader mode, then continue."))

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

                            QMessageBox.information(self, "Info", "Done updating bootloader.")

            else:
                print("Could not find the partition")
                QMessageBox.information(self, "Info", "Could not find the partition.\nPress the RST button TWICE\nthen re-try the pressing the DETECT button again.")


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
                        self.label_detected_meshtastic_version.setText(f'Detected:\n{self.detected_meshtastic_version}')
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
                        QMessageBox.information(self, "Info", "NRF device detected.\n\nPress RST button twice then click the DETECT button again.")
                    else:
                        device = self.hwModel_to_device(hwModel)
                        self.update_device_dropdown(device)
            except Exception as e:
                print(f'Exception:{e}')
                QMessageBox.warning(self, "Warning", "Had a problem talking with the device.\nMaybe disconnect and reconnect the device?\nIf the device is an nrf52 (T-Echo or RAK),\nthen put in boot mode by pressing RST button twice.")
        return is_nrf


    def update_device_dropdown(self, device):
        """Update the device drop down with the device detected"""
        if device:
            self.select_device.clear()
            self.select_device.addItem('Detected')
            # not make the label 'Detected' selectable
            self.select_device.model().item(0).setEnabled(False)
            self.select_device.addItem(device)
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
        self.system_info_file = None
        self.bin_file = None
        self.update_only = None
        self.select_device.clear()
        self.select_port.clear()
        self.select_flash.setEnabled(False)
        self.select_port.setEnabled(False)
        self.select_device.setEnabled(False)
        self.detected_meshtastic_version = None
        self.label_detected_meshtastic_version.setText('')


    def enable_at_end_of_detect(self):
        """Set combo boxes and flash button if appropriate."""
        if self.select_port.count() > 0:
            self.select_port.setToolTip("Select the communication port/destination")
            self.select_port.setEnabled(True)
        else:
            self.select_port.setEnabled(False)

        if self.select_device.count() > 0:
            self.select_device.setToolTip("Select the device variant")
            self.select_device.setEnabled(True)
        else:
            self.select_device.setEnabled(False)

        # only enable Flash button and Device dropdown if we have firmware and ports
        if self.select_port.count() > 0 and self.firmware_version:
            self.select_flash.setEnabled(True)
            self.select_flash.setToolTip('Click the FLASH button to write to the device.')


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
                ports = self.detect_ports_using_find_ports(ports, supported_devices_detected)
                print(f'from find_ports ports:{ports}')

            is_rak11200 = self.is_rak11200(supported_devices_detected)
            if is_rak11200:
                print("Looks like a RAK 11200, ensure in boot mode (single red solid light, no green nor blue lights).")
                print("See https://docs.rakwireless.com/assets/images/wisblock/rak11200/quickstart/rak11200-Boot0-for-flashing.png")
                QMessageBox.information(self, "Info", ("Looks like a RAK 11200 was detected.\n\n"
                                        "Verify it is in BOOT mode.\n\n"
                                        "There should be a single, solid red light.\n"
                                        "There should not be any other lights, solid nor flashing.\n\n"
                                        "If not, disconnect the device and provide a jumper between GND and BOOT0 while you plug it in.\n\n"))

            else:
                if use_meshtastic_check:
                    # probably not in boot mode, see if this device is an nrf device
                    is_nrf = self.version_and_device_from_info(ports)
                    if not is_nrf:

                        if self.select_port.count() > 0:
                            self.all_devices()
                        else:
                            print("No devices detected")
                            QMessageBox.information(self, "Info", "No devices detected.\n\nAre you using a data cable?\n\nDo you need to have a device driver installed?\n\nPlugin a device?")

                        self.progress.setValue(80)
                        QApplication.processEvents()
                else:
                    if self.select_port.count() > 0:
                        self.all_devices()

        self.enable_at_end_of_detect()

        self.progress.setValue(100)
        QApplication.processEvents()
        print("end of detect")


    # pylint: disable=unused-argument
    def logo_clicked(self, event):
        """The logo was clicked."""
        print("The logo was clicked")
        webbrowser.open('https://meshtastic.org')


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
            update_only_message = "**update only** "
        else:
            print('update only is not checked')
        return update_only_message


    def confirm_flash_question(self, update_only_message):
        """Prompt the user to confirm if they want to proceed with the flashing.
           Returns True if user answered Yes, otherwise returns False
        """
        want_to_proceed = False
        verb = 'flash'
        all_settings_msg = ''
        if update_only_message == '':
            all_settings_msg = 'NOTE: All Meshtastic settings will be erased.'
        if self.nrf:
            verb = 'copy'
            update_only_message = ''
            all_settings_msg = ''
        confirm_msg = f'Are you sure you want to {update_only_message}{verb}\n{self.firmware_version}\n'
        confirm_msg += f'{self.port}\n{self.device}?\n\n{all_settings_msg}'
        reply = meshtastic_flasher.yes_no.YesNo(message=confirm_msg).exec()
        if reply == QDialog.Accepted:
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
        msg = 'Does the device currently have Meshtastic version 1.2 or greater?'
        reply = meshtastic_flasher.yes_no.YesNo(message=msg).exec()
        if reply == QDialog.Accepted:
            want_to_check = True
            print("User confirmed they want to check using the Meshtastic python method")
        else:
            print("User declined detection using the Meshtastic python method")
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
                QMessageBox.information(self, "Info", "File was copied.\nWait for the device to reboot.")
            else:
                # esp32 devices
                self.device_file = f"{self.firmware_version}/firmware-{self.device}-{self.firmware_version}.bin"
                if self.update_only:
                    self.do_esptool()
                else:
                    self.system_info_file = f"{self.firmware_version}/system-info.bin"
                    self.bin_file = f"{self.firmware_version}/spiffs-{self.firmware_version}.bin"
                    self.do_esptool()
