"""class for the channels settings"""


from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QComboBox, QDialogButtonBox, QLineEdit, QMessageBox, QPushButton

from meshtastic.util import genPSK256, fromPSK
from meshtastic.__init__ import BROADCAST_ADDR

from meshtastic.channel_pb2 import ChannelSettings, Channel
from meshtastic_flasher.util import zero_if_blank

class ChannelForm(QDialog):
    """channels settings form"""

    def __init__(self, parent=None, channel_index=0):
        """constructor"""
        super(ChannelForm, self).__init__(parent)

        self.parent = parent
        self.channel_index = channel_index
        self.use_name = None

        width = 500
        height = 800
        self.setMinimumSize(width, height)
        self.setWindowTitle("Channel Settings")

        self.port = None
        self.interface = None
        self.ch = None
        self.psk = None

        # Create widgets
        self.name = QLineEdit()
        self.role = QComboBox()
        self.role.setMinimumContentsLength(17)
        self.modem_config = None
        if self.channel_index == 0:
            self.name.setReadOnly(True) # primary channel name cannot be changed
            # modem config is only on primary channel
            self.modem_config = QComboBox()
            self.modem_config.setMinimumContentsLength(17)
        self.uplink_enabled = QCheckBox()
        self.downlink_enabled = QCheckBox()
        self.tx_power = QLineEdit()
        self.bandwidth = QLineEdit()
        self.spread_factor = QLineEdit()
        self.coding_rate = QLineEdit()
        self.psk_random_button = QPushButton("PSKRandom")
        self.psk_default_button = QPushButton("PSKDefault")
        # TODO: self.id = QLineEdit()

        self.psk_random_button.clicked.connect(self.psk_random)
        self.psk_default_button.clicked.connect(self.psk_default)

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Name"), self.name)
        form_layout.addRow(self.tr("Role"), self.role)
        if self.channel_index == 0:
            form_layout.addRow(self.tr("Modem Config"), self.modem_config)
        form_layout.addRow(self.tr("Uplink enabled"), self.uplink_enabled)
        form_layout.addRow(self.tr("Downlink enabled"), self.downlink_enabled)
        form_layout.addRow(self.tr("TX Power"), self.tx_power)
        form_layout.addRow(self.tr("Bandwidth"), self.bandwidth)
        form_layout.addRow(self.tr("Spread Factor"), self.spread_factor)
        form_layout.addRow(self.tr("Coding Rate"), self.coding_rate)
        form_layout.addRow(self.tr(""), self.psk_random_button)
        form_layout.addRow(self.tr(""), self.psk_default_button)
        form_layout.addRow(self.tr(""), self.button_box)
        self.setLayout(form_layout)


    def psk_random(self):
        """Generate random psk"""
        print('generated random psk')
        self.psk = fromPSK("random")
        print(f'psk is now:{self.psk}')


    def psk_default(self):
        """Use default psk"""
        print('using default psk')
        self.psk = fromPSK("default")
        print(f'psk is now:{self.psk}')


    def button_state(self, b):
        """Button state"""
        if b.text() == "PSKRandom":
            if b.isChecked():
                print(f'{b.text()} is selected')
            else:
                print(f'{b.text()} is deselected')
        if b.text() == "PSKDefault":
            if b.isChecked():
                print(f'{b.text()} is selected')
            else:
                print(f'{b.text()} is deselected')
        if b.text() == "PSKNone":
            if b.isChecked():
                print(f'{b.text()} is selected')
            else:
                print(f'{b.text()} is deselected')


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

                self.ch = self.interface.localNode.getChannelByChannelIndex(self.channel_index)
                print(f'self.ch:{self.ch}')

                temp = 0
                if self.ch.role:
                    temp = self.ch.role
                self.role.clear()
                desc = Channel.Role.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    if self.channel_index == 0:
                        # only allow primary channel role on primary channel
                        if v.number == 1:
                            self.role.addItem(k, v.number)
                            self.role.setCurrentIndex(0)
                    else:
                        if v.number == 0:
                            self.role.addItem(k, v.number)
                            if v.number == temp:
                                self.role.setCurrentIndex(0)
                        elif v.number == 1:
                            pass
                        elif v.number == 2:
                            self.role.addItem(k, v.number)
                            if v.number == temp:
                                self.role.setCurrentIndex(1)

                if self.modem_config:
                    temp = 0
                    if self.ch.settings.modem_config:
                        temp = self.ch.settings.modem_config
                    self.modem_config.clear()
                    desc = ChannelSettings.ModemConfig.DESCRIPTOR
                    for k,v in desc.values_by_name.items():
                        self.modem_config.addItem(k, v.number)
                        if v.number == temp:
                            self.modem_config.setCurrentIndex(v.number)

                if self.ch.settings.name:
                    self.name.setText(f'{self.ch.settings.name}')
                else:
                    self.name.setText("")
                if self.channel_index == 0:
                    self.name.setText("PRIMARY")

                if self.ch.settings.psk:
                    self.psk = self.ch.settings.psk

                if self.ch.settings.uplink_enabled:
                    self.uplink_enabled.setChecked(True)

                if self.ch.settings.downlink_enabled:
                    self.downlink_enabled.setChecked(True)

                if self.ch.settings.tx_power:
                    self.tx_power.setText(f'{self.tx_power}')
                else:
                    self.tx_power.setText("0")

                if self.ch.settings.bandwidth:
                    self.bandwidth.setText(f'{self.bandwidth}')
                else:
                    self.bandwidth.setText("0")

                if self.ch.settings.spread_factor:
                    self.spread_factor.setText(f'{self.spread_factor}')
                else:
                    self.spread_factor.setText("0")

                if self.ch.settings.coding_rate:
                    self.coding_rate.setText(f'{self.coding_rate}')
                else:
                    self.coding_rate.setText("0")


        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:

                self.use_name = self.name.text()

                if self.use_name == '':
                    QMessageBox.warning(self, "Warning", "Need to have a channel name")

                else:
                    # Primary channel stuff
                    if self.channel_index == 0:
                        self.use_name = "" # primary has no name

                    before = self.interface.localNode.getChannelByChannelIndex(self.channel_index)
                    print(f'before:{before}')

                    ch = Channel()
                    ch.role = self.role.currentData()
                    #ch.settings.channel_num = self.channel_index + 1
                    ch.settings.name = self.use_name
                    if self.channel_index == 0:
                        # ex: chs.modem_config = chs.Bw250Cr46Sf2048
                        ch.settings.modem_config = self.modem_config.currentData()
                    if self.psk is None and self.channel_index != 0:
                        # if there was no PSK (i.e., adding a secondary channel then generate a PSK)
                        self.psk = genPSK256()
                    ch.settings.psk = self.psk
                    ch.settings.uplink_enabled = self.uplink_enabled.isChecked()
                    ch.settings.downlink_enabled = self.downlink_enabled.isChecked()
                    ch.settings.tx_power = int(zero_if_blank(self.tx_power.text()))
                    ch.settings.bandwidth = int(zero_if_blank(self.bandwidth.text()))
                    ch.settings.spread_factor = int(zero_if_blank(self.spread_factor.text()))
                    ch.settings.coding_rate = int(zero_if_blank(self.coding_rate.text()))
                    ch.index = self.channel_index
                    print(f'ch:{ch}')

                    n = self.interface.getNode(BROADCAST_ADDR)

                    print(f'before n.channels:{n.channels}')
                    n.channels[self.channel_index] = ch
                    print(f'after n.channels:{n.channels}')

                    print("Writing modified channels to device")
                    n.writeChannel(self.channel_index)

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
