"""class for the radio settings"""


from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QComboBox, QDialogButtonBox

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref


class RadioForm(QDialog):
    """position settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(RadioForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Radio Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.is_router = QCheckBox()
        self.region = QComboBox()
        self.region.setMinimumContentsLength(17)
        self.debug_log_enabled = QCheckBox()
        self.serial_disabled = QCheckBox()

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)


        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Is router?"), self.is_router)
        form_layout.addRow(self.tr("Region"), self.region)
        form_layout.addRow(self.tr("Debug Log"), self.debug_log_enabled)
        form_layout.addRow(self.tr("Serial Disabled"), self.serial_disabled)
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

                if self.prefs.is_router:
                    self.is_router.setChecked(True)

                tmp_r = 'Unset'
                if self.prefs.region:
                    tmp_r = self.prefs.region
                    print(f'tmp_r:{tmp_r}')
                count = 0
                self.region.clear()
                desc = meshtastic.radioconfig_pb2.RegionCode.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    self.region.addItem(k, v.number)
                    if v.number == tmp_r:
                        self.region.setCurrentIndex(count)
                    count = count + 1

                if self.prefs.debug_log_enabled:
                    self.debug_log_enabled.setChecked(True)

                if self.prefs.serial_disabled:
                    self.serial_disabled.setChecked(True)

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                # TODO: Should we only write if we changed values?
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'is_router', f'{self.is_router.isChecked()}')
                setPref(prefs, 'region', f'{self.region.currentData()}')
                setPref(prefs, 'debug_log_enabled', f'{self.debug_log_enabled.isChecked()}')
                setPref(prefs, 'serial_disabled', f'{self.serial_disabled.isChecked()}')
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
