"""tests for Form"""
import re

#import functools

#from pytestqt.qt_compat import qt_api
#from PySide6.QtWidgets import QMessageBox

from meshtastic_flasher.installer import Form

#def rsetattr(obj, attr, val):
#    pre, _, post = attr.rpartition('.')
#    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def test_Form_title(qtbot):
    """Test for title var in Form"""
    widget = Form()
    qtbot.addWidget(widget)
    assert re.search(r'Meshtastic Flasher v1.0.', widget.windowTitle(), re.MULTILINE)

def test_buttons_and_combo_boxes(qtbot):
    """Test initial state of buttons and combo boxes in Form"""
    widget = Form()
    qtbot.addWidget(widget)

    # ensure buttons are present and enabled
    assert widget.get_versions_button.isEnabled()
    assert widget.select_detect.isEnabled()

    # ensure these are not enabled
    assert not widget.select_firmware_version.isEnabled()
    assert not widget.select_port.isEnabled()
    assert not widget.select_device.isEnabled()
    assert not widget.select_flash.isEnabled()


def test_get_versions_from_github():
    """Test get_versions_from_github()"""
    #exp_versions = ['v1.2.53.19c1f9f', 'v1.2.52.b63802c', 'v1.2.51.f9ff06b',
                    #'v1.2.50.41dcfdd', 'v1.2.49.5354c49', 'v1.2.48.371335e']
