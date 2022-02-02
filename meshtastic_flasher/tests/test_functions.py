import re

from pytestqt.qt_compat import qt_api

from PySide6.QtWidgets import QMessageBox

from meshtastic_flasher.installer import Form, get_path, populate_tag_in_firmware_dropdown

def test_get_path():
    assert get_path("foo.file").endswith("foo.file")
    assert len(get_path("foo.file")) > 10

def test_populate_tag_in_firmware_dropdown():
    assert populate_tag_in_firmware_dropdown("v1.2.52.foo")
    assert not populate_tag_in_firmware_dropdown("v1.2.51.foo")


