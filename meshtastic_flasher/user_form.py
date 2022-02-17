"""class for the user settings"""


from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox, QFormLayout, QLineEdit, QMessageBox, QLabel, QComboBox

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
from meshtastic.__init__ import BROADCAST_ADDR


class UserForm(QDialog):
    """user settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(UserForm, self).__init__(parent)

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

        self.ok_button = QPushButton("OK")

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Device ID"), self.device_id)
        form_layout.addRow(self.tr("Hardware"), self.hardware)
        form_layout.addRow(self.tr("Mac Address"), self.mac_address)
        form_layout.addRow(self.tr("Long Name"), self.long_name)
        form_layout.addRow(self.tr("Short Name"), self.short_name)
        form_layout.addRow(self.tr("Licensed Operator?"), self.licensed_operator)
        form_layout.addRow(self.tr("Team"), self.team)
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

                for n in self.interface.nodes.values():
                    if n['num'] == self.interface.myInfo.my_node_num:
                        print(f'n:{n}')
                        if 'id' in n['user']:
                            self.device_id.setText(n['user']['id'])
                        if 'hwModel' in n['user']:
                            self.hardware.setText(n['user']['hwModel'])
                        if 'macaddr' in n['user']:
                            self.mac_address.setText(meshtastic.util.convert_mac_addr(n['user']['macaddr']))
                        if 'longName' in n['user']:
                            self.long_name.setText(n['user']['longName'])
                        if 'shortName' in n['user']:
                            self.short_name.setText(n['user']['shortName'])
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
                # TODO: Should we only write if we changed values?
                self.interface.getNode(BROADCAST_ADDR).setOwner(long_name=self.long_name.text(), short_name=self.short_name.text(), is_licensed=self.licensed_operator.isChecked(), team=self.team.currentData())
        except Exception as e:
            print(f'Exception:{e}')


    def close_form(self):
        """Close the form"""
        print('OK button was clicked')
        self.write_values()
        self.interface.close()
        self.interface = None # so any saved values are re-read upon next form use
        self.close()
