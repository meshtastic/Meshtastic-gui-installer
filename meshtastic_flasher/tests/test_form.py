"""tests for Form"""
import re

from unittest.mock import patch

from pytestqt.qt_compat import qt_api
from PySide6.QtWidgets import QMessageBox

from meshtastic_flasher.installer import Form


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


@patch('webbrowser.open')
def test_logo_clicked(fake_open, qtbot, capsys):
    """Test logo clicked in Form"""
    widget = Form()
    qtbot.addWidget(widget)
    qtbot.mouseClick(widget.logo, qt_api.QtCore.Qt.MouseButton.LeftButton)
    out, err = capsys.readouterr()
    assert re.search(r'The logo was clicked', out, re.MULTILINE)
    assert err == ''
    fake_open.assert_called()


@patch('meshtastic_flasher.installer.Form.flash_esp32_full_step4')
@patch('meshtastic_flasher.installer.Form.flash_esp32_full_step3')
@patch('meshtastic_flasher.installer.Form.flash_esp32_full_step2')
@patch('meshtastic_flasher.installer.Form.flash_esp32_full_step1')
@patch('meshtastic_flasher.installer.Form.confirm_flash_question', return_value=True)
def test_flash_esp32_full_clicked_user_said_yes(fake_confirm, fake1, fake2, fake3, fake4, monkeypatch, qtbot, capsys):
    """Test clicked Flash in Form"""
    widget = Form()
    qtbot.addWidget(widget)

    # do some setup
    assert widget.select_port.count() == 0
    widget.select_port.addItem('fake1')
    assert widget.select_port.count() == 1

    assert widget.select_device.count() == 0
    widget.select_device.addItem('fake2')
    assert widget.select_device.count() == 1

    widget.select_flash.setEnabled(True)

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    qtbot.mouseClick(widget.select_flash, qt_api.QtCore.Qt.MouseButton.LeftButton)
    out, err = capsys.readouterr()
    assert re.search(r'Flash was clicked', out, re.MULTILINE)
    assert re.search(r'update only is not checked', out, re.MULTILINE)
    assert re.search(r'esp32 full complete', out, re.MULTILINE)
    assert err == ''
    fake_confirm.assert_called()
    fake1.assert_called()
    fake2.assert_called()
    fake3.assert_called()
    fake4.assert_called()


@patch('meshtastic_flasher.installer.Form.flash_esp32_update_only_step2')
@patch('meshtastic_flasher.installer.Form.flash_esp32_update_only_step1')
@patch('meshtastic_flasher.installer.Form.confirm_flash_question', return_value=True)
def test_flash_esp32_update_only_clicked_user_said_yes(fake_confirm, fake1, fake2, monkeypatch, qtbot, capsys):
    """Test clicked Flash in Form"""
    widget = Form()
    qtbot.addWidget(widget)

    # do some setup
    assert widget.select_port.count() == 0
    widget.select_port.addItem('fake1')
    assert widget.select_port.count() == 1

    assert widget.select_device.count() == 0
    widget.select_device.addItem('fake2')
    assert widget.select_device.count() == 1

    widget.advanced_form.update_only_cb.setChecked(True)
    widget.select_flash.setEnabled(True)

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    qtbot.mouseClick(widget.select_flash, qt_api.QtCore.Qt.MouseButton.LeftButton)
    out, err = capsys.readouterr()
    assert re.search(r'Flash was clicked', out, re.MULTILINE)
    assert re.search(r'update only is checked', out, re.MULTILINE)
    assert re.search(r'esp32 update_only complete', out, re.MULTILINE)
    assert err == ''
    fake_confirm.assert_called()
    fake1.assert_called()
    fake2.assert_called()


@patch('meshtastic_flasher.installer.Form.flash_nrf52')
@patch('meshtastic_flasher.installer.Form.confirm_flash_question', return_value=True)
def test_flash_nrf_clicked_user_said_yes(fake_confirm, fake1, monkeypatch, qtbot, capsys):
    """Test clicked Flash in Form"""
    widget = Form()
    qtbot.addWidget(widget)

    # do some setup
    assert widget.select_port.count() == 0
    widget.select_port.addItem('fake1')
    assert widget.select_port.count() == 1

    assert widget.select_device.count() == 0
    widget.select_device.addItem('fake2')
    assert widget.select_device.count() == 1

    widget.select_flash.setEnabled(True)
    widget.nrf = True

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    qtbot.mouseClick(widget.select_flash, qt_api.QtCore.Qt.MouseButton.LeftButton)
    out, err = capsys.readouterr()
    assert re.search(r'Flash was clicked', out, re.MULTILINE)
    assert re.search(r'nrf52 file was copied', out, re.MULTILINE)
    assert err == ''
    fake_confirm.assert_called()
    fake1.assert_called()


# Not sure why the patch is not working.
#@patch('meshtastic.util.detect_supported_devices', return_value=set())
#def test_detect_devices_none_found(faked, capsys, monkeypatch, qtbot):
#    """Test detect_devices()"""
#    widget = Form()
#    qtbot.addWidget(widget)
#    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
#
#    widget.detect_devices()
#    faked.assert_called()
#    out, err = capsys.readouterr()
#    assert re.search(r'No devices detected', out, re.MULTILINE)
#    assert err == ''


# Not sure why patch is not working
#@patch('meshtastic.util.findPorts', return_value=[])
#def test_update_ports_for_weird_tlora_no_ports(faked, capsys, monkeypatch, qtbot):
#    """Test update_ports_for_weird_tlora()"""
#    widget = Form()
#    qtbot.addWidget(widget)
#    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
#
#    widget.update_ports_for_weird_tlora()
#
#    faked.assert_called()
#    out, err = capsys.readouterr()
#    assert re.search(r'No devices detected', out, re.MULTILINE)
#    assert err == ''

# grp is not available on any system other than Linux... change?
#@patch('grp.getgrall')
#@patch('os.getlogin', return_value="bob")
#@patch('platform.system', return_value="Linux")
#def test_warn_linux_users_if_not_in_dialout_group(faked_system, faked_getlogin, faked_gr, capsys, monkeypatch, qtbot):
#    """Test update_ports_for_weird_tlora()"""
#    widget = Form()
#    qtbot.addWidget(widget)
#    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
#
#    widget.warn_linux_users_if_not_in_dialout_group()
#
#    faked_system.assert_called()
#    faked_getlogin.assert_called()
#    faked_gr.assert_called()
#    out, err = capsys.readouterr()
#    assert re.search(r'user is not in dialout group', out, re.MULTILINE)
#    assert err == ''
