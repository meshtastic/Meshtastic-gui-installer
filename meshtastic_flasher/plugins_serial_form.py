"""class for the serial plugin settings"""


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
    """serial plugin settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(SerialForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Serial Plugin Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.serialplugin_about = QLabel(self.parent.parent.doc_url('serialplugin_about'))
        self.serialplugin_about.setOpenExternalLinks(True)
        self.serialplugin_about.setTextFormat(QtCore.Qt.RichText)
        self.serialplugin_about.setToolTip("Link shows more info about the settings for this plugin.")
        self.serialplugin_enabled = QCheckBox()
        self.serialplugin_enabled.setToolTip(self.parent.parent.description('serialplugin_enabled'))
        self.serialplugin_echo = QCheckBox()
        self.serialplugin_echo.setToolTip(self.parent.parent.description('serialplugin_echo'))
        self.serialplugin_mode = QLineEdit()
        self.serialplugin_mode.setToolTip(self.parent.parent.description('serialplugin_mode'))
        self.serialplugin_rxd = QLineEdit()
        self.serialplugin_rxd.setToolTip(self.parent.parent.description('serialplugin_rxd'))
        self.serialplugin_txd = QLineEdit()
        self.serialplugin_txd.setToolTip(self.parent.parent.description('serialplugin_txd'))
        self.serialplugin_timeout = QLineEdit()
        self.serialplugin_timeout.setToolTip(self.parent.parent.description('serialplugin_timeout'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.parent.parent.label("serialplugin_about"), self.serialplugin_about)
        form_layout.addRow(self.parent.parent.label("serialplugin_enabled"), self.serialplugin_enabled)
        form_layout.addRow(self.parent.parent.label("serialplugin_echo"), self.serialplugin_echo)
        form_layout.addRow(self.parent.parent.label("serialplugin_mode"), self.serialplugin_mode)
        form_layout.addRow(self.parent.parent.label("serialplugin_txd"), self.serialplugin_txd)
        form_layout.addRow(self.parent.parent.label("serialplugin_rxd"), self.serialplugin_rxd)
        form_layout.addRow(self.parent.parent.label("serialplugin_timeout"), self.serialplugin_timeout)
        form_layout.addRow(self.tr(""), self.button_box)
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

                if self.prefs.serialplugin_enabled and self.prefs.serialplugin_enabled is True:
                    self.serialplugin_enabled.setChecked(True)

                if self.prefs.serialplugin_echo and self.prefs.serialplugin_echo is True:
                    self.serialplugin_enabled.setChecked(True)

                if self.prefs.serialplugin_mode:
                    self.serialplugin_mode.setText(f'{self.prefs.serialplugin_mode}')
                else:
                    self.serialplugin_mode.setText("0")

                if self.prefs.serialplugin_rxd:
                    self.serialplugin_rxd.setText(f'{self.prefs.serialplugin_rxd}')
                else:
                    self.serialplugin_rxd.setText("0")

                if self.prefs.serialplugin_timeout:
                    self.serialplugin_timeout.setText(f'{self.prefs.serialplugin_timeout}')
                else:
                    self.serialplugin_timeout.setText("0")

                if self.prefs.serialplugin_txd:
                    self.serialplugin_txd.setText(f'{self.prefs.serialplugin_txd}')
                else:
                    self.serialplugin_txd.setText("0")

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'serialplugin_enabled', f'{self.serialplugin_enabled.isChecked()}')
                setPref(prefs, 'serialplugin_echo', f'{self.serialplugin_echo.isChecked()}')
                setPref(prefs, 'serialplugin_mode', zero_if_blank(self.serialplugin_mode.text()))
                setPref(prefs, 'serialplugin_rxd', zero_if_blank(self.serialplugin_rxd.text()))
                setPref(prefs, 'serialplugin_txd', zero_if_blank(self.serialplugin_txd.text()))
                setPref(prefs, 'serialplugin_timeout', zero_if_blank(self.serialplugin_timeout.text()))
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
