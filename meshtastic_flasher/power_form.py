"""class for the power settings"""


from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QComboBox, QDialogButtonBox, QLineEdit

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref
from meshtastic_flasher.util import zero_if_blank


class PowerForm(QDialog):
    """position settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(PowerForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Power Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.charge_current = QComboBox()
        self.charge_current.setToolTip(self.parent.description('charge_current'))
        self.charge_current.setMinimumContentsLength(17)
        self.is_always_powered = QCheckBox()
        self.is_always_powered.setToolTip(self.parent.description('is_always_powered'))
        self.is_low_power = QCheckBox()
        self.is_low_power.setToolTip(self.parent.description('is_low_power'))
        self.adc_multiplier_override = QLineEdit()
        self.adc_multiplier_override.setToolTip(self.parent.description('adc_multiplier_override'))
        self.is_power_saving = QCheckBox()
        self.is_power_saving.setToolTip(self.parent.description('is_power_saving'))
        self.ls_secs = QLineEdit()
        self.ls_secs.setToolTip(self.parent.description('ls_secs'))
        self.mesh_sds_timeout_secs = QLineEdit()
        self.mesh_sds_timeout_secs.setToolTip(self.parent.description('mesh_sds_timeout_secs'))
        self.min_wake_secs = QLineEdit()
        self.min_wake_secs.setToolTip(self.parent.description('min_wake_secs'))
        self.on_battery_shutdown_after_secs = QLineEdit()
        self.on_battery_shutdown_after_secs.setToolTip(self.parent.description('on_battery_shutdown_after_secs'))
        self.phone_sds_timeout_sec = QLineEdit()
        self.phone_sds_timeout_sec.setToolTip(self.parent.description('phone_sds_timeout_sec'))
        self.phone_timeout_secs = QLineEdit()
        self.phone_timeout_secs.setToolTip(self.parent.description('phone_timeout_secs'))
        self.screen_on_secs = QLineEdit()
        self.screen_on_secs.setToolTip(self.parent.description('screen_on_secs'))
        self.sds_secs = QLineEdit()
        self.sds_secs.setToolTip(self.parent.description('sds_secs'))
        self.wait_bluetooth_secs = QLineEdit()
        self.wait_bluetooth_secs.setToolTip(self.parent.description('wait_bluetooth_secs'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.parent.label("charge_current"), self.charge_current)
        form_layout.addRow(self.parent.label("is_always_powered"), self.is_always_powered)
        form_layout.addRow(self.parent.label("is_low_power"), self.is_low_power)
        form_layout.addRow(self.parent.label("adc_multiplier_override"), self.adc_multiplier_override)
        form_layout.addRow(self.parent.label("is_power_saving"), self.is_power_saving)
        form_layout.addRow(self.parent.label("ls_secs"), self.ls_secs)
        form_layout.addRow(self.parent.label("mesh_sds_timeout_secs"), self.mesh_sds_timeout_secs)
        form_layout.addRow(self.parent.label("min_wake_secs"), self.min_wake_secs)
        form_layout.addRow(self.parent.label("on_battery_shutdown_after_secs"), self.on_battery_shutdown_after_secs)
        form_layout.addRow(self.parent.label("phone_sds_timeout_sec"), self.phone_sds_timeout_sec)
        form_layout.addRow(self.parent.label("phone_timeout_secs"), self.phone_timeout_secs)
        form_layout.addRow(self.parent.label("screen_on_secs"), self.screen_on_secs)
        form_layout.addRow(self.parent.label("sds_secs"), self.sds_secs)
        form_layout.addRow(self.parent.label("wait_bluetooth_secs"), self.wait_bluetooth_secs)
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

                temp = 0
                if self.prefs.charge_current:
                    temp = self.prefs.charge_current
                self.charge_current.clear()
                desc = meshtastic.radioconfig_pb2.ChargeCurrent.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    self.charge_current.addItem(k, v.number)
                    if v.number == temp:
                        self.charge_current.setCurrentIndex(v.number)

                if self.prefs.is_always_powered and self.prefs.is_always_powered is True:
                    self.is_always_powered.setChecked(True)

                if self.prefs.is_low_power and self.prefs.is_low_power is True:
                    self.is_low_power.setChecked(True)

                if self.prefs.adc_multiplier_override:
                    self.adc_multiplier_override.setText(f'{self.prefs.adc_multiplier_override}')
                else:
                    self.adc_multiplier_override.setText("0")

                if self.prefs.is_power_saving and self.prefs.is_power_saving is True:
                    self.is_power_saving.setChecked(True)

                if self.prefs.ls_secs:
                    self.ls_secs.setText(f'{self.prefs.ls_secs}')
                else:
                    self.ls_secs.setText("0")

                if self.prefs.mesh_sds_timeout_secs:
                    self.mesh_sds_timeout_secs.setText(f'{self.prefs.mesh_sds_timeout_secs}')
                else:
                    self.mesh_sds_timeout_secs.setText("0")

                if self.prefs.min_wake_secs:
                    self.min_wake_secs.setText(f'{self.prefs.min_wake_secs}')
                else:
                    self.min_wake_secs.setText("0")

                if self.prefs.on_battery_shutdown_after_secs:
                    self.on_battery_shutdown_after_secs.setText(f'{self.prefs.on_battery_shutdown_after_secs}')
                else:
                    self.on_battery_shutdown_after_secs.setText("0")

                if self.prefs.phone_sds_timeout_sec:
                    self.phone_sds_timeout_sec.setText(f'{self.prefs.phone_sds_timeout_sec}')
                else:
                    self.phone_sds_timeout_sec.setText("0")

                if self.prefs.phone_timeout_secs:
                    self.phone_timeout_secs.setText(f'{self.prefs.phone_timeout_secs}')
                else:
                    self.phone_timeout_secs.setText("0")

                if self.prefs.screen_on_secs:
                    self.screen_on_secs.setText(f'{self.prefs.screen_on_secs}')
                else:
                    self.screen_on_secs.setText("0")

                if self.prefs.sds_secs:
                    self.sds_secs.setText(f'{self.prefs.sds_secs}')
                else:
                    self.sds_secs.setText("0")

                if self.prefs.wait_bluetooth_secs:
                    self.wait_bluetooth_secs.setText(f'{self.prefs.wait_bluetooth_secs}')
                else:
                    self.wait_bluetooth_secs.setText("0")

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'charge_current', f'{self.charge_current.currentData()}')
                setPref(prefs, 'is_always_powered', f'{self.is_always_powered.isChecked()}')
                setPref(prefs, 'is_low_power', f'{self.is_low_power.isChecked()}')
                setPref(prefs, 'adc_multiplier_override', zero_if_blank(self.adc_multiplier_override.text()))
                setPref(prefs, 'is_power_saving', f'{self.is_power_saving.isChecked()}')
                setPref(prefs, 'ls_secs', zero_if_blank(self.ls_secs.text()))
                setPref(prefs, 'mesh_sds_timeout_secs', zero_if_blank(self.mesh_sds_timeout_secs.text()))
                setPref(prefs, 'min_wake_secs', zero_if_blank(self.min_wake_secs.text()))
                setPref(prefs, 'on_battery_shutdown_after_secs', zero_if_blank(self.on_battery_shutdown_after_secs.text()))
                setPref(prefs, 'phone_sds_timeout_sec', zero_if_blank(self.phone_sds_timeout_sec.text()))
                setPref(prefs, 'phone_timeout_secs', zero_if_blank(self.phone_timeout_secs.text()))
                setPref(prefs, 'screen_on_secs', zero_if_blank(self.screen_on_secs.text()))
                setPref(prefs, 'sds_secs', zero_if_blank(self.sds_secs.text()))
                setPref(prefs, 'wait_bluetooth_secs', zero_if_blank(self.wait_bluetooth_secs.text()))
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
