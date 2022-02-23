"""class for the fixed position settings"""

import geocoder

from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QDialogButtonBox, QLineEdit, QPushButton

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref


class FixedPositionForm(QDialog):
    """fixed position form"""

    def __init__(self, parent=None):
        """constructor"""
        super(FixedPositionForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Fixed Position Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.fixed_position = QCheckBox()
        self.fixed_position.setToolTip(self.parent.parent.description('fixed_position'))
        self.lat = QLineEdit()
        self.lat.setToolTip(self.parent.parent.description('lat'))
        self.lon = QLineEdit()
        self.lon.setToolTip(self.parent.parent.description('lon'))
        self.alt = QLineEdit()
        self.alt.setToolTip(self.parent.parent.description('alt'))
        self.get_location_using_ip_button = QPushButton("Get Lat/Lon using your IP")
        self.get_location_using_ip_button.clicked.connect(self.latlon)

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.parent.parent.label("fixed_position"), self.fixed_position)
        form_layout.addRow("", self.get_location_using_ip_button)
        form_layout.addRow(self.parent.parent.label("lat"), self.lat)
        form_layout.addRow(self.parent.parent.label("lon"), self.lon)
        form_layout.addRow(self.parent.parent.label("alt"), self.alt)
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

                if self.prefs.fixed_position and self.prefs.fixed_position is True:
                    self.fixed_position.setChecked(True)

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'fixed_position', f'{self.fixed_position.isChecked()}')
                self.interface.getNode(BROADCAST_ADDR).writeConfig()
                lat = float(self.lat.text())
                lon = float(self.lon.text())
                alt = float(self.alt.text())
                print(f'lat:{lat} lon:{lon} alt:{alt}')
                self.interface.sendPosition(lat, lon, alt)

        except Exception as e:
            print(f'Exception:{e}')


    def accept(self):
        """Close the form"""
        print('SAVE button was clicked')
        self.write_values()


    def latlon(self):
        """Set lat and lon from ip using geocoder"""
        print('set lat and lon from ip using geocoder')
        g = geocoder.ip('me')
        self.lat.setText(f'{g.latlng[0]}')
        self.lon.setText(f'{g.latlng[1]}')
