"""class for the power settings"""


from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox, QFormLayout, QMessageBox, QComboBox

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

        self.ok_button = QPushButton("OK")

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Charge Current"), self.charge_current)
        form_layout.addRow(self.tr("Always Powered"), self.is_always_powered)
        form_layout.addRow(self.tr("Powered by low powere source (solar)"), self.is_low_power)
        form_layout.addRow(self.tr(""), self.ok_button)
        self.setLayout(form_layout)

        self.ok_button.clicked.connect(self.close_form)


    def run(self):
        """load the form"""
        self.port = self.parent().select_port.currentText()
        if self.port:
            print(f'using port:{self.port}')
            self.get_values()
            self.show()
        else:
            print('We do not have a port.')
            QMessageBox.information(self, "Info", "Need a port. Click DETECT DEVICE.")
            self.close()


    def get_values(self):
        """Get values from device"""
        try:
            if self.interface is None:
                self.interface = meshtastic.serial_interface.SerialInterface(devPath=self.port)
            if self.interface:
                self.prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences

                tmp_cc = 'MAUnset'
                if self.prefs.location_share:
                    tmp_cc = self.prefs.charge_current
                    print(f'tmp_cc:{tmp_cc}')
                count = 0
                self.charge_current.clear()
                desc = meshtastic.radioconfig_pb2.ChargeCurrent.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    self.charge_current.addItem(k, v.number)
                    if k == tmp_cc:
                        self.charge_current.setCurrentIndex(count)
                    count = count + 1

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
                setPref(prefs, 'charge_current', self.charge_current.currentData())
                setPref(prefs, 'is_always_powered', self.is_always_powered.text())
                setPref(prefs, 'is_low_power', self.is_low_power.text())
                self.interface.getNode(BROADCAST_ADDR).writeConfig()

        except Exception as e:
            print(f'Exception:{e}')


    def close_form(self):
        """Close the form"""
        print('OK button was clicked')
        self.write_values()
        self.interface.close()
        self.interface = None # so any saved values are re-read upon next form use
        self.close()
