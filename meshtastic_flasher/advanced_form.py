"""class for the Advanced options form"""


from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox, QFormLayout


class AdvancedForm(QDialog):
    """Advanced options form"""

    def __init__(self, parent=None):
        """constructor"""
        super(AdvancedForm, self).__init__(parent)

        width = 240
        height = 120
        self.setMinimumSize(width, height)
        self.setWindowTitle("Advanced Options")

        # Create widgets
        self.update_only_cb = QCheckBox()
        self.update_only_cb.setToolTip("If enabled, the device will be updated (not completely erased).")
        self.rak_bootloader_cb = QCheckBox()
        self.rak_bootloader_cb.setToolTip("If enabled, the NRF52 bootloader on RAK devices will be checked and updated in DETECT step.")

        self.ok_button = QPushButton("OK")

        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("&Update only"), self.update_only_cb)
        form_layout.addRow(self.tr("&RAK Bootloader Update"), self.rak_bootloader_cb)
        form_layout.addRow(self.tr(""), self.ok_button)
        self.setLayout(form_layout)

        self.ok_button.clicked.connect(self.close_advanced_options)

    def close_advanced_options(self):
        """Close the advanced options form"""
        print('OK button was clicked in advanced options')
        self.close()
