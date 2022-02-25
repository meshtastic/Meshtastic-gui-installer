"""class for the plugin store and forward settings"""


from PySide6 import QtCore
from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QDialogButtonBox, QLineEdit, QLabel

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref
from meshtastic_flasher.util import zero_if_blank


class StoreAndForwardForm(QDialog):
    """plugin store and forward settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(StoreAndForwardForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Store and Forward Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.store_forware_plugin_about = QLabel(self.parent.parent.doc_url('store_forware_plugin_about'))
        self.store_forware_plugin_about.setOpenExternalLinks(True)
        self.store_forware_plugin_about.setTextFormat(QtCore.Qt.RichText)
        self.store_forware_plugin_about.setToolTip("Link shows more info about the settings for this plugin.")
        self.store_forward_plugin_enabled = QCheckBox()
        self.store_forward_plugin_enabled.setToolTip(self.parent.parent.description('store_forward_plugin_enabled'))
        self.store_forward_plugin_heartbeat = QCheckBox()
        self.store_forward_plugin_heartbeat.setToolTip(self.parent.parent.description('store_forward_plugin_heartbeat'))
        self.store_forward_plugin_history_return_max = QLineEdit()
        self.store_forward_plugin_history_return_max.setToolTip(self.parent.parent.description('store_forward_plugin_history_return_max'))
        self.store_forward_plugin_history_return_window = QLineEdit()
        self.store_forward_plugin_history_return_window.setToolTip(self.parent.parent.description('store_forward_plugin_history_return_window'))
        self.store_forward_plugin_records = QLineEdit()
        self.store_forward_plugin_records.setToolTip(self.parent.parent.description('store_forward_plugin_records'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.parent.parent.label("store_forware_plugin_about"), self.store_forware_plugin_about)
        form_layout.addRow(self.parent.parent.label("store_forward_plugin_enabled"), self.store_forward_plugin_enabled)
        form_layout.addRow(self.parent.parent.label("store_forward_plugin_heartbeat"), self.store_forward_plugin_heartbeat)
        form_layout.addRow(self.parent.parent.label("store_forward_plugin_history_return_max"), self.store_forward_plugin_history_return_max)
        form_layout.addRow(self.parent.parent.label("store_forward_plugin_history_return_window"), self.store_forward_plugin_history_return_window)
        form_layout.addRow(self.parent.parent.label("store_forward_plugin_records"), self.store_forward_plugin_records)
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

                if self.prefs.store_forward_plugin_enabled and self.prefs.store_forward_plugin_enabled is True:
                    self.store_forward_plugin_enabled.setChecked(True)

                if self.prefs.store_forward_plugin_heartbeat and self.prefs.store_forward_plugin_heartbeat is True:
                    self.store_forward_plugin_heartbeat.setChecked(True)

                if self.prefs.store_forward_plugin_history_return_max:
                    self.store_forward_plugin_history_return_max.setText(f'{self.prefs.store_forward_plugin_history_return_max}')
                else:
                    self.store_forward_plugin_history_return_max.setText("0")

                if self.prefs.store_forward_plugin_history_return_window:
                    self.store_forward_plugin_history_return_window.setText(f'{self.prefs.store_forward_plugin_history_return_window}')
                else:
                    self.store_forward_plugin_history_return_window.setText("0")

                if self.prefs.store_forward_plugin_records:
                    self.store_forward_plugin_records.setText(f'{self.prefs.store_forward_plugin_records}')
                else:
                    self.store_forward_plugin_records.setText("0")

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'store_forward_plugin_enabled', f'{self.store_forward_plugin_enabled.isChecked()}')
                setPref(prefs, 'store_forward_plugin_heartbeat', f'{self.store_forward_plugin_heartbeat.isChecked()}')
                setPref(prefs, 'store_forward_plugin_history_return_max', zero_if_blank(self.store_forward_plugin_history_return_max.text()))
                setPref(prefs, 'store_forward_plugin_history_return_window', zero_if_blank(self.store_forward_plugin_history_return_window.text()))
                setPref(prefs, 'store_forward_plugin_records', zero_if_blank(self.store_forward_plugin_records.text()))
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
