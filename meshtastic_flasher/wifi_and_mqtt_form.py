"""class for the Wifi and MQTT settings"""


from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QLineEdit, QDialogButtonBox

import meshtastic.serial_interface
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref


class Wifi_and_MQTT_Form(QDialog):
    """wifi and mqtt form"""

    def __init__(self, parent=None):
        """constructor"""
        super(Wifi_and_MQTT_Form, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Wifi & MQTT Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets

        # WiFi
        self.wifi_ap_mode = QCheckBox()
        self.wifi_ap_mode.setToolTip(self.parent.description('wifi_ap_mode'))
        self.wifi_ssid = QLineEdit()
        self.wifi_ssid.setToolTip(self.parent.description('wifi_ssid'))
        self.wifi_ssid.setMaxLength(self.parent.max_size('wifi_ssid'))
        self.wifi_ssid.setFixedWidth(self.parent.max_size('wifi_ssid') * self.parent.pixel_mult)
        self.wifi_password = QLineEdit()
        self.wifi_password.setToolTip(self.parent.description('wifi_password'))
        self.wifi_password.setMaxLength(self.parent.max_size('wifi_password'))
        self.wifi_password.setFixedWidth(self.parent.max_size('wifi_password') * self.parent.pixel_mult)

        # MQTT
        self.mqtt_disabled = QCheckBox()
        self.mqtt_disabled.setToolTip(self.parent.description('mqtt_disabled'))
        self.mqtt_server = QLineEdit()
        self.mqtt_server.setToolTip(self.parent.description('mqtt_server'))
        self.mqtt_server.setMaxLength(self.parent.max_size('mqtt_server'))
        self.mqtt_server.setFixedWidth(self.parent.max_size('mqtt_server') * self.parent.pixel_mult)
        self.mqtt_username = QLineEdit()
        self.mqtt_username.setToolTip(self.parent.description('mqtt_username'))
        self.mqtt_username.setMaxLength(self.parent.max_size('mqtt_username'))
        self.mqtt_username.setFixedWidth(self.parent.max_size('mqtt_username') * self.parent.pixel_mult)
        self.mqtt_password = QLineEdit()
        self.mqtt_password.setToolTip(self.parent.description('mqtt_password'))
        self.mqtt_password.setMaxLength(self.parent.max_size('mqtt_password'))
        self.mqtt_password.setFixedWidth(self.parent.max_size('mqtt_password') * self.parent.pixel_mult)
        self.mqtt_encryption_enabled = QCheckBox()
        self.mqtt_encryption_enabled.setToolTip(self.parent.description('mqtt_encryption_enabled'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)


        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.parent.label("wifi_ap_mode"), self.wifi_ap_mode)
        form_layout.addRow(self.parent.label("wifi_ssid"), self.wifi_ssid)
        form_layout.addRow(self.parent.label("wifi_password"), self.wifi_password)
        form_layout.addRow(self.parent.label("mqtt_disabled"), self.mqtt_disabled)
        form_layout.addRow(self.parent.label("mqtt_server"), self.mqtt_server)
        form_layout.addRow(self.parent.label("mqtt_username"), self.mqtt_username)
        form_layout.addRow(self.parent.label("mqtt_password"), self.mqtt_password)
        form_layout.addRow(self.parent.label("mqtt_encryption_enabled"), self.mqtt_encryption_enabled)
        form_layout.addRow(self.tr(""), self.button_box)
        self.setLayout(form_layout)


    def run(self, port=None, interface=None):
        """load the form"""
        self.port = port
        self.interface = interface
        print(f'port:{port}')
        if self.port:
            print(f'using port:{self.port}')
            self.get_prefs()
            print(f'prefs:{self.prefs}')

            if self.prefs.wifi_ap_mode and self.prefs.wifi_ap_mode is True:
                self.wifi_ap_mode.setChecked(True)

            if self.prefs.wifi_ssid:
                self.wifi_ssid.setText(self.prefs.wifi_ssid)
            else:
                self.wifi_ssid.setText("")

            if self.prefs.wifi_password:
                self.wifi_password.setText(self.prefs.wifi_password)
            else:
                self.wifi_password.setText("")

            if self.prefs.mqtt_disabled and self.prefs.mqtt_disabled is True:
                self.mqtt_disabled.setChecked(True)

            if self.prefs.mqtt_server:
                self.mqtt_server.setText(self.prefs.mqtt_server)
            else:
                self.mqtt_server.setText("")

            if self.prefs.mqtt_username:
                self.mqtt_username.setText(self.prefs.mqtt_username)
            else:
                self.mqtt_username.setText("")

            if self.prefs.mqtt_password:
                self.mqtt_password.setText(self.prefs.mqtt_password)
            else:
                self.mqtt_password.setText("")

            if self.prefs.mqtt_encryption_enabled and self.prefs.mqtt_encryption_enabled is True:
                self.mqtt_encryption_enabled.setChecked(True)

            self.show()


    def get_prefs(self):
        """Get preferences from device"""
        try:
            if self.interface is None:
                print('interface was none?')
                self.interface = meshtastic.serial_interface.SerialInterface(devPath=self.port)
            if self.interface:
                self.prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
        except Exception as e:
            print(f'Exception:{e}')


    def write_prefs(self):
        """Write preferences to device"""
        try:
            if self.interface:
                print("Writing modified preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'wifi_ap_mode', f'{self.wifi_ap_mode.isChecked()}' )
                setPref(prefs, 'wifi_ssid', self.wifi_ssid.text())
                # only write the password if is not the "obscured" password
                if self.wifi_password.text() != 'sekrit':
                    setPref(prefs, 'wifi_password', self.wifi_password.text())
                else:
                    print('Not saving the password.')
                setPref(prefs, 'mqtt_disabled', f'{self.mqtt_disabled.isChecked()}' )
                setPref(prefs, 'mqtt_server', self.mqtt_server.text())
                setPref(prefs, 'mqtt_username', self.mqtt_username.text())
                setPref(prefs, 'mqtt_password', self.mqtt_password.text())
                setPref(prefs, 'mqtt_encryption_enabled', f'{self.mqtt_encryption_enabled.isChecked()}' )
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
        self.write_prefs()
