"""class for the plugin range test settings"""


from PySide6 import QtCore
from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QDialogButtonBox, QLineEdit, QLabel

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref
from meshtastic_flasher.util import zero_if_blank


class RangeTestForm(QDialog):
    """plugin range test settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(RangeTestForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Plugins Range Test Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.range_test_about = QLabel(self.parent.parent.doc_url('range_test_plugin_about'))
        self.range_test_about.setOpenExternalLinks(True)
        self.range_test_about.setTextFormat(QtCore.Qt.RichText)
        self.range_test_about.setToolTip("Link shows more info about the settings for this plugin.")
        self.range_test_plugin_enabled = QCheckBox()
        self.range_test_plugin_enabled.setToolTip(self.parent.parent.description('range_test_plugin_enabled'))
        self.range_test_plugin_save = QCheckBox()
        self.range_test_plugin_save.setToolTip(self.parent.parent.description('range_test_plugin_save'))
        self.range_test_plugin_sender = QLineEdit()
        self.range_test_plugin_sender.setToolTip(self.parent.parent.description('range_test_plugin_sender'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.parent.parent.label("range_test_plugin_about"), self.range_test_about)
        form_layout.addRow(self.parent.parent.label("range_test_plugin_enabled"), self.range_test_plugin_enabled)
        form_layout.addRow(self.parent.parent.label("range_test_plugin_save"), self.range_test_plugin_save)
        form_layout.addRow(self.parent.parent.label("range_test_plugin_sender"), self.range_test_plugin_sender)
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

                if self.prefs.range_test_plugin_enabled and self.prefs.range_test_plugin_enabled is True:
                    self.range_test_plugin_enabled.setChecked(True)

                if self.prefs.range_test_plugin_save and self.prefs.range_test_plugin_save is True:
                    self.range_test_plugin_save.setChecked(True)

                if self.prefs.range_test_plugin_sender:
                    self.range_test_plugin_sender.setText(f'{self.prefs.range_test_plugin_sender}')
                else:
                    self.range_test_plugin_sender.setText("0")

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'range_test_plugin_enabled', f'{self.range_test_plugin_enabled.isChecked()}')
                setPref(prefs, 'range_test_plugin_save', f'{self.range_test_plugin_save.isChecked()}')
                setPref(prefs, 'range_test_plugin_sender', zero_if_blank(self.range_test_plugin_sender.text()))
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
