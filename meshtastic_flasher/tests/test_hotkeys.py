"""Test hotkeys
"""
import re

from unittest.mock import patch

from PySide6.QtWidgets import QMessageBox
from meshtastic.supported_device import SupportedDevice

from meshtastic_flasher.installer import Form

def test_hotkey_a(qtbot, capsys):
    """Test hot key 'a' """
    widget = Form()
    qtbot.addWidget(widget)
    qtbot.keyPress(widget, "a")
    widget.advanced_form.close_advanced_options()
    out, err = capsys.readouterr()
    assert re.search(r'A was pressed', out, re.MULTILINE)
    assert re.search(r'OK button was clicked in advanced options', out, re.MULTILINE)
    assert err == ''


@patch('meshtastic_flasher.installer.Form.version_and_device_from_info')
@patch('meshtastic_flasher.installer.Form.detect_nrf_stuff')
@patch('meshtastic_flasher.installer.Form.all_devices')
@patch('meshtastic_flasher.installer.Form.detect_ports_using_find_ports')
@patch('meshtastic_flasher.installer.Form.detect_ports_on_supported_devices', return_value=['/dev/foo'])
@patch('meshtastic_flasher.installer.Form.detect_devices')
@patch('meshtastic_flasher.installer.Form.warn_linux_users_if_not_in_dialout_group', return_value=False)
def test_hotkey_d(fake_warn, fake_detect_devices, fake_detect_ports_on_supported_devices,
                  fake_detect_ports_using_find_ports, fake_all_devices, fake_nrf_stuff,
                  fake_version_and_device_from_info, qtbot, capsys):
    """Test hot key 'd' """
    widget = Form()
    qtbot.addWidget(widget)

    #widget.select_port.addItem("foo")
    widget.select_device.addItem("bar")
    widget.firmware_version="1.0.3"

    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]
    fake_detect_devices.return_value = fake_supported_devices

    assert not widget.select_flash.isEnabled()

    qtbot.keyPress(widget, "d")

    out, err = capsys.readouterr()
    assert re.search(r'D was pressed', out, re.MULTILINE)
    assert re.search(r'start of detect', out, re.MULTILINE)
    assert re.search(r'end of detect', out, re.MULTILINE)
    assert err == ''
    fake_warn.assert_called()
    fake_detect_devices.assert_called()
    fake_detect_ports_on_supported_devices.assert_called()
    fake_detect_ports_using_find_ports.assert_called()
    fake_all_devices.assert_called()
    fake_nrf_stuff.assert_called()
    fake_version_and_device_from_info.assert_called()


@patch('meshtastic_flasher.installer.unzip_if_necessary')
@patch('meshtastic_flasher.installer.download_if_zip_does_not_exist')
@patch('meshtastic_flasher.installer.get_tags_from_github', return_value=['v1.2.53aa', 'v1.2.53fff', 'v1.2.51f'])
def test_hotkey_g(fake_get_tags, fake_download, fake_unzip, qtbot, capsys):
    """Test hot key 'g' """
    widget = Form()
    qtbot.addWidget(widget)
    qtbot.keyPress(widget, "g")
    out, err = capsys.readouterr()
    assert re.search(r'G was pressed', out, re.MULTILINE)
    assert err == ''
    fake_get_tags.assert_called()
    fake_download.assert_called()
    fake_unzip.assert_called()


def test_hotkey_h(qtbot, monkeypatch, capsys):
    """Test hot key 'h' """
    widget = Form()
    qtbot.addWidget(widget)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
    qtbot.keyPress(widget, "h")
    out, err = capsys.readouterr()
    assert re.search(r'hotkeys', out, re.MULTILINE)
    assert re.search(r'H was pressed', out, re.MULTILINE)
    assert err == ''


def test_hotkey_q(qtbot, capsys):
    """Test hot key 'q' """
    widget = Form()
    qtbot.addWidget(widget)
    qtbot.keyPress(widget, "q")
    out, err = capsys.readouterr()
    assert re.search(r'Q was pressed', out, re.MULTILINE)
    assert err == ''
