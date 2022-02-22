"""class for the plugin settings"""


from PySide6.QtWidgets import QTabWidget, QMainWindow

from meshtastic_flasher.plugins_range_test_form import RangeTestForm
from meshtastic_flasher.plugins_external_notifications_form import ExternalNotificationsForm
from meshtastic_flasher.plugins_environmental_measurement_form import EnvironmentalMeasurementForm
from meshtastic_flasher.plugins_serial_form import SerialForm
from meshtastic_flasher.plugins_rotary_encoder_form import RotaryEncoderForm
from meshtastic_flasher.plugins_canned_message_form import CannedMessageForm
#from meshtastic_flasher.plugins_store_and_forward_form import StoreAndForwardForm


class PluginSettings(QMainWindow):
    """plugin settings"""

    def __init__(self, parent=None):
        """constructor"""
        super(PluginSettings, self).__init__()

        self.parent = parent
        self.port = None
        self.interface = None

        width = 800
        height = 600
        self.setMinimumSize(width, height)
        self.setWindowTitle("Plugin Settings")

        self.range_test_form = RangeTestForm(self)
        self.external_notifications_form = ExternalNotificationsForm(self)
        self.envrionmental_measurement_form = EnvironmentalMeasurementForm(self)
        self.serial_form = SerialForm(self)
        self.rotary_encoder_form = RotaryEncoderForm(self)
        self.canned_message_form = CannedMessageForm(self)
        #self.store_and_forward_form = StoreAndForwardForm(self)

        self.tabs = QTabWidget()

        self.tabs.blockSignals(True) # just for not showing initial message
        self.tabs.currentChanged.connect(self.on_change_tabs)

        self.tabs.setTabPosition(QTabWidget.North)

        self.tabs.addTab(self.range_test_form, "Range")
        self.tabs.addTab(self.external_notifications_form, "Notifications")
        self.tabs.addTab(self.envrionmental_measurement_form, "Environment")
        self.tabs.addTab(self.serial_form, "Serial")
        self.tabs.addTab(self.rotary_encoder_form, "Rotary")
        self.tabs.addTab(self.canned_message_form, "Canned")
        #self.tabs.addTab(self.store_and_forward_form, "Store/Forward")

        self.setCentralWidget(self.tabs)

        self.tabs.blockSignals(False) # now listen the currentChanged signal


    def on_change_tabs(self, i):
        """On change of each tab """
        print(f'on_change_tabs:{i}')
        if i == 0:
            print('range_test_form.run()')
            self.range_test_form.run(port=self.port, interface=self.interface)
        elif i == 1:
            print('external_notifications_form.run()')
            self.external_notifications_form.run(port=self.port, interface=self.interface)
        elif i == 2:
            print('envrionmental_measurement_form.run()')
            self.envrionmental_measurement_form.run(port=self.port, interface=self.interface)
        elif i == 3:
            print('serial_form.run()')
            self.serial_form.run(port=self.port, interface=self.interface)
        elif i == 4:
            print('rotary_encoder_form.run()')
            self.rotary_encoder_form.run(port=self.port, interface=self.interface)
        elif i == 5:
            print('canned_message_form.run()')
            self.canned_message_form.run(port=self.port, interface=self.interface)
        #elif i == 6:
            #print('store_and_forward_form.run()')
            #self.store_and_forward_form.run(port=self.port, interface=self.interface)


    def run(self, port=None, interface=None):
        """load the form"""
        print(f'in plugin settings run() port:{port}:')
        self.port = port
        self.interface = interface
        self.show()
        self.range_test_form.run(port=self.port, interface=self.interface)
