"""class for the channel settings"""


from PySide6.QtWidgets import QTabWidget, QMainWindow

from meshtastic_flasher.channel_form import ChannelForm


class ChannelSettings(QMainWindow):
    """channel settings"""

    def __init__(self, parent=None):
        """constructor"""
        super(ChannelSettings, self).__init__()

        self.parent = parent
        self.port = None
        self.interface = None

        width = 800
        height = 600
        num_channels = 8
        self.setMinimumSize(width, height)
        self.setWindowTitle("Channel Settings")

        self.channel_forms = []
        for i in range(num_channels):
            self.channel_forms.append(ChannelForm(self, channel_index=i))

        self.tabs = QTabWidget()

        self.tabs.blockSignals(True) # just for not showing initial message
        self.tabs.currentChanged.connect(self.on_change_tabs)

        self.tabs.setTabPosition(QTabWidget.North)

        for i in range(num_channels):
            self.tabs.addTab(self.channel_forms[i], f"{i}")

        self.setCentralWidget(self.tabs)

        self.tabs.blockSignals(False) # now listen the currentChanged signal


    def on_change_tabs(self, i):
        """On change of each tab """
        print(f'on_change_tabs:{i}')
        self.channel_forms[i].run(port=self.port, interface=self.interface)


    def run(self, port=None, interface=None):
        """load the form"""
        print(f'in plugin settings run() port:{port}:')
        self.port = port
        self.interface = interface
        self.show()
        self.channel_forms[0].run(port=self.port, interface=self.interface)
