"""Test hotkeys
"""
import re

from unittest.mock import patch

from PySide6.QtWidgets import QMessageBox

from meshtastic.supported_device import SupportedDevice

from meshtastic_flasher.form import Form

@patch('meshtastic_flasher.util.check_if_newer_version')
@patch('meshtastic_flasher.form.Form.get_versions_from_disk')
def test_hotkey_a(fake_versions, fake_check_newer, qtbot, capsys):
    """Test hot key 'a' """
    widget = Form()
    qtbot.addWidget(widget)
    qtbot.keyPress(widget, "a")
    widget.advanced_form.close_advanced_options()
    out, err = capsys.readouterr()
    assert re.search(r'A was pressed', out, re.MULTILINE)
    assert re.search(r'OK button was clicked in advanced options', out, re.MULTILINE)
    assert err == ''
    fake_versions.assert_called()
    fake_check_newer.assert_called()


@patch('meshtastic_flasher.util.check_if_newer_version')
@patch('meshtastic_flasher.form.Form.confirm_check_using_meshtastic', return_value=True)
@patch('meshtastic_flasher.form.Form.get_versions_from_disk')
@patch('meshtastic_flasher.form.Form.version_and_device_from_info')
@patch('meshtastic_flasher.form.Form.detect_ports_using_find_ports')
@patch('meshtastic_flasher.form.Form.detect_ports_on_supported_devices', return_value=['/dev/foo'])
@patch('meshtastic_flasher.form.Form.detect_devices')
@patch('meshtastic_flasher.form.Form.warn_linux_users_if_not_in_dialout_group', return_value=False)
def test_hotkey_d(fake_warn, fake_detect_devices, fake_detect_ports_on_supported_devices,
                  fake_detect_ports_using_find_ports, fake_version_and_device_from_info, fake_versions,
                  fake_confirm_meshtastic_check, fake_check_newer, qtbot, capsys):
    """Test hot key 'd' """
    widget = Form()
    qtbot.addWidget(widget)

    widget.select_device.addItem("bar")
    widget.firmware_version="1.0.3"

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
    fake_version_and_device_from_info.assert_called()
    fake_versions.assert_called()
    fake_confirm_meshtastic_check.assert_called()
    fake_check_newer.assert_called()


@patch('meshtastic_flasher.util.check_if_newer_version')
@patch('meshtastic_flasher.form.Form.get_versions_from_disk')
@patch('meshtastic_flasher.form.Form.detect_nrf_stuff')
@patch('meshtastic_flasher.form.Form.detect_ports_on_supported_devices')
@patch('meshtastic_flasher.form.Form.detect_devices')
@patch('meshtastic_flasher.form.Form.warn_linux_users_if_not_in_dialout_group')
def test_hotkey_d_with_nrf(fake_warn, fake_detect_devices, fake_detect_ports_on_supported_devices,
                           fake_detect_nrf_stuff, fake_versions, fake_check_newer, qtbot, capsys):
    """Test hot key 'd' """
    widget = Form()
    qtbot.addWidget(widget)

    widget.select_device.addItem("bar")
    widget.firmware_version="1.0.3"

    assert not widget.select_flash.isEnabled()

    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]
    fake_detect_devices.return_value = fake_supported_devices

    qtbot.keyPress(widget, "d")

    out, err = capsys.readouterr()
    assert re.search(r'D was pressed', out, re.MULTILINE)
    assert re.search(r'start of detect', out, re.MULTILINE)
    assert re.search(r'end of detect', out, re.MULTILINE)
    assert err == ''
    fake_warn.assert_called()
    fake_detect_devices.assert_called()
    fake_detect_ports_on_supported_devices.assert_called()
    fake_detect_nrf_stuff.assert_called()
    fake_versions.assert_called()
    fake_check_newer.assert_called()


@patch('meshtastic_flasher.util.check_if_newer_version')
@patch('meshtastic_flasher.form.Form.get_versions_from_disk')
@patch('meshtastic_flasher.util.unzip_if_necessary')
@patch('meshtastic_flasher.util.download_if_zip_does_not_exist')
@patch('meshtastic_flasher.util.get_tags_from_github', return_value=['v1.2.53aa', 'v1.2.53fff', 'v1.2.51f'])
def test_hotkey_g(fake_get_tags, fake_download, fake_unzip, fake_versions, fake_check_newer, qtbot, capsys):
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
    fake_versions.assert_called()
    fake_check_newer.assert_called()


@patch('meshtastic_flasher.util.check_if_newer_version')
@patch('meshtastic_flasher.form.Form.get_versions_from_disk')
def test_hotkey_h(fake_versions, fake_check_newer, qtbot, monkeypatch, capsys):
    """Test hot key 'h' """
    widget = Form()
    qtbot.addWidget(widget)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
    qtbot.keyPress(widget, "h")
    out, err = capsys.readouterr()
    assert re.search(r'hotkeys', out, re.MULTILINE)
    assert re.search(r'H was pressed', out, re.MULTILINE)
    assert err == ''
    fake_versions.assert_called()
    fake_check_newer.assert_called()


@patch('meshtastic_flasher.util.check_if_newer_version')
@patch('meshtastic_flasher.form.Form.get_versions_from_disk')
def test_hotkey_q(fake_versions, fake_check_newer, qtbot, capsys):
    """Test hot key 'q' """
    widget = Form()
    qtbot.addWidget(widget)
    qtbot.keyPress(widget, "q")
    out, err = capsys.readouterr()
    assert re.search(r'Q was pressed', out, re.MULTILINE)
    assert err == ''
    fake_versions.assert_called()
    fake_check_newer.assert_called()


# TODO: fix
#@patch('meshtastic_flasher.util.check_if_newer_version')
#@patch('meshtastic_flasher.form.Form.get_versions_from_disk')
#def test_hotkey_t(fake_versions, fake_check_newer, qtbot, monkeypatch, capsys):
#    """Test hot key 't' """
#    widget = Form()
#    qtbot.addWidget(widget)
#    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
#    qtbot.keyPress(widget, "t")
#    out, err = capsys.readouterr()
#    assert re.search(r'tips', out, re.MULTILINE)
#    assert re.search(r'T was pressed', out, re.MULTILINE)
#    assert err == ''
#    fake_versions.assert_called()
#    fake_check_newer.assert_called()
