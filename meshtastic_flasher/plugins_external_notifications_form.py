"""class for the external notification module settings"""


from PySide6 import QtCore
from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QDialogButtonBox, QLineEdit, QLabel

from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref
from meshtastic_flasher.util import zero_if_blank


class ExternalNotificationsForm(QDialog):
    """external notification module form"""

    def __init__(self, parent=None):
        """constructor"""
        super(ExternalNotificationsForm, self).__init__(parent)

        self.parent = parent
        self.main = parent.main

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle(self.main.text('ext_notification_module_settings'))

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.ext_notification_about = QLabel(self.main.doc_url('ext_notification_module_about'))
        self.ext_notification_about.setOpenExternalLinks(True)
        self.ext_notification_about.setTextFormat(QtCore.Qt.RichText)
        self.ext_notification_about.setToolTip(self.main.tooltip('module_link'))
        self.ext_notification_module_enabled = QCheckBox()
        self.ext_notification_module_enabled.setToolTip(self.main.description('ext_notification_module_enabled'))
        self.ext_notification_module_active = QCheckBox()
        self.ext_notification_module_active.setToolTip(self.main.description('ext_notification_module_active'))
        self.ext_notification_module_alert_bell = QCheckBox()
        self.ext_notification_module_alert_bell.setToolTip(self.main.description('ext_notification_module_alert_bell'))
        self.ext_notification_module_alert_message = QCheckBox()
        self.ext_notification_module_alert_message.setToolTip(self.main.description('ext_notification_module_alert_message'))
        self.ext_notification_module_output = QLineEdit()
        self.ext_notification_module_output.setToolTip(self.main.description('ext_notification_module_output'))
        self.ext_notification_module_output_ms = QLineEdit()
        self.ext_notification_module_output_ms.setToolTip(self.main.description('ext_notification_module_output_ms'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.main.label("ext_notification_module_about"), self.ext_notification_about)
        form_layout.addRow(self.main.label("ext_notification_module_enabled"), self.ext_notification_module_enabled)
        form_layout.addRow(self.main.label("ext_notification_module_active"), self.ext_notification_module_active)
        form_layout.addRow(self.main.label("ext_notification_module_alert_bell"), self.ext_notification_module_alert_bell)
        form_layout.addRow(self.main.label("ext_notification_module_alert_message"), self.ext_notification_module_alert_message)
        form_layout.addRow(self.main.label("ext_notification_module_output"), self.ext_notification_module_output)
        form_layout.addRow(self.main.label("ext_notification_module_output_ms"), self.ext_notification_module_output_ms)
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

                if self.prefs.ext_notification_module_active and self.prefs.ext_notification_module_active is True:
                    self.ext_notification_module_active.setChecked(True)

                if self.prefs.ext_notification_module_alert_bell and self.prefs.ext_notification_module_alert_bell is True:
                    self.ext_notification_module_alert_bell.setChecked(True)

                if self.prefs.ext_notification_module_alert_message and self.prefs.ext_notification_module_alert_message is True:
                    self.ext_notification_module_alert_message.setChecked(True)

                if self.prefs.ext_notification_module_enabled and self.prefs.ext_notification_module_enabled is True:
                    self.ext_notification_module_enabled.setChecked(True)

                if self.prefs.ext_notification_module_output:
                    self.ext_notification_module_output.setText(f'{self.prefs.ext_notification_module_output}')
                else:
                    self.ext_notification_module_output.setText("0")

                if self.prefs.ext_notification_module_output_ms:
                    self.ext_notification_module_output_ms.setText(f'{self.prefs.ext_notification_module_output_ms}')
                else:
                    self.ext_notification_module_output_ms.setText("0")

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'ext_notification_module_active', f'{self.ext_notification_module_active.isChecked()}')
                setPref(prefs, 'ext_notification_module_alert_bell', f'{self.ext_notification_module_alert_bell.isChecked()}')
                setPref(prefs, 'ext_notification_module_alert_message', f'{self.ext_notification_module_alert_message.isChecked()}')
                setPref(prefs, 'ext_notification_module_enabled', f'{self.ext_notification_module_enabled.isChecked()}')
                setPref(prefs, 'ext_notification_module_output', zero_if_blank(self.ext_notification_module_output.text()))
                setPref(prefs, 'ext_notification_module_output_ms', zero_if_blank(self.ext_notification_module_output_ms.text()))
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
