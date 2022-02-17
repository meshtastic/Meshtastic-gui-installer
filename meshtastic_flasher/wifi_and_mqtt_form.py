"""class for the Wifi and MQTT settings"""


from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox, QFormLayout, QLineEdit, QMessageBox

import meshtastic.serial_interface
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref


class Wifi_and_MQTT_Form(QDialog):
    """wifi and mqtt form"""

    def __init__(self, parent=None):
        """constructor"""
        super(Wifi_and_MQTT_Form, self).__init__(parent)

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
        self.wifi_ssid = QLineEdit()
        self.wifi_password = QLineEdit()

        # MQTT
        self.mqtt_disabled = QCheckBox()
        self.mqtt_server = QLineEdit()
        self.mqtt_username = QLineEdit()
        self.mqtt_password = QLineEdit()

        self.ok_button = QPushButton("OK")

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Enable Wifi AP"), self.wifi_ap_mode)
        form_layout.addRow(self.tr("Wifi SSID"), self.wifi_ssid)
        form_layout.addRow(self.tr("Wifi Password"), self.wifi_password)
        form_layout.addRow(self.tr("MQTT Disabled"), self.mqtt_disabled)
        form_layout.addRow(self.tr("MQTT Server"), self.mqtt_server)
        form_layout.addRow(self.tr("MQTT Username"), self.mqtt_username)
        form_layout.addRow(self.tr("MQTT Password"), self.mqtt_password)
        form_layout.addRow(self.tr(""), self.ok_button)
        self.setLayout(form_layout)

        self.ok_button.clicked.connect(self.close_form)


    def run(self):
        """load the form"""
        self.port = self.parent().select_port.currentText()
        if self.port:
            print(f'using port:{self.port}')
            self.get_prefs()
            print(f'prefs:{self.prefs}')
            if self.prefs.wifi_ap_mode and self.prefs.wifi_ap_mode is True:
                self.wifi_ap_mode.setChecked(True)
            if self.prefs.wifi_ssid:
                self.wifi_ssid.setText(self.prefs.wifi_ssid)
            if self.prefs.wifi_password:
                self.wifi_password.setText(self.prefs.wifi_password)
            if self.prefs.mqtt_disabled and self.prefs.mqtt_disabled is True:
                self.mqtt_disabled.setChecked(True)
            if self.prefs.mqtt_server:
                self.mqtt_server.setText(self.prefs.mqtt_server)
            if self.prefs.mqtt_username:
                self.mqtt_username.setText(self.prefs.mqtt_username)
            if self.prefs.mqtt_password:
                self.mqtt_password.setText(self.prefs.mqtt_password)
            self.show()
        else:
            print('We do not have a port.')
            QMessageBox.information(self, "Info", "Need a port. Click DETECT DEVICE.")
            self.close()


    def get_prefs(self):
        """Get preferences from device"""
        try:
            if self.interface is None:
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
                setPref(prefs, 'wifi_password', self.wifi_password.text())
                setPref(prefs, 'mqtt_disabled', f'{self.mqtt_disabled.isChecked()}' )
                setPref(prefs, 'mqtt_server', self.mqtt_server.text())
                setPref(prefs, 'mqtt_username', self.mqtt_username.text())
                setPref(prefs, 'mqtt_password', self.mqtt_password.text())
                self.interface.getNode(BROADCAST_ADDR).writeConfig()
        except Exception as e:
            print(f'Exception:{e}')


    def close_form(self):
        """Close the form"""
        print('OK button was clicked')
        self.write_prefs()
        self.interface.close()
        self.interface = None # so any saved values are re-read upon next form use
        self.close()
