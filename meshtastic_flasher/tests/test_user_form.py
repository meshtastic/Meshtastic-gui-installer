"""Tests for user_form"""

import re

from unittest.mock import patch

from PySide6 import QtCore

from meshtastic_flasher.settings import Settings
from meshtastic_flasher.user_form import UserForm


def test_form_cancel(qtbot, capsys):
    """Test cancel form"""
    settings = Settings()
    widget = UserForm(settings)
    qtbot.addWidget(settings)
    qtbot.addWidget(widget)

    # ensure default values
    assert widget.device_id.text() == ''
    assert widget.hw_model.text() == ''
    assert widget.macaddr.text() == ''
    assert widget.long_name.text() == ''
    assert widget.short_name.text() == ''
    assert widget.is_licensed.isChecked() is False
    assert widget.team.currentText() == ''

    # ensure tooltips
    assert widget.device_id.toolTip() != ''
    assert widget.hw_model.toolTip() != ''
    assert widget.macaddr.toolTip() != ''
    assert widget.long_name.toolTip() != ''
    assert widget.short_name.toolTip() != ''
    assert widget.is_licensed.toolTip() != ''
    assert widget.team.toolTip() != ''

    # ensure labels on inputs
    assert widget.form_layout.labelForField(widget.device_id) != ''
    assert widget.form_layout.labelForField(widget.hw_model) != ''
    assert widget.form_layout.labelForField(widget.macaddr) != ''
    assert widget.form_layout.labelForField(widget.long_name) != ''
    assert widget.form_layout.labelForField(widget.short_name) != ''
    assert widget.form_layout.labelForField(widget.is_licensed) != ''
    assert widget.form_layout.labelForField(widget.team) != ''

    qtbot.keyPress(widget, QtCore.Qt.Key_Escape)
    out, err = capsys.readouterr()
    assert re.search(r'user CANCELLED form', out, re.MULTILINE)
    assert err == ''


def test_get_values(qtbot, iface_with_nodes):
    """Test get_values()"""
    settings = Settings()
    widget = UserForm(settings)
    qtbot.addWidget(settings)
    qtbot.addWidget(widget)
    iface = iface_with_nodes
    iface.myInfo.my_node_num = 2475227164
    widget.interface = iface
    widget.get_values()
    assert widget.device_id.text() == '!9388f81c'
    assert widget.hw_model.text() == 'TBEAM'
    assert widget.macaddr.text() == '44:17:93:88:f8:1c'
    assert widget.long_name.text() == 'Unknown f81c'
    assert widget.short_name.text() == '?1C'
    assert widget.is_licensed.isChecked() is False
    assert widget.team.currentText() == 'CLEAR'


def test_get_values2(qtbot, iface_with_nodes_no_keys):
    """Test get_values()"""
    settings = Settings()
    widget = UserForm(settings)
    qtbot.addWidget(settings)
    qtbot.addWidget(widget)
    iface = iface_with_nodes_no_keys
    iface.myInfo.my_node_num = 2475227164
    widget.interface = iface
    widget.get_values()
    assert widget.device_id.text() == ''
    assert widget.hw_model.text() == ''
    assert widget.macaddr.text() == ''
    assert widget.long_name.text() == ''
    assert widget.short_name.text() == ''
    assert widget.is_licensed.isChecked() is True
    assert widget.team.currentText() == 'BLUE'


@patch('meshtastic_flasher.user_form.UserForm.get_values')
def test_run(fake_get_values, qtbot):
    """Test run()"""
    settings = Settings()
    widget = UserForm(settings)
    qtbot.addWidget(settings)
    qtbot.addWidget(widget)
    widget.run(port='foo2', interface='bar')
    fake_get_values.assert_called()
