"""class for the serial module settings"""


from PySide6 import QtCore
from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QDialogButtonBox, QLineEdit, QLabel

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref
from meshtastic_flasher.util import zero_if_blank


class SerialForm(QDialog):
    """serial module settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(SerialForm, self).__init__(parent)

        self.parent = parent
        self.main = parent.main

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle(self.main.text('serial_plugin_settings'))

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.serial_module_about = QLabel(self.main.doc_url('serial_module_about'))
        self.serial_module_about.setOpenExternalLinks(True)
        self.serial_module_about.setTextFormat(QtCore.Qt.RichText)
        self.serial_module_about.setToolTip(self.main.tooltip('module_link'))
        self.serial_module_enabled = QCheckBox()
        self.serial_module_enabled.setToolTip(self.main.description('serial_module_enabled'))
        self.serial_module_echo = QCheckBox()
        self.serial_module_echo.setToolTip(self.main.description('serial_module_echo'))
        self.serial_module_mode = QLineEdit()
        self.serial_module_mode.setToolTip(self.main.description('serial_module_mode'))
        self.serial_module_rxd = QLineEdit()
        self.serial_module_rxd.setToolTip(self.main.description('serial_module_rxd'))
        self.serial_module_txd = QLineEdit()
        self.serial_module_txd.setToolTip(self.main.description('serial_module_txd'))
        self.serial_module_timeout = QLineEdit()
        self.serial_module_timeout.setToolTip(self.main.description('serial_module_timeout'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.main.label("serial_module_about"), self.serial_module_about)
        form_layout.addRow(self.main.label("serial_module_enabled"), self.serial_module_enabled)
        form_layout.addRow(self.main.label("serial_module_echo"), self.serial_module_echo)
        form_layout.addRow(self.main.label("serial_module_mode"), self.serial_module_mode)
        form_layout.addRow(self.main.label("serial_module_txd"), self.serial_module_txd)
        form_layout.addRow(self.main.label("serial_module_rxd"), self.serial_module_rxd)
        form_layout.addRow(self.main.label("serial_module_timeout"), self.serial_module_timeout)
        form_layout.addRow("", self.button_box)
        self.setLayout(form_layout)


    def run(self, port=None, interface=None):
        """load the form"""
        self.port = port
        self.interface = interface
        if self.port:
            print(f'using port:{self.port}')
            self.get_values()
            self.show()


    def get_values(self):
        """Get values from device"""
        try:
            if self.interface is None:
                print('interface was none?')
                self.interface = meshtastic.serial_interface.SerialInterface(devPath=self.port)
            if self.interface:
                self.prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences

                if self.prefs.serial_module_enabled and self.prefs.serial_module_enabled is True:
                    self.serial_module_enabled.setChecked(True)

                if self.prefs.serial_module_echo and self.prefs.serial_module_echo is True:
                    self.serial_module_enabled.setChecked(True)

                if self.prefs.serial_module_mode:
                    self.serial_module_mode.setText(f'{self.prefs.serial_module_mode}')
                else:
                    self.serial_module_mode.setText("0")

                if self.prefs.serial_module_rxd:
                    self.serial_module_rxd.setText(f'{self.prefs.serial_module_rxd}')
                else:
                    self.serial_module_rxd.setText("0")

                if self.prefs.serial_module_timeout:
                    self.serial_module_timeout.setText(f'{self.prefs.serial_module_timeout}')
                else:
                    self.serial_module_timeout.setText("0")

                if self.prefs.serial_module_txd:
                    self.serial_module_txd.setText(f'{self.prefs.serial_module_txd}')
                else:
                    self.serial_module_txd.setText("0")

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'serial_module_enabled', f'{self.serial_module_enabled.isChecked()}')
                setPref(prefs, 'serial_module_echo', f'{self.serial_module_echo.isChecked()}')
                setPref(prefs, 'serial_module_mode', zero_if_blank(self.serial_module_mode.text()))
                setPref(prefs, 'serial_module_rxd', zero_if_blank(self.serial_module_rxd.text()))
                setPref(prefs, 'serial_module_txd', zero_if_blank(self.serial_module_txd.text()))
                setPref(prefs, 'serial_module_timeout', zero_if_blank(self.serial_module_timeout.text()))
                self.interface.getNode(BROADCAST_ADDR).writeConfig()

        except Exception as e:
            print(f'Exception:{e}')


    def reject(self):
        """Cancel without saving"""
        print('CANCEL button was clicked')
        self.parent.my_close()


    def accept(self):
        """Close the form"""
        print('SAVE button was clicked')
        self.write_values()
