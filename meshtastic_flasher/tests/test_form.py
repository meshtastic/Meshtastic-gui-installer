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
