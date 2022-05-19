"""class to show images of detected radios and images to let user pick which one they have"""

from PySide6 import QtCore
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QRadioButton, QGridLayout, QLabel, QDialog

import meshtastic_flasher.util

class RadioPickerForm(QDialog):
    """radio picker form"""

    def __init__(self, parent=None):
        """constructor"""
        super(RadioPickerForm, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.scale_x = 256
        self.scale_y = 256

        self.radios = None

        self.heltec_v1 = None
        self.heltec_v1_image = None
        self.heltec_v1_pixmap = None
        self.heltec_v20 = None
        self.heltec_v20_image = None
        self.heltec_v20_pixmap = None
        self.heltec_v21 = None
        self.heltec_v21_image = None
        self.heltec_v21_pixmap = None
        self.tbeam_v07 = None
        self.tbeam_v07_image = None
        self.tbeam_v07_pixmap = None
        self.tbeam_v11 = None
        self.tbeam_v11_image = None
        self.tbeam_v11_pixmap = None
        self.tlora_v1 = None
        self.tlora_v1_image = None
        self.tlora_v1_pixmap = None
        self.tlora_v13 = None
        self.tlora_v13_image = None
        self.tlora_v13_pixmap = None
        self.tlora_v2 = None
        self.tlora_v2_image = None
        self.tlora_v2_pixmap = None
        self.tlora_v2116 = None
        self.tlora_v2116_image = None
        self.tlora_v2116_pixmap = None
        self.meshtastic_diy = None
        self.meshtastic_diy_image = None
        self.meshtastic_diy_pixmap = None
        self.rak11200 = None
        self.rak11200_image = None
        self.rak11200_pixmap = None
        self.rak4631_5005 = None
        self.rak4631_5005_image = None
        self.rak4631_5005_pixmap = None
        self.rak4631_5005_epaper = None
        self.rak4631_5005_epaper_image = None
        self.rak4631_5005_epaper_pixmap = None
        self.rak4631_19003 = None
        self.rak4631_19003_image = None
        self.rak4631_19003_pixmap = None
        self.techo = None
        self.techo_image = None
        self.techo_pixmap = None
        self.nano_g1 = None
        self.nano_g1_image = None
        self.nano_g1_pixmap = None


    def populate_radios(self):
        """Populate the list of radios with images"""
        grid_row = 0

        if "heltec-v1" in self.radios:
            self.heltec_v1 = QRadioButton("Heltec v1")
            self.heltec_v1.radio = "heltec-v1"
            self.heltec_v1.toggled.connect(self.onClicked)
            self.layout.addWidget(self.heltec_v1, grid_row, 0)

            self.heltec_v1_image = QLabel(self)
            self.heltec_v1_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/heltec-v1.png'))
            self.heltec_v1_image.setPixmap(self.heltec_v1_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.heltec_v1_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.heltec_v1_image, grid_row, 1)
            grid_row = grid_row + 1

        if "heltec-v2.0" in self.radios:
            self.heltec_v20 = QRadioButton("Heltec v2.0")
            self.heltec_v20.radio = "heltec-v2.0"
            self.heltec_v20.toggled.connect(self.onClicked)
            self.layout.addWidget(self.heltec_v20, grid_row, 0)

            self.heltec_v20_image = QLabel(self)
            self.heltec_v20_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/heltec-v2.0.png'))
            self.heltec_v20_image.setPixmap(self.heltec_v20_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.heltec_v20_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.heltec_v20_image, grid_row, 1)
            grid_row = grid_row + 1

        if "heltec-v2.1" in self.radios:
            self.heltec_v21 = QRadioButton("Heltec v2.1")
            self.heltec_v21.radio = "heltec-v2.1"
            self.heltec_v21.toggled.connect(self.onClicked)
            self.layout.addWidget(self.heltec_v21, grid_row, 0)

            self.heltec_v21_image = QLabel(self)
            self.heltec_v21_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/heltec-v2.1.jpg'))
            self.heltec_v21_image.setPixmap(self.heltec_v21_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.heltec_v21_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.heltec_v21_image, grid_row, 1)
            grid_row = grid_row + 1

        if "tbeam0.7" in self.radios:
            self.tbeam_v07 = QRadioButton("T-Beam v0.7")
            self.tbeam_v07.radio = "tbeam0.7"
            self.tbeam_v07.toggled.connect(self.onClicked)
            self.layout.addWidget(self.tbeam_v07, grid_row, 0)

            self.tbeam_v07_image = QLabel(self)
            self.tbeam_v07_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/t-beam-v0.7.png'))
            self.tbeam_v07_image.setPixmap(self.tbeam_v07_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.tbeam_v07_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.tbeam_v07_image, grid_row, 1)
            grid_row = grid_row + 1

        if "tbeam" in self.radios:
            self.tbeam_v11 = QRadioButton("T-Beam")
            self.tbeam_v11.radio = "tbeam"
            self.tbeam_v11.toggled.connect(self.onClicked)
            self.layout.addWidget(self.tbeam_v11, grid_row, 0)

            self.tbeam_v11_image = QLabel(self)
            self.tbeam_v11_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/t-beam.png'))
            self.tbeam_v11_image.setPixmap(self.tbeam_v11_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.tbeam_v11_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.tbeam_v11_image, grid_row, 1)
            grid_row = grid_row + 1

        if "tlora-v1" in self.radios:
            self.tlora_v1 = QRadioButton("T-Lora v1")
            self.tlora_v1.radio = "tlora-v1"
            self.tlora_v1.toggled.connect(self.onClicked)
            self.layout.addWidget(self.tlora_v1, grid_row, 0)

            self.tlora_v1_image = QLabel(self)
            self.tlora_v1_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/tlora-v1.png'))
            self.tlora_v1_image.setPixmap(self.tlora_v1_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.tlora_v1_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.tlora_v1_image, grid_row, 1)
            grid_row = grid_row + 1

        if "tlora-v1_3" in self.radios:
            self.tlora_v13 = QRadioButton("T-Lora v1_3")
            self.tlora_v13.radio = "tlora-v1_3"
            self.tlora_v13.toggled.connect(self.onClicked)
            self.layout.addWidget(self.tlora_v13, grid_row, 0)

            self.tlora_v13_image = QLabel(self)
            self.tlora_v13_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/tlora-v1_3.png'))
            self.tlora_v13_image.setPixmap(self.tlora_v13_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.tlora_v13_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.tlora_v13_image, grid_row, 1)
            grid_row = grid_row + 1

        if "tlora-v2" in self.radios:
            self.tlora_v2 = QRadioButton("T-Lora v2")
            self.tlora_v2.radio = "tlora-v2"
            self.tlora_v2.toggled.connect(self.onClicked)
            self.layout.addWidget(self.tlora_v2, grid_row, 0)

            self.tlora_v2_image = QLabel(self)
            self.tlora_v2_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/tlora-v2.png'))
            self.tlora_v2_image.setPixmap(self.tlora_v2_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.tlora_v2_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.tlora_v2_image, grid_row, 1)
            grid_row = grid_row + 1

        if "tlora-v2-1-1.6" in self.radios:
            self.tlora_v2116 = QRadioButton("T-Lora v2.1-1.6")
            self.tlora_v2116.radio = "tlora-v2-1-1.6"
            self.tlora_v2116.toggled.connect(self.onClicked)
            self.layout.addWidget(self.tlora_v2116, grid_row, 0)

            self.tlora_v2116_image = QLabel(self)
            self.tlora_v2116_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/tlora-v2.1-1.6.png'))
            self.tlora_v2116_image.setPixmap(self.tlora_v2116_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.tlora_v2116_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.tlora_v2116_image, grid_row, 1)
            grid_row = grid_row + 1

        if "meshtastic-diy-v1" in self.radios:
            self.meshtastic_diy = QRadioButton("Meshtastic DIY")
            self.meshtastic_diy.radio = "meshtastic-diy-v1"
            self.meshtastic_diy.toggled.connect(self.onClicked)
            self.layout.addWidget(self.meshtastic_diy, grid_row, 0)

            self.meshtastic_diy_image = QLabel(self)
            self.meshtastic_diy_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/meshtastic-diy.jpg'))
            self.meshtastic_diy_image.setPixmap(self.meshtastic_diy_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.meshtastic_diy_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.meshtastic_diy_image, grid_row, 1)
            grid_row = grid_row + 1

        if "rak11200" in self.radios:
            self.rak11200 = QRadioButton("RAK 11200")
            self.rak11200.radio = "rak11200"
            self.rak11200.toggled.connect(self.onClicked)
            self.layout.addWidget(self.rak11200, grid_row, 0)

            self.rak11200_image = QLabel(self)
            self.rak11200_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/rak11200.jpg'))
            self.rak11200_image.setPixmap(self.rak11200_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.rak11200_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.rak11200_image, grid_row, 1)
            grid_row = grid_row + 1

        if "rak4631_5005" in self.radios:
            self.rak4631_5005 = QRadioButton("RAK 4631/5005")
            self.rak4631_5005.radio = "rak4631_5005"
            self.rak4631_5005.toggled.connect(self.onClicked)
            self.layout.addWidget(self.rak4631_5005, grid_row, 0)

            self.rak4631_5005_image = QLabel(self)
            self.rak4631_5005_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/rak4631_5005.png'))
            self.rak4631_5005_image.setPixmap(self.rak4631_5005_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.rak4631_5005_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.rak4631_5005_image, grid_row, 1)
            grid_row = grid_row + 1

        if "rak4631_5005_epaper" in self.radios:
            self.rak4631_5005_epaper = QRadioButton("RAK 4631/5005/14000 epaper")
            self.rak4631_5005_epaper.radio = "rak4631_5005_epaper"
            self.rak4631_5005_epaper.toggled.connect(self.onClicked)
            self.layout.addWidget(self.rak4631_5005_epaper, grid_row, 0)

            self.rak4631_5005_epaper_image = QLabel(self)
            self.rak4631_5005_epaper_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/rak4631_5005_epaper.jpg'))
            self.rak4631_5005_epaper_image.setPixmap(self.rak4631_5005_epaper_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.rak4631_5005_epaper_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.rak4631_5005_epaper_image, grid_row, 1)
            grid_row = grid_row + 1

        if "rak4631_19003" in self.radios:
            self.rak4631_19003 = QRadioButton("RAK 4631/19003")
            self.rak4631_19003.radio = "rak4631_19003"
            self.rak4631_19003.toggled.connect(self.onClicked)
            self.layout.addWidget(self.rak4631_19003, grid_row, 0)

            self.rak4631_19003_image = QLabel(self)
            self.rak4631_19003_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/rak4631_19003.png'))
            self.rak4631_19003_image.setPixmap(self.rak4631_19003_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.rak4631_19003_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.rak4631_19003_image, grid_row, 1)
            grid_row = grid_row + 1

        if "t-echo" in self.radios:
            self.techo = QRadioButton("T-Echo")
            self.techo.radio = "t-echo"
            self.techo.toggled.connect(self.onClicked)
            self.layout.addWidget(self.techo, grid_row, 0)

            self.techo_image = QLabel(self)
            self.techo_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/t-echo.jpeg'))
            self.techo_image.setPixmap(self.techo_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.techo_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.techo_image, grid_row, 1)
            grid_row = grid_row + 1

        if "nano-g1" in self.radios:
            self.nano_g1 = QRadioButton("Nano G1")
            self.nano_g1.radio = "nano-g1"
            self.nano_g1.toggled.connect(self.onClicked)
            self.layout.addWidget(self.nano_g1, grid_row, 0)

            self.nano_g1_image = QLabel(self)
            self.nano_g1_pixmap = QPixmap(meshtastic_flasher.util.get_path('radios/nano-g1.jpeg'))
            self.nano_g1_image.setPixmap(self.nano_g1_pixmap.scaled(self.scale_x, self.scale_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.nano_g1_image.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.nano_g1_image, grid_row, 1)
            grid_row = grid_row + 1


    def onClicked(self):
        """When the user clicks a value."""
        radioButton = self.sender()
        if radioButton.isChecked():
            print(f"User picked radio {radioButton.radio}")
            self.parent.device_from_picker = radioButton.radio
            self.close()


    def run(self, list_of_radios):
        """Show the firm with only the radios in the list_of_radios"""
        self.radios = list_of_radios
        self.populate_radios()
        self.exec()
