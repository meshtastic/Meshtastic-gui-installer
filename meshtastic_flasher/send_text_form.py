"""class for the send text form"""

import sys

from PySide6.QtWidgets import QDialog, QFormLayout, QDialogButtonBox, QLineEdit, QMessageBox

from meshtastic.__main__ import main


class SendTextForm(QDialog):
    """send text form"""

    def __init__(self, parent=None):
        """constructor"""
        super(SendTextForm, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Send Text")

        self.prefs = None

        # Create widgets
        self.message = QLineEdit()
        self.message.setToolTip('The message to be sent.')

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok)
        self.button_box.rejected.connect(self.rejected)
        self.button_box.accepted.connect(self.send_message)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow("Message", self.message)
        form_layout.addRow(self.tr(""), self.button_box)
        self.setLayout(form_layout)


    def run(self):
        """load the form"""
        self.show()


    def send_message(self):
        """Send the message"""
        print(f'Send {self.message.text()}')

        if self.message.text() == '':
            QMessageBox.information(self, "Info", "Please supply a message to send.")
        else:
            old_sys_argv = sys.argv
            sys.argv = ['', '--sendtext', f'{self.message.text()}']
            try:
                main()
            except SystemExit:
                pass
            sys.argv = old_sys_argv
            QMessageBox.information(self, "Info", "Message sent")
            self.close()


    def rejected(self):
        """Close this form"""
        self.close()
