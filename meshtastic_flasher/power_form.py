"""class for the power settings"""


from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QComboBox, QDialogButtonBox

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref


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
        self.charge_current.setMinimumContentsLength(17)
        self.is_always_powered= QCheckBox()
        self.is_low_power = QCheckBox()

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Charge Current"), self.charge_current)
        form_layout.addRow(self.tr("Always Powered"), self.is_always_powered)
        form_layout.addRow(self.tr("Powered by low powere source (solar)"), self.is_low_power)
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

                if self.prefs.is_always_powered:
                    self.is_always_powered.setChecked(True)

                if self.prefs.is_low_power:
                    self.is_low_power.setChecked(True)

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                # TODO: Should we only write if we changed values?
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'charge_current', f'{self.charge_current.currentData()}')
                setPref(prefs, 'is_always_powered', f'{self.is_always_powered.isChecked()}')
                setPref(prefs, 'is_low_power', f'{self.is_low_power.isChecked()}')
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
