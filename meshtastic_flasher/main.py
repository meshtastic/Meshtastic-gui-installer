#!/usr/bin/env python3
""" installer for Meshtastic firmware (aka "Meshtastic flasher")
"""

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

import meshtastic_flasher.form
from meshtastic_flasher.util import get_path

def main():
    """Main loop"""

    # Create the Qt Application
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_path(meshtastic_flasher.form.MESHTASTIC_LOGO_FILENAME)))
    app.setApplicationName("Meshtastic Flasher")
    apply_stylesheet(app, theme=get_path('meshtastic_theme.xml'))

    # Create and show the form
    form = meshtastic_flasher.form.Form()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
