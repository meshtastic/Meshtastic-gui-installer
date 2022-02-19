"""class for the user settings"""


from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QLineEdit, QLabel, QComboBox, QDialogButtonBox

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
from meshtastic.__init__ import BROADCAST_ADDR


class UserForm(QDialog):
    """user settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(UserForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("User Settings")

        self.port = None
        self.interface = None

        # Create widgets
        self.device_id = QLabel()
        self.hardware = QLabel()
        self.mac_address = QLabel()
        self.long_name = QLineEdit()
        self.short_name = QLineEdit()
        self.licensed_operator = QCheckBox()
        self.team = QComboBox()
        self.team.setMinimumContentsLength(17)

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Device ID"), self.device_id)
        form_layout.addRow(self.tr("Hardware"), self.hardware)
        form_layout.addRow(self.tr("Mac Address"), self.mac_address)
        form_layout.addRow(self.tr("Long Name"), self.long_name)
        form_layout.addRow(self.tr("Short Name"), self.short_name)
        form_layout.addRow(self.tr("Licensed Operator?"), self.licensed_operator)
        form_layout.addRow(self.tr("Team"), self.team)
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
            if self.interface:
                for n in self.interface.nodes.values():
                    if n['num'] == self.interface.myInfo.my_node_num:

                        if 'id' in n['user']:
                            self.device_id.setText(n['user']['id'])
                        else:
                            self.device_id.setText('')

                        if 'hwModel' in n['user']:
                            self.hardware.setText(n['user']['hwModel'])
                        else:
                            self.hardware.setText('')

                        if 'macaddr' in n['user']:
                            self.mac_address.setText(meshtastic.util.convert_mac_addr(n['user']['macaddr']))
                        else:
                            self.mac_address.setText('')

                        if 'longName' in n['user']:
                            self.long_name.setText(n['user']['longName'])
                        else:
                            self.long_name.setText('')

                        if 'shortName' in n['user']:
                            self.short_name.setText(n['user']['shortName'])
                        else:
                            self.short_name.setText('')

                        if 'licensed_operator' in n['user']:
                            self.licensed_operator.setChecked(True)

                        tmp_team = 'CLEAR'
                        if 'team' in n['user']:
                            tmp_team = n['user']['team']
                            print(f'tmp_team:{tmp_team}')
                        count = 0
                        self.team.clear()
                        desc = meshtastic.mesh_pb2.Team.DESCRIPTOR
                        for k,v in desc.values_by_name.items():
                            self.team.addItem(k, v.number)
                            if k == tmp_team:
                                self.team.setCurrentIndex(count)
                            count = count + 1

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing values to device")
                self.interface.getNode(BROADCAST_ADDR).setOwner(long_name=self.long_name.text(), short_name=self.short_name.text(), is_licensed=self.licensed_operator.isChecked(), team=self.team.currentData())
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
