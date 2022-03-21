"""class for the fixed position settings"""

import geocoder

from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QDialogButtonBox, QLineEdit, QPushButton

from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref

from meshtastic_flasher.util import zero_if_blank


class FixedPositionForm(QDialog):
    """fixed position form"""

    def __init__(self, parent=None):
        """constructor"""
        super(FixedPositionForm, self).__init__(parent)

        self.parent = parent
        self.main = parent.main

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle(self.main.text('fixed_position_settings'))

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.fixed_position = QCheckBox()
        self.fixed_position.setToolTip(self.main.description('fixed_position'))
        self.lat = QLineEdit()
        self.lat.setToolTip(self.main.description('lat'))
        self.lon = QLineEdit()
        self.lon.setToolTip(self.main.description('lon'))
        self.alt = QLineEdit()
        self.alt.setToolTip(self.main.description('alt'))
        self.get_location_using_ip_button = QPushButton(self.main.text('get_lat_lon_using_ip'))
        self.get_location_using_ip_button.clicked.connect(self.latlon)

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.main.label("fixed_position"), self.fixed_position)
        form_layout.addRow("", self.get_location_using_ip_button)
        form_layout.addRow(self.main.label("lat"), self.lat)
        form_layout.addRow(self.main.label("lon"), self.lon)
        form_layout.addRow(self.main.label("alt"), self.alt)
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
                lat = float(zero_if_blank(self.lat.text()))
                lon = float(zero_if_blank(self.lon.text()))
                alt = float(zero_if_blank(self.alt.text()))
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
