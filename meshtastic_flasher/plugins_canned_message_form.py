"""class for the canned message module settings"""


from PySide6 import QtCore
from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QDialogButtonBox, QLineEdit, QLabel, QTextEdit

from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref


class CannedMessageForm(QDialog):
    """canned message module settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(CannedMessageForm, self).__init__(parent)

        self.parent = parent
        self.main = parent.main

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle(self.main.text("canned_message_module_settings"))

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.canned_message_about = QLabel(self.main.doc_url('canned_message_module_about'))
        self.canned_message_about.setOpenExternalLinks(True)
        self.canned_message_about.setTextFormat(QtCore.Qt.RichText)
        self.canned_message_about.setToolTip(self.main.tooltip('module_link'))
        self.canned_message_module_enabled = QCheckBox()
        self.canned_message_module_enabled.setToolTip(self.main.description('canned_message_module_enabled'))
        self.canned_message_module_allow_input_source = QLineEdit()
        self.canned_message_module_allow_input_source.setToolTip(self.main.description('canned_message_module_allow_input_source'))
        self.canned_message_module_messages = QTextEdit()
        self.canned_message_module_messages.setToolTip(self.main.description('canned_message_module_messages'))
        self.canned_message_module_send_bell = QCheckBox()
        self.canned_message_module_send_bell.setToolTip(self.main.description('canned_message_module_send_bell'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.main.label("canned_message_module_about"), self.canned_message_about)
        form_layout.addRow(self.main.label("canned_message_module_enabled"), self.canned_message_module_enabled)
        form_layout.addRow(self.main.label("canned_message_module_send_bell"), self.canned_message_module_send_bell)
        form_layout.addRow(self.main.label("canned_message_module_allow_input_source"), self.canned_message_module_allow_input_source)
        form_layout.addRow(self.main.label("canned_message_module_messages"), self.canned_message_module_messages)
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
            if self.interface:
                self.prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences

                if self.prefs.canned_message_module_enabled and self.prefs.canned_message_module_enabled is True:
                    self.canned_message_module_enabled.setChecked(True)

                if self.prefs.canned_message_module_allow_input_source:
                    self.canned_message_module_allow_input_source.setText(f'{self.prefs.canned_message_module_allow_input_source}')
                else:
                    self.canned_message_module_allow_input_source.setText("")

                if self.prefs.canned_message_module_send_bell and self.prefs.canned_message_module_send_bell is True:
                    self.canned_message_module_send_bell.setChecked(True)

                # TODO: change me
                #if self.prefs.canned_message_module_messages:
                    #self.canned_message_module_messages.setText(f'{self.prefs.canned_message_module_messages}')
                #else:
                    #self.canned_message_module_messages.setText("")


        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'canned_message_module_enabled', f'{self.canned_message_module_enabled.isChecked()}')
                setPref(prefs, 'canned_message_module_allow_input_source', f'{self.canned_message_module_allow_input_source.text()}')
                setPref(prefs, 'canned_message_module_send_bell', f'{self.canned_message_module_send_bell.isChecked()}')
                # TODO setPref(prefs, 'canned_message_module_messages', self.canned_message_module_messages.toPlainText())
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
