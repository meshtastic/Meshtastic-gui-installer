"""Tests for radio_form"""

import re

from unittest.mock import patch

from PySide6 import QtCore

#from meshtastic.radioconfig_pb2 import RadioConfig

from meshtastic_flasher.settings import Settings
from meshtastic_flasher.radio_form import RadioForm


def test_form_cancel(qtbot, capsys):
    """Test cancel form"""
    settings = Settings()
    widget = RadioForm(settings)
    qtbot.addWidget(settings)
    qtbot.addWidget(widget)

    # ensure default values
    assert widget.is_router.isChecked() is False
    assert widget.region.currentText() == ''
    assert widget.debug_log_enabled.isChecked() is False
    assert widget.serial_disabled.isChecked() is False
    assert widget.auto_screen_carousel_secs.text() == ''
    assert widget.frequency_offset.text() == ''
    assert widget.hop_limit.text() == ''
    assert widget.is_lora_tx_disabled.isChecked() is False
    assert widget.send_owner_interval.text() == ''

    # ensure tooltips
    assert widget.is_router.toolTip() != ''
    assert widget.region.toolTip() != ''
    assert widget.debug_log_enabled.toolTip() != ''
    assert widget.serial_disabled.toolTip() != ''
    assert widget.auto_screen_carousel_secs.toolTip() != ''
    assert widget.frequency_offset.toolTip() != ''
    assert widget.hop_limit.toolTip() != ''
    assert widget.is_lora_tx_disabled.toolTip() != ''
    assert widget.send_owner_interval.toolTip() != ''

    # ensure labels on inputs
    assert widget.form_layout.labelForField(widget.is_router) != ''
    assert widget.form_layout.labelForField(widget.region) != ''
    assert widget.form_layout.labelForField(widget.debug_log_enabled) != ''
    assert widget.form_layout.labelForField(widget.serial_disabled) != ''
    assert widget.form_layout.labelForField(widget.auto_screen_carousel_secs) != ''
    assert widget.form_layout.labelForField(widget.frequency_offset) != ''
    assert widget.form_layout.labelForField(widget.hop_limit) != ''
    assert widget.form_layout.labelForField(widget.is_lora_tx_disabled) != ''
    assert widget.form_layout.labelForField(widget.send_owner_interval) != ''

    qtbot.keyPress(widget, QtCore.Qt.Key_Escape)
    out, err = capsys.readouterr()
    assert re.search(r'user CANCELLED form', out, re.MULTILINE)
    assert err == ''


#@patch('meshtastic.serial_interface.SerialInterface')
#def test_get_values_defaults(fake_si, qtbot, capsys):
#    """Test get_values()"""
#    radioConfig = RadioConfig()
#    radioConfig.preferences.auto_screen_carousel_secs = 0
#    radioConfig.preferences.frequency_offset = 0
#    radioConfig.preferences.send_owner_interval = 0
#    radioConfig.preferences.hop_limit = 0
#    fake_si.getNode().return_value = radioConfig
#    settings = Settings()
#    widget = RadioForm(settings)
#    qtbot.addWidget(settings)
#    qtbot.addWidget(widget)
#    widget.get_values()
#    fake_si.assert_called()
#    out, err = capsys.readouterr()
#    assert re.search(r'interface was none', out, re.MULTILINE)
#    assert err == ''
#
#    assert widget.is_router.isChecked() is False
#    assert widget.region.currentText() == 'Unset'
#    assert widget.debug_log_enabled.isChecked() is False
#    assert widget.serial_disabled.isChecked() is False
#    # TODO:
#    #assert widget.auto_screen_carousel_secs.text() == ''
#    #assert widget.frequency_offset.text() == ''
#    #assert widget.hop_limit.text() == ''
#    assert widget.is_lora_tx_disabled.isChecked() is False
#    #assert widget.send_owner_interval.text() == ''


#def test_get_values(qtbot, capsys):
#    """Test get_values()"""
#    radioConfig = RadioConfig()
#    radioConfig.preferences.is_router = True
#    radioConfig.preferences.region = 1
#    radioConfig.preferences.debug_log_enabled = True
#    radioConfig.preferences.serial_disabled = True
#    radioConfig.preferences.auto_screen_carousel_secs = 20
#    radioConfig.preferences.frequency_offset = 20
#    radioConfig.preferences.send_owner_interval = 20
#    radioConfig.preferences.hop_limit = 4
#    fake_si.getNode().return_value = radioConfig
#    settings = Settings()
#    widget = RadioForm(settings)
#    qtbot.addWidget(settings)
#    qtbot.addWidget(widget)
#    widget.get_values()
#    fake_si.assert_called()
#    out, err = capsys.readouterr()
#    assert re.search(r'interface was none', out, re.MULTILINE)
#    assert err == ''
#
#    assert widget.is_router.isChecked() is True
#    #assert widget.region.currentText() == 'Unset'
#    #assert widget.debug_log_enabled.isChecked() is False
#    #assert widget.serial_disabled.isChecked() is False
#    # TODO:
#    #assert widget.auto_screen_carousel_secs.text() == ''
#    #assert widget.frequency_offset.text() == ''
#    #assert widget.hop_limit.text() == ''
#    #assert widget.is_lora_tx_disabled.isChecked() is False
#    #assert widget.send_owner_interval.text() == ''


@patch('meshtastic_flasher.radio_form.RadioForm.get_values')
def test_run(fake_get_values, qtbot):
    """Test run()"""
    settings = Settings()
    widget = RadioForm(settings)
    qtbot.addWidget(settings)
    qtbot.addWidget(widget)
    widget.run(port='foo2', interface='bar')
    fake_get_values.assert_called()
