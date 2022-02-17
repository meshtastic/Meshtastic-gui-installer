"""class for the channels settings"""


from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QComboBox, QDialogButtonBox, QLineEdit

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR


class ChannelsForm(QDialog):
    """channels settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(ChannelsForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Channel Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.name = QLineEdit() # for primary, it is always primary
        self.name.setReadOnly(True) # primary channel name cannot be changed
        self.name.setText("Primary") # name for primary channel (for display only)
        #self.enabled = QCheckBox()
        #self.enabled.setChecked(True) # primary is always enabled
        #self.enabled.setReadOnly(True) # primary channel is always enabled
        self.key_size = QComboBox()
        self.key_size.setMinimumContentsLength(17)
        self.psk = QLineEdit()
        self.uplink_enabled = QCheckBox()
        self.downlink_enabled = QCheckBox()

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Name"), self.name)
        #form_layout.addRow(self.tr("Enabled"), self.enabled)
        form_layout.addRow(self.tr("Key size"), self.key_size)
        form_layout.addRow(self.tr("Pre-Shared Key"), self.psk)
        form_layout.addRow(self.tr("Uplink enabled"), self.uplink_enabled)
        form_layout.addRow(self.tr("Downlink enabled"), self.downlink_enabled)
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
                ch = self.interface.localNode.getChannelByChannelIndex(0)
                print(f'ch:{ch}')
                self.prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences

                # setup key size drop down
                # if len(psk) == 0: no encryption
                # elif len(psk) == 16 bytes '128 Bit'
                # elif len(psk) == 32 bytes '256 Bit'
                self.key_size.addItem('No encryption', 0)
                self.key_size.addItem('128 Bit', 1)
                self.key_size.addItem('256 Bit', 2)

                if len(ch.settings.psk) == 1 and ch.settings.psk == b'\001':
                    self.key_size.setCurrentIndex(0)

                self.psk = ch.settings.psk

                if ch.settings.uplink_enabled:
                    self.uplink_enabled.setChecked(True)

                if ch.settings.downlink_enabled:
                    self.downlink_enabled.setChecked(True)


        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                # TODO: Should we only write if we changed values?
                print("Writing preferences to device")
                # TODO:
                #prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                #setPref(prefs, 'charge_current', f'{self.charge_current.currentData()}')
                #setPref(prefs, 'is_always_powered', f'{self.is_always_powered.isChecked()}')
                #setPref(prefs, 'is_low_power', f'{self.is_low_power.isChecked()}')
                #self.interface.getNode(BROADCAST_ADDR).writeConfig()

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
