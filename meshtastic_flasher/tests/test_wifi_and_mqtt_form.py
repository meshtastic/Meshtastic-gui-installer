"""Tests for wifi_and_mqtt_form"""

import re

from unittest.mock import patch, MagicMock

from PySide6 import QtCore

from meshtastic.radioconfig_pb2 import RadioConfig

from meshtastic_flasher.settings import Settings
from meshtastic_flasher.wifi_and_mqtt_form import Wifi_and_MQTT_Form


def test_form_cancel(qtbot, capsys):
    """Test cancel form"""
    settings = Settings()
    widget = Wifi_and_MQTT_Form(settings)
    qtbot.addWidget(settings)
    qtbot.addWidget(widget)

    # ensure default values
    assert widget.wifi_ap_mode.isChecked() is False
    assert widget.wifi_ssid.text() == ''
    assert widget.wifi_password.text() == ''
    assert widget.mqtt_disabled.isChecked() is False
    assert widget.mqtt_server.text() == ''
    assert widget.mqtt_username.text() == ''
    assert widget.mqtt_password.text() == ''
    assert widget.mqtt_encryption_enabled.isChecked() is False

    # ensure tooltips
    assert widget.wifi_ap_mode.toolTip() != ''
    assert widget.wifi_ssid.toolTip() != ''
    assert widget.wifi_password.toolTip() != ''
    assert widget.mqtt_disabled.toolTip() != ''
    assert widget.mqtt_server.toolTip() != ''
    assert widget.mqtt_username.toolTip() != ''
    assert widget.mqtt_password.toolTip() != ''
    assert widget.mqtt_encryption_enabled.toolTip() != ''

    # ensure labels on inputs
    assert widget.form_layout.labelForField(widget.wifi_ap_mode) != ''
    assert widget.form_layout.labelForField(widget.wifi_ssid) != ''
    assert widget.form_layout.labelForField(widget.wifi_password) != ''
    assert widget.form_layout.labelForField(widget.mqtt_disabled) != ''
    assert widget.form_layout.labelForField(widget.mqtt_server) != ''
    assert widget.form_layout.labelForField(widget.mqtt_username) != ''
    assert widget.form_layout.labelForField(widget.mqtt_password) != ''
    assert widget.form_layout.labelForField(widget.mqtt_encryption_enabled) != ''

    qtbot.keyPress(widget, QtCore.Qt.Key_Escape)
    out, err = capsys.readouterr()
    assert re.search(r'user CANCELLED form', out, re.MULTILINE)
    assert err == ''


@patch('meshtastic.serial_interface.SerialInterface')
def test_get_prefs(fake_si, qtbot, capsys):
    """Test get_prefs()"""
    radioConfig = RadioConfig()
    fake_si.getNode().return_value = radioConfig
    settings = Settings()
    widget = Wifi_and_MQTT_Form(settings)
    qtbot.addWidget(settings)
    qtbot.addWidget(widget)
    widget.get_prefs()
    fake_si.assert_called()
    out, err = capsys.readouterr()
    assert re.search(r'interface was none', out, re.MULTILINE)
    assert err == ''


@patch('meshtastic_flasher.wifi_and_mqtt_form.Wifi_and_MQTT_Form.get_prefs')
def test_run_no_prefs(fake_get_prefs, qtbot):
    """Test run()"""
    settings = Settings()
    widget = Wifi_and_MQTT_Form(settings)
    qtbot.addWidget(settings)
    qtbot.addWidget(widget)

    # set prefs
    prefs = MagicMock()
    prefs.wifi_ap_mode = None
    prefs.wifi_ssid = None
    prefs.wifi_password = None
    prefs.mqtt_disabled = None
    prefs.mqtt_server = None
    prefs.mqtt_username = None
    prefs.mqtt_password = None
    prefs.mqtt_encryption_enabled = None

    widget.prefs = prefs

    widget.run(port='foo', interface='bar')

    fake_get_prefs.assert_called()

    # ensure all defaults
    assert widget.wifi_ap_mode.isChecked() is False
    assert widget.wifi_ssid.text() == ''
    assert widget.wifi_password.text() == ''
    assert widget.mqtt_disabled.isChecked() is False
    assert widget.mqtt_server.text() == ''
    assert widget.mqtt_username.text() == ''
    assert widget.mqtt_password.text() == ''
    assert widget.mqtt_encryption_enabled.isChecked() is False


@patch('meshtastic_flasher.wifi_and_mqtt_form.Wifi_and_MQTT_Form.get_prefs')
def test_run(fake_get_prefs, qtbot):
    """Test run()"""
    settings = Settings()
    widget = Wifi_and_MQTT_Form(settings)
    qtbot.addWidget(settings)
    qtbot.addWidget(widget)

    # set prefs
    prefs = MagicMock()
    prefs.wifi_ap_mode = True
    prefs.wifi_ssid = 'foo'
    prefs.wifi_password = 'sekrit'
    prefs.mqtt_disabled = True
    prefs.mqtt_server = 'boo'
    prefs.mqtt_username = 'bar'
    prefs.mqtt_password = 'baz'
    prefs.mqtt_encryption_enabled = True

    widget.prefs = prefs

    widget.run(port='foo2', interface='bar')

    fake_get_prefs.assert_called()

    # ensure all defaults
    assert widget.wifi_ap_mode.isChecked() is True
    assert widget.wifi_ssid.text() == 'foo'
    assert widget.wifi_password.text() == 'sekrit'
    assert widget.mqtt_disabled.isChecked() is True
    assert widget.mqtt_server.text() == 'boo'
    assert widget.mqtt_username.text() == 'bar'
    assert widget.mqtt_password.text() == 'baz'
    assert widget.mqtt_encryption_enabled.isChecked() is True


def test_write_prefs(qtbot, capsys):
    """Test write_prefs()"""
    settings = Settings()
    widget = Wifi_and_MQTT_Form(settings)
    qtbot.addWidget(settings)
    qtbot.addWidget(widget)

    widget.interface = MagicMock()

    widget.write_prefs()

    out, err = capsys.readouterr()
    assert re.search(r'Set wifi_ap_mode to', out, re.MULTILINE)
    assert re.search(r'Set wifi_ssid to', out, re.MULTILINE)
    assert re.search(r'Set wifi_password to', out, re.MULTILINE)
    assert re.search(r'Set mqtt_disabled to', out, re.MULTILINE)
    assert re.search(r'Set mqtt_server to', out, re.MULTILINE)
    assert re.search(r'Set mqtt_username to', out, re.MULTILINE)
    assert re.search(r'Set mqtt_password to', out, re.MULTILINE)
    assert re.search(r'Set mqtt_encryption_enabled to', out, re.MULTILINE)
    assert err == ''
