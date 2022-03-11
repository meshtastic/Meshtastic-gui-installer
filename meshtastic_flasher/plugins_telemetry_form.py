"""class for the telemetry module settings"""


from PySide6 import QtCore
from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QComboBox, QDialogButtonBox, QLineEdit, QLabel

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref
from meshtastic_flasher.util import zero_if_blank


class TelemetryForm(QDialog):
    """telemetry module form"""

    def __init__(self, parent=None):
        """constructor"""
        super(TelemetryForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Telemetry Module Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.telemetry_module_about = QLabel(self.parent.parent.doc_url('telemetry_module_about'))
        self.telemetry_module_about.setOpenExternalLinks(True)
        self.telemetry_module_about.setTextFormat(QtCore.Qt.RichText)
        self.telemetry_module_about.setToolTip("Link shows more info about the settings for this plugin.")
        self.telemetry_module_measurement_enabled = QCheckBox()
        self.telemetry_module_measurement_enabled.setToolTip(self.parent.parent.description('telemetry_module_measurement_enabled'))
        self.telemetry_module_display_farenheit = QCheckBox()
        self.telemetry_module_display_farenheit.setToolTip(self.parent.parent.description('telemetry_module_display_farenheit'))
        self.telemetry_module_read_error_count_threshold = QLineEdit()
        self.telemetry_module_read_error_count_threshold.setToolTip(self.parent.parent.description('telemetry_module_read_error_count_threshold'))
        self.telemetry_module_recovery_interval = QLineEdit()
        self.telemetry_module_recovery_interval.setToolTip(self.parent.parent.description('telemetry_module_recovery_interval'))
        self.telemetry_module_screen_enabled = QCheckBox()
        self.telemetry_module_screen_enabled.setToolTip(self.parent.parent.description('telemetry_module_screen_enabled'))
        self.telemetry_module_sensor_pin = QLineEdit()
        self.telemetry_module_sensor_pin.setToolTip(self.parent.parent.description('telemetry_module_sensor_pin'))
        self.telemetry_module_sensor_type = QComboBox()
        self.telemetry_module_sensor_type.setToolTip(self.parent.parent.description('telemetry_module_sensor_type'))
        self.telemetry_module_sensor_type.setMinimumContentsLength(17)
        self.telemetry_module_update_interval = QLineEdit()
        self.telemetry_module_update_interval.setToolTip(self.parent.parent.description('telemetry_module_update_interval'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.parent.parent.label("telemetry_module_about"), self.telemetry_module_about)
        form_layout.addRow(self.parent.parent.label("telemetry_module_measurement_enabled"), self.telemetry_module_measurement_enabled)
        form_layout.addRow(self.parent.parent.label("telemetry_module_display_farenheit"), self.telemetry_module_display_farenheit)
        form_layout.addRow(self.parent.parent.label("telemetry_module_read_error_count_threshold"), self.telemetry_module_read_error_count_threshold)
        form_layout.addRow(self.parent.parent.label("telemetry_module_recovery_interval"), self.telemetry_module_recovery_interval)
        form_layout.addRow(self.parent.parent.label("telemetry_module_screen_enabled"), self.telemetry_module_screen_enabled)
        form_layout.addRow(self.parent.parent.label("telemetry_module_sensor_pin"), self.telemetry_module_sensor_pin)
        form_layout.addRow(self.parent.parent.label("telemetry_module_sensor_type"), self.telemetry_module_sensor_type)
        form_layout.addRow(self.parent.parent.label("telemetry_module_update_interval"), self.telemetry_module_update_interval)
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

                if self.prefs.telemetry_module_display_farenheit and self.prefs.telemetry_module_display_farenheit is True:
                    self.telemetry_module_display_farenheit.setChecked(True)

                if self.prefs.telemetry_module_measurement_enabled and self.prefs.telemetry_module_measurement_enabled is True:
                    self.telemetry_module_measurement_enabled.setChecked(True)

                if self.prefs.telemetry_module_read_error_count_threshold:
                    self.telemetry_module_read_error_count_threshold.setText(f'{self.prefs.telemetry_module_read_error_count_threshold}')
                else:
                    self.telemetry_module_read_error_count_threshold.setText("0")

                if self.prefs.telemetry_module_recovery_interval:
                    self.telemetry_module_recovery_interval.setText(f'{self.prefs.telemetry_module_recovery_interval}')
                else:
                    self.telemetry_module_recovery_interval.setText("0")

                if self.prefs.telemetry_module_screen_enabled and self.prefs.telemetry_module_screen_enabled is True:
                    self.telemetry_module_screen_enabled.setChecked(True)

                if self.prefs.telemetry_module_sensor_pin:
                    self.telemetry_module_sensor_pin.setText(f'{self.prefs.telemetry_module_sensor_pin}')
                else:
                    self.telemetry_module_sensor_pin.setText("0")

                temp = 0
                if self.prefs.telemetry_module_sensor_type:
                    temp = int(self.prefs.telemetry_module_sensor_type)
                self.telemetry_module_sensor_type.clear()
                # pylint: disable=no-member
                desc = meshtastic.radioconfig_pb2.RadioConfig.UserPreferences.TelemetrySensorType.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    self.telemetry_module_sensor_type.addItem(k, v.number)
                    if v.number == temp:
                        self.telemetry_module_sensor_type.setCurrentIndex(v.number)

                if self.prefs.telemetry_module_update_interval:
                    self.telemetry_module_update_interval.setText(f'{self.prefs.telemetry_module_update_interval}')
                else:
                    self.telemetry_module_update_interval.setText("0")

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'telemetry_module_display_farenheit', f'{self.telemetry_module_display_farenheit.isChecked()}')
                setPref(prefs, 'telemetry_module_measurement_enabled', f'{self.telemetry_module_measurement_enabled.isChecked()}')
                setPref(prefs, 'telemetry_module_read_error_count_threshold', zero_if_blank(self.telemetry_module_read_error_count_threshold.text()))
                setPref(prefs, 'telemetry_module_recovery_interval', zero_if_blank(self.telemetry_module_recovery_interval.text()))
                setPref(prefs, 'telemetry_module_screen_enabled', f'{self.telemetry_module_screen_enabled.isChecked()}')
                setPref(prefs, 'telemetry_module_sensor_pin', zero_if_blank(self.telemetry_module_sensor_pin.text()))
                setPref(prefs, 'telemetry_module_sensor_type', f'{self.telemetry_module_sensor_type.currentData()}')
                setPref(prefs, 'telemetry_module_update_interval', zero_if_blank(self.telemetry_module_update_interval.text()))
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
