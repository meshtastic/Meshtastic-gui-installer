"""class for info form"""

from PySide6.QtWidgets import QDialog, QFormLayout, QPlainTextEdit


class InfoForm(QDialog):
    """info form"""

    def __init__(self, parent=None):
        """constructor"""
        super(InfoForm, self).__init__(parent)

        self.parent = parent
        self.main = parent.main

        width = 800
        height = 900
        self.setMinimumSize(width, height)
        self.setWindowTitle(self.main.text('info'))

        # Create widgets
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.text)
        self.setLayout(form_layout)

    def write(self, data):
        """Write the output to text widget"""
        if data:
            self.text.appendPlainText(data)
