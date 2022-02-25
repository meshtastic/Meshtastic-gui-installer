"""class for the canned message plugin settings"""


from PySide6 import QtCore
from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QDialogButtonBox, QLineEdit, QLabel, QTextEdit

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref


class CannedMessageForm(QDialog):
    """canned message settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(CannedMessageForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Canned Message Plugin Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.canned_message_about = QLabel(self.parent.parent.doc_url('canned_message_plugin_about'))
        self.canned_message_about.setOpenExternalLinks(True)
        self.canned_message_about.setTextFormat(QtCore.Qt.RichText)
        self.canned_message_about.setToolTip("Link shows more info about the settings for this plugin.")
        self.canned_message_plugin_enabled = QCheckBox()
        self.canned_message_plugin_enabled.setToolTip(self.parent.parent.description('canned_message_plugin_enabled'))
        self.canned_message_plugin_allow_input_source = QLineEdit()
        self.canned_message_plugin_allow_input_source.setToolTip(self.parent.parent.description('canned_message_plugin_allow_input_source'))
        self.canned_message_plugin_messages = QTextEdit()
        self.canned_message_plugin_messages.setToolTip(self.parent.parent.description('canned_message_plugin_messages'))
        self.canned_message_plugin_send_bell = QCheckBox()
        self.canned_message_plugin_send_bell.setToolTip(self.parent.parent.description('canned_message_plugin_send_bell'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.parent.parent.label("canned_message_plugin_about"), self.canned_message_about)
        form_layout.addRow(self.parent.parent.label("canned_message_plugin_enabled"), self.canned_message_plugin_enabled)
        form_layout.addRow(self.parent.parent.label("canned_message_plugin_send_bell"), self.canned_message_plugin_send_bell)
        form_layout.addRow(self.parent.parent.label("canned_message_plugin_allow_input_source"), self.canned_message_plugin_allow_input_source)
        form_layout.addRow(self.parent.parent.label("canned_message_plugin_messages"), self.canned_message_plugin_messages)
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

                if self.prefs.canned_message_plugin_enabled and self.prefs.canned_message_plugin_enabled is True:
                    self.canned_message_plugin_enabled.setChecked(True)

                if self.prefs.canned_message_plugin_allow_input_source:
                    self.canned_message_plugin_allow_input_source.setText(f'{self.prefs.canned_message_plugin_allow_input_source}')
                else:
                    self.canned_message_plugin_allow_input_source.setText("")

                if self.prefs.canned_message_plugin_send_bell and self.prefs.canned_message_plugin_send_bell is True:
                    self.canned_message_plugin_send_bell.setChecked(True)

                if self.prefs.canned_message_plugin_messages:
                    self.canned_message_plugin_messages.setText(f'{self.prefs.canned_message_plugin_messages}')
                else:
                    self.canned_message_plugin_messages.setText("")


        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'canned_message_plugin_enabled', f'{self.canned_message_plugin_enabled.isChecked()}')
                setPref(prefs, 'canned_message_plugin_allow_input_source', f'{self.canned_message_plugin_allow_input_source.text()}')
                setPref(prefs, 'canned_message_plugin_send_bell', f'{self.canned_message_plugin_send_bell.isChecked()}')
                setPref(prefs, 'canned_message_plugin_messages', self.canned_message_plugin_messages.toPlainText())
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
