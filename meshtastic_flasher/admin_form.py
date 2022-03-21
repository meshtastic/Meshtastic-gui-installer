"""class for the admin settings"""

from PySide6.QtWidgets import QDialog, QFormLayout, QPushButton, QMessageBox

from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref


class AdminForm(QDialog):
    """admin settings form"""

    def __init__(self, parent=None):
        """constructor"""
        super(AdminForm, self).__init__(parent)

        self.parent = parent
        self.main = parent.main

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle(self.main.text('admin_settings'))

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets
        self.factory_reset_button = QPushButton(self.main.text('factory_reset'))
        self.factory_reset_button.clicked.connect(self.factory_reset)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow("", self.factory_reset_button)
        self.setLayout(form_layout)


    def run(self, port=None, interface=None):
        """load the form"""
        self.port = port
        self.interface = interface
        if self.port:
            print(f'using port:{self.port}')
            self.show()


    def factory_reset(self):
        """Do a factory reset."""
        print('factory reset button clicked')
        reply = QMessageBox.question(self, self.main.text('flash'), self.main.text('confirm_reset_device'), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("User confirmed they want to do a factory reset")
            if self.interface:
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'factory_reset', 'true')
                self.interface.getNode(BROADCAST_ADDR).writeConfig()
                self.interface.getNode(BROADCAST_ADDR).reboot()
                QMessageBox.information(self, self.main.text('info'), self.main.text('device_was_reset'))
            self.parent.my_close()
        else:
            print("User does not want to do a factory reset")
