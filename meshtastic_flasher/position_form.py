"""class for the position settings"""


from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QLineEdit, QLabel, QComboBox, QDialogButtonBox

import meshtastic.serial_interface
import meshtastic.util
import meshtastic.mesh_pb2
import meshtastic.radioconfig_pb2
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref
from meshtastic_flasher.util import zero_if_blank


class PositionForm(QDialog):
    """position settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(PositionForm, self).__init__(parent)

        self.parent = parent

        width = 900
        height = 500
        self.setMinimumSize(width, height)
        self.setWindowTitle("Position Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.position_broadcast_secs = QLineEdit()
        self.position_broadcast_smart = QCheckBox()
        self.position_broadcast_smart.setToolTip("Calculates an ideal position update interval based on the data rate of your selected channel configuration.")
        self.position_broadcast_secs.setToolTip("We should send our position this often (but only if it has changed significantly). Defaults to 900 seconds (15 minutes).")
        self.position_flag_altitude = QCheckBox("Include altitude", self)
        self.position_flag_alt_msl = QCheckBox("Altitude is MSL", self) # TODO: what is MSL?
        self.position_flag_geo_sep = QCheckBox("Include geoidal separation", self)
        self.position_flag_dop = QCheckBox("Include the DOP value (PDOP is used by default)")
        self.position_flag_hvdop = QCheckBox("If DOP is set, send separate HDOP / VDOP values instead of PDOP")
        self.position_flag_battery = QCheckBox("Include battery level")
        self.position_flag_satinview = QCheckBox("Include the number of satellites in view")
        self.position_flag_seq_nos = QCheckBox("Include a sequence number incremented per packet")
        self.position_flag_timestamp = QCheckBox("Include positional timestamp (from GPS solution)")
        self.position_flags = QLabel() # field that shows the number for the prior bit fields
        self.position_flags.setToolTip("The 'position_flags' adds up the bits from the position flags above. Try changing one of the values above to see this value change. This is the value that gets written to the device.")
        self.fixed_position = QCheckBox()
        self.location_share = QComboBox()
        self.location_share.setMinimumContentsLength(17)
        self.gps_operation = QComboBox()
        self.gps_operation.setMinimumContentsLength(17)
        self.gps_format = QComboBox()
        self.gps_format.setMinimumContentsLength(17)
        self.gps_accept_2d = QCheckBox()
        self.gps_max_dop = QLineEdit()
        self.gps_attempt_time = QLabel()

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Broadcast Interval"), self.position_broadcast_secs)
        form_layout.addRow(self.tr("Broadcast smart"), self.position_broadcast_smart)
        form_layout.addRow(self.tr("Position Flags"), self.position_flag_altitude)
        form_layout.addRow(self.tr("              "), self.position_flag_alt_msl)
        form_layout.addRow(self.tr("              "), self.position_flag_geo_sep)
        form_layout.addRow(self.tr("              "), self.position_flag_dop)
        form_layout.addRow(self.tr("              "), self.position_flag_hvdop)
        form_layout.addRow(self.tr("              "), self.position_flag_battery)
        form_layout.addRow(self.tr("              "), self.position_flag_satinview)
        form_layout.addRow(self.tr("              "), self.position_flag_seq_nos)
        form_layout.addRow(self.tr("              "), self.position_flag_timestamp)
        form_layout.addRow(self.tr("Position Flags Value (Calculated)"), self.position_flags)
        form_layout.addRow(self.tr("Use Fixed Position"), self.fixed_position)
        form_layout.addRow(self.tr("Location Sharing"), self.location_share)
        form_layout.addRow(self.tr("GPS Operation"), self.gps_operation)
        form_layout.addRow(self.tr("GPS Coordinate Format"), self.gps_format)
        form_layout.addRow(self.tr("GPS Accept 2D Fix"), self.gps_accept_2d)
        form_layout.addRow(self.tr("GPS Max DOP"), self.gps_max_dop)
        form_layout.addRow(self.tr("Last GPS Attempt"), self.gps_attempt_time)
        form_layout.addRow(self.tr(""), self.button_box)
        self.setLayout(form_layout)

        self.position_flag_altitude.stateChanged.connect(self.on_position_flag_change)
        self.position_flag_alt_msl.stateChanged.connect(self.on_position_flag_change)
        self.position_flag_geo_sep.stateChanged.connect(self.on_position_flag_change)
        self.position_flag_dop.stateChanged.connect(self.on_position_flag_change)
        self.position_flag_hvdop.stateChanged.connect(self.on_position_flag_change)
        self.position_flag_battery.stateChanged.connect(self.on_position_flag_change)
        self.position_flag_satinview.stateChanged.connect(self.on_position_flag_change)
        self.position_flag_seq_nos.stateChanged.connect(self.on_position_flag_change)
        self.position_flag_timestamp.stateChanged.connect(self.on_position_flag_change)


    # pylint: disable=unused-argument
    def on_position_flag_change(self, value):
        """When the select_firmware drop down value is changed."""
        tmp = 0
        if self.position_flag_altitude.isChecked():
            tmp += 1
        if self.position_flag_alt_msl.isChecked():
            tmp += 2
        if self.position_flag_geo_sep.isChecked():
            tmp += 4
        if self.position_flag_dop.isChecked():
            tmp += 8
        if self.position_flag_hvdop.isChecked():
            tmp += 16
        if self.position_flag_battery.isChecked():
            tmp += 32
        if self.position_flag_satinview.isChecked():
            tmp += 64
        if self.position_flag_seq_nos.isChecked():
            tmp += 128
        if self.position_flag_timestamp.isChecked():
            tmp += 256
        self.position_flags.setText(f'{tmp}')


    def set_position_flags(self, position_flags):
        """set the position flags when the form first opens - 'position_flags' value comes from device"""
        tmp = int(position_flags)
        if tmp >= 256:
            self.position_flag_timestamp.setChecked(True)
            tmp = tmp - 256
        if tmp >= 128:
            self.position_flag_seq_nos.setChecked(True)
            tmp = tmp - 128
        if tmp >= 64:
            self.position_flag_satinview.setChecked(True)
            tmp = tmp - 64
        if tmp >= 32:
            self.position_flag_battery.setChecked(True)
            tmp = tmp - 32
        if tmp >= 16:
            self.position_flag_hvdop.setChecked(True)
            tmp = tmp - 16
        if tmp >= 8:
            self.position_flag_dop.setChecked(True)
            tmp = tmp - 8
        if tmp >= 4:
            self.position_flag_geo_sep.setChecked(True)
            tmp = tmp - 4
        if tmp >= 2:
            self.position_flag_alt_msl.setChecked(True)
            tmp = tmp - 2
        if tmp >= 1:
            self.position_flag_altitude.setChecked(True)


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

                if self.prefs.position_broadcast_secs:
                    self.position_broadcast_secs.setText(f'{self.prefs.position_broadcast_secs}')
                else:
                    self.position_broadcast_secs.setText("0")

                print(f'self.prefs.position_broadcast_smart:{self.prefs.position_broadcast_smart}')
                if self.prefs.position_broadcast_smart:
                    self.position_broadcast_smart.setChecked(True)

                if self.prefs.position_flags:
                    self.position_flags.setText(f'{self.prefs.position_flags}')
                else:
                    self.position_flags.setText("0")
                self.set_position_flags(self.position_flags.text())

                if self.prefs.fixed_position:
                    self.fixed_position.setChecked(True)

                temp = 0
                if self.prefs.location_share:
                    temp = int(self.prefs.location_share)
                self.location_share.clear()
                desc = meshtastic.radioconfig_pb2.LocationSharing.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    self.location_share.addItem(k, v.number)
                    if v.number == temp:
                        self.location_share.setCurrentIndex(v.number)

                temp = 0
                if self.prefs.gps_operation:
                    temp = int(self.prefs.gps_operation)
                self.gps_operation.clear()
                desc = meshtastic.radioconfig_pb2.GpsOperation.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    self.gps_operation.addItem(k, v.number)
                    if v.number == temp:
                        self.gps_operation.setCurrentIndex(v.number)

                temp = 0
                if self.prefs.gps_format:
                    temp = int(self.prefs.gps_format)
                self.gps_format.clear()
                desc = meshtastic.radioconfig_pb2.GpsCoordinateFormat.DESCRIPTOR
                for k,v in desc.values_by_name.items():
                    self.gps_format.addItem(k, v.number)
                    if v.number == temp:
                        self.gps_format.setCurrentIndex(v.number)

                if self.prefs.gps_accept_2d:
                    self.gps_accept_2d.setChecked(True)

                if self.prefs.gps_max_dop:
                    self.gps_max_dop.setText(f'{self.prefs.gps_max_dop}')
                else:
                    self.gps_max_dop.setText("0")

                if self.prefs.gps_attempt_time:
                    self.gps_attempt_time.setText(f'{self.prefs.gps_attempt_time}')
                else:
                    self.gps_attempt_time.setText('')

        except Exception as e:
            print(f'Exception:{e}')


    def write_values(self):
        """Write values to device"""
        try:
            if self.interface:
                print("Writing preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'position_broadcast_secs', zero_if_blank(self.position_broadcast_secs.text()))
                setPref(prefs, 'position_broadcast_smart', f'{self.position_broadcast_smart.isChecked()}')
                setPref(prefs, 'position_flags', self.position_flags.text())
                setPref(prefs, 'fixed_position', f'{self.fixed_position.isChecked()}')
                setPref(prefs, 'location_share', f'{self.location_share.currentData()}')
                setPref(prefs, 'gps_operation', f'{self.gps_operation.currentData()}')
                setPref(prefs, 'gps_format', f'{self.gps_format.currentData()}')
                setPref(prefs, 'gps_accept_2d', f'{self.gps_accept_2d.isChecked()}')
                setPref(prefs, 'gps_max_dop', zero_if_blank(self.gps_max_dop.text()))
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
