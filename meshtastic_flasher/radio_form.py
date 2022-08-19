"""class for the radio settings"""


from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QComboBox, QDialogButtonBox, QLineEdit

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.config_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref
from meshtastic_flasher.util import zero_if_blank


class RadioForm(QDialog):
    """position settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(RadioForm, self).__init__(parent)

        self.parent = parent
        self.main = parent.main

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle(self.main.text('radio_settings'))

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.region = QComboBox()
        self.region.setToolTip(self.main.description('region'))
        self.region.setMinimumContentsLength(17)
        # self.debug_log_enabled = QCheckBox()
        # self.debug_log_enabled.setToolTip(self.main.description('debug_log_enabled'))
        # self.serial_disabled = QCheckBox()
        # self.serial_disabled.setToolTip(self.main.description('serial_disabled'))
        # self.auto_screen_carousel_secs = QLineEdit()
        # self.auto_screen_carousel_secs.setToolTip(self.main.description('auto_screen_carousel_secs'))
        # self.frequency_offset = QLineEdit()
        # self.frequency_offset.setToolTip(self.main.description('frequency_offset'))
        # self.hop_limit = QLineEdit()
        # # TODO: hops_reliable?
        # self.hop_limit.setToolTip(self.main.description('hop_limit'))
        # # TODO: see https://github.com/meshtastic/Meshtastic-python/issues/280 (add when fixed)
        # #self.ignore_incoming = QLineEdit()
        # self.is_lora_tx_disabled = QCheckBox()
        # self.is_lora_tx_disabled.setToolTip(self.main.description('is_lora_tx_disabled'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)


        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.main.label("region"), self.region)
        # form_layout.addRow(self.main.label("debug_log_enabled"), self.debug_log_enabled)
        # form_layout.addRow(self.main.label("serial_disabled"), self.serial_disabled)
        # form_layout.addRow(self.main.label("auto_screen_carousel_secs"), self.auto_screen_carousel_secs)
        # form_layout.addRow(self.main.label("frequency_offset"), self.frequency_offset)
        # form_layout.addRow(self.main.label("hop_limit"), self.hop_limit)
        # #form_layout.addRow(self.main.label("Ignore Incoming"), self.ignore_incoming)
        # form_layout.addRow(self.main.label("is_lora_tx_disabled"), self.is_lora_tx_disabled)
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
                self.prefs = self.interface.getNode(BROADCAST_ADDR).localConfig

                # Handle the int/float/bool arguments
                tmp_r = self.prefs.lora.region or 'Unset'

                count = 0
                self.region.clear()

                desc = meshtastic.config_pb2.Config.LoRaConfig.RegionCode.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    self.region.addItem(k, v.number)
                    if v.number == tmp_r:
                        self.region.setCurrentIndex(count)
                    count = count + 1

                # if self.prefs.debug_log_enabled and self.prefs.debug_log_enabled is True:
                #     self.debug_log_enabled.setChecked(True)

                # if self.prefs.serial_disabled and self.prefs.serial_disabled is True:
                #     self.serial_disabled.setChecked(True)

                # if self.prefs.auto_screen_carousel_secs:
                #     self.auto_screen_carousel_secs.setText(f'{self.prefs.auto_screen_carousel_secs}')
                # else:
                #     self.auto_screen_carousel_secs.setText("0")

                # if self.prefs.frequency_offset:
                #     self.frequency_offset.setText(f'{self.prefs.frequency_offset}')
                # else:
                #     self.frequency_offset.setText("0")

                # if self.prefs.hop_limit:
                #     self.hop_limit.setText(f'{self.prefs.hop_limit}')
                # else:
                #     self.hop_limit.setText("0")

#                if self.prefs.ignore_incoming:
#                    self.ignore_incoming.setText(f'{self.prefs.ignore_incoming}')
#                else:
#                    self.ignore_incoming.setText("0")

                # if self.prefs.is_lora_tx_disabled and self.prefs.is_lora_tx_disabled is True:
                #     self.is_lora_tx_disabled.setChecked(True)

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).localConfig
                setPref(prefs, 'lora.region', f'{self.region.currentData()}')
                # setPref(prefs, 'debug_log_enabled', f'{self.debug_log_enabled.isChecked()}')
                # setPref(prefs, 'serial_disabled', f'{self.serial_disabled.isChecked()}')
                # setPref(prefs, 'auto_screen_carousel_secs', zero_if_blank(self.auto_screen_carousel_secs.text()))
                # setPref(prefs, 'frequency_offset', zero_if_blank(self.frequency_offset.text()))
                # setPref(prefs, 'hop_limit', zero_if_blank(self.hop_limit.text()))
                # #setPref(prefs, 'ignore_incoming', zero_if_blank(self.ignore_incoming.text()))
                # setPref(prefs, 'is_lora_tx_disabled', f'{self.is_lora_tx_disabled.isChecked()}')
                self.interface.getNode(BROADCAST_ADDR).writeConfig('lora')

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
