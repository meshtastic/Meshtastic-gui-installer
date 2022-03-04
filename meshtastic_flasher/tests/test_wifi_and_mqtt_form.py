"""Tests for wifi_and_mqtt_form"""

import re

from unittest.mock import patch

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

    # form loaded - ensure all default values and all fields have tool tips

    # WiFi
    assert widget.wifi_ap_mode.isChecked() is False
    assert widget.wifi_ap_mode.toolTip() != ''
    assert widget.wifi_ssid.text() == ''
    assert widget.wifi_ssid.toolTip() != ''
    assert widget.wifi_password.text() == ''
    assert widget.wifi_password.toolTip() != ''
    # MQTT
    assert widget.mqtt_disabled.isChecked() is False
    assert widget.mqtt_disabled.toolTip() != ''
    assert widget.mqtt_server.text() == ''
    assert widget.mqtt_server.toolTip() != ''
    assert widget.mqtt_username.text() == ''
    assert widget.mqtt_username.toolTip() != ''
    assert widget.mqtt_password.text() == ''
    assert widget.mqtt_password.toolTip() != ''
    assert widget.mqtt_encryption_enabled.isChecked() is False
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

    # TODO: for save
    #qtbot.mouseClick(widget.button_box, qt_api.QtCore.Qt.MouseButton.LeftButton)


@patch('meshtastic.serial_interface.SerialInterface')
def test_get_prefs(fake_si, qtbot, capsys):
    """Test get_prefs()"""
    radioConfig = RadioConfig()
    #radioConfig.preferences.position_flags = 35
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
