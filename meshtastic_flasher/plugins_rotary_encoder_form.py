"""class for the rotary encoder plugin settings"""


from PySide6 import QtCore
from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QDialogButtonBox, QLineEdit, QLabel, QComboBox

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref
from meshtastic_flasher.util import zero_if_blank


class RotaryEncoderForm(QDialog):
    """serial plugin settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(RotaryEncoderForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Rotary Encoder Plugin Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.rotary1_about = QLabel(self.parent.parent.doc_url('rotary1_about'))
        self.rotary1_about.setOpenExternalLinks(True)
        self.rotary1_about.setTextFormat(QtCore.Qt.RichText)
        self.rotary1_about.setToolTip("Link shows more info about the settings for this plugin.")
        self.rotary1_enabled = QCheckBox()
        self.rotary1_enabled.setToolTip(self.parent.parent.description('rotary1_enabled'))
        self.rotary1_event_cw = QComboBox()
        self.rotary1_event_cw.setToolTip(self.parent.parent.description('rotary1_event_cw'))
        self.rotary1_event_cw.setMinimumContentsLength(17)
        self.rotary1_event_ccw = QComboBox()
        self.rotary1_event_ccw.setToolTip(self.parent.parent.description('rotary1_event_ccw'))
        self.rotary1_event_ccw.setMinimumContentsLength(17)
        self.rotary1_event_press = QComboBox()
        self.rotary1_event_press.setToolTip(self.parent.parent.description('rotary1_event_press'))
        self.rotary1_event_press.setMinimumContentsLength(17)
        self.rotary1_pin_a = QLineEdit()
        self.rotary1_pin_a.setToolTip(self.parent.parent.description('rotary1_pin_a'))
        self.rotary1_pin_b = QLineEdit()
        self.rotary1_pin_b.setToolTip(self.parent.parent.description('rotary1_pin_b'))
        self.rotary1_pin_press = QLineEdit()
        self.rotary1_pin_press.setToolTip(self.parent.parent.description('rotary1_pin_press'))

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.parent.parent.label("rotary1_about"), self.rotary1_about)
        form_layout.addRow(self.parent.parent.label("rotary1_enabled"), self.rotary1_enabled)
        form_layout.addRow(self.parent.parent.label("rotary1_event_cw"), self.rotary1_event_cw)
        form_layout.addRow(self.parent.parent.label("rotary1_event_ccw"), self.rotary1_event_ccw)
        form_layout.addRow(self.parent.parent.label("rotary1_event_press"), self.rotary1_event_press)
        form_layout.addRow(self.parent.parent.label("rotary1_pin_a"), self.rotary1_pin_a)
        form_layout.addRow(self.parent.parent.label("rotary1_pin_b"), self.rotary1_pin_b)
        form_layout.addRow(self.parent.parent.label("rotary1_pin_press"), self.rotary1_pin_press)
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

                if self.prefs.rotary1_enabled and self.prefs.rotary1_enabled is True:
                    self.rotary1_enabled.setChecked(True)

                temp = 0
                if self.prefs.rotary1_event_cw:
                    temp = int(self.prefs.rotary1_event_cw)
                print(f'temp:{temp}')
                self.rotary1_event_cw.clear()
                desc = meshtastic.radioconfig_pb2.InputEventChar.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    print(f'k:{k} v.number:{v.number}')
                    self.rotary1_event_cw.addItem(k, v.number)
                temp2 = self.rotary1_event_cw.findData(temp)
                if temp2 != -1:
                    self.rotary1_event_cw.setCurrentIndex(temp2)

                temp = 0
                if self.prefs.rotary1_event_ccw:
                    temp = int(self.prefs.rotary1_event_ccw)
                print(f'temp:{temp}')
                self.rotary1_event_ccw.clear()
                desc = meshtastic.radioconfig_pb2.InputEventChar.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    print(f'k:{k} v.number:{v.number}')
                    self.rotary1_event_ccw.addItem(k, v.number)
                temp2 = self.rotary1_event_ccw.findData(temp)
                if temp2 != -1:
                    self.rotary1_event_ccw.setCurrentIndex(temp2)

                temp = 0
                if self.prefs.rotary1_event_press:
                    temp = int(self.prefs.rotary1_event_press)
                print(f'temp:{temp}')
                self.rotary1_event_press.clear()
                desc = meshtastic.radioconfig_pb2.InputEventChar.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    print(f'k:{k} v.number:{v.number}')
                    self.rotary1_event_press.addItem(k, v.number)
                temp2 = self.rotary1_event_press.findData(temp)
                if temp2 != -1:
                    self.rotary1_event_press.setCurrentIndex(temp2)

                if self.prefs.rotary1_pin_a:
                    self.rotary1_pin_a.setText(f'{self.prefs.rotary1_pin_a}')
                else:
                    self.rotary1_pin_a.setText("0")

                if self.prefs.rotary1_pin_b:
                    self.rotary1_pin_b.setText(f'{self.prefs.rotary1_pin_b}')
                else:
                    self.rotary1_pin_b.setText("0")

                if self.prefs.rotary1_pin_press:
                    self.rotary1_pin_press.setText(f'{self.prefs.rotary1_pin_press}')
                else:
                    self.rotary1_pin_press.setText("0")


        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'rotary1_enabled', f'{self.rotary1_enabled.isChecked()}')
                setPref(prefs, 'rotary1_event_cw', f'{self.rotary1_event_cw.currentData()}')
                setPref(prefs, 'rotary1_event_ccw', f'{self.rotary1_event_ccw.currentData()}')
                setPref(prefs, 'rotary1_event_press', f'{self.rotary1_event_press.currentData()}')
                setPref(prefs, 'rotary1_pin_a', zero_if_blank(self.rotary1_pin_a.text()))
                setPref(prefs, 'rotary1_pin_b', zero_if_blank(self.rotary1_pin_b.text()))
                setPref(prefs, 'rotary1_pin_press', zero_if_blank(self.rotary1_pin_press.text()))
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
