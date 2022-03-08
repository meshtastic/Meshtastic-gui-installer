"""Tests for fixed_position"""

#import re

from unittest.mock import patch, MagicMock

from PySide6 import QtCore

#from meshtastic.radioconfig_pb2 import RadioConfig

from meshtastic_flasher.settings import Settings
from meshtastic_flasher.position_form import PositionForm
from meshtastic_flasher.fixed_position_form import FixedPositionForm


def test_form_cancel(qtbot):
    """Test cancel form"""
    settings = Settings()
    pos_form = PositionForm(settings)
    widget = FixedPositionForm(pos_form)
    qtbot.addWidget(settings)
    qtbot.addWidget(pos_form)
    qtbot.addWidget(widget)

    # ensure default values
    assert widget.fixed_position.isChecked() is False
    assert widget.lat.text() == ''
    assert widget.lon.text() == ''
    assert widget.lat.text() == ''

    # ensure tooltips
    assert widget.fixed_position.toolTip() != ''
    assert widget.lat.toolTip() != ''
    assert widget.lon.toolTip() != ''
    assert widget.alt.toolTip() != ''

    # ensure labels on inputs
    assert widget.form_layout.labelForField(widget.fixed_position) != ''
    assert widget.form_layout.labelForField(widget.lat) != ''
    assert widget.form_layout.labelForField(widget.lon) != ''
    assert widget.form_layout.labelForField(widget.alt) != ''

    qtbot.keyPress(widget, QtCore.Qt.Key_Escape)


#def test_get_values(qtbot, capsys, iface_with_nodes):
#    """Test get_values()"""
#
#    settings = Settings()
#    pos_form = PositionForm(settings)
#    widget = FixedPositionForm(pos_form)
#    qtbot.addWidget(settings)
#    qtbot.addWidget(pos_form)
#    qtbot.addWidget(widget)
#
#    # set prefs
#    #prefs = MagicMock()
#    #prefs.fixed_position = True
#    radioConfig = RadioConfig()
#    radioConfig.preferences.fixed_position = True
#
#    iface = iface_with_nodes
#    iface.myInfo.my_node_num = 2475227164
#    iface.myInfo.latitude = 100
#    iface.myInfo.longitude = 101
#    iface.myInfo.altitude = 102
#    widget.interface = iface
#    print(f'iface:{iface}')
#
#    fake.return_value = radioConfig
#
#    widget.get_values()
#
#    # ensure we get values
#    # TODO assert widget.fixed_position.isChecked() is True
#    assert widget.lat.text() == '100'
#    assert widget.lon.text() == '101'
#    assert widget.alt.text() == '102'
#
#    fake.assert_called()
#    out, err = capsys.readouterr()
#    assert re.search(r'interface was none', out, re.MULTILINE)
#    assert err == ''


@patch('meshtastic_flasher.fixed_position_form.FixedPositionForm.get_values')
def test_run_no_values(fake_get_values, qtbot):
    """Test run()"""
    settings = Settings()
    pos_form = PositionForm(settings)
    widget = FixedPositionForm(pos_form)
    qtbot.addWidget(settings)
    qtbot.addWidget(pos_form)
    qtbot.addWidget(widget)

    # set prefs
    prefs = MagicMock()
    prefs.fixed_position = None
    prefs.lat = None
    prefs.lon = None
    prefs.alt = None

    widget.prefs = prefs

    widget.run(port='foo', interface='bar')

    fake_get_values.assert_called()

    # ensure all defaults
    assert widget.fixed_position.isChecked() is False
    assert widget.lat.text() == ''
    assert widget.lon.text() == ''
    assert widget.alt.text() == ''


@patch('meshtastic_flasher.fixed_position_form.FixedPositionForm.get_values')
def test_run(fake_get_values, qtbot):
    """Test run()"""
    settings = Settings()
    pos_form = PositionForm(settings)
    widget = FixedPositionForm(pos_form)
    qtbot.addWidget(settings)
    qtbot.addWidget(pos_form)
    qtbot.addWidget(widget)

    # set prefs
    prefs = MagicMock()
    prefs.fixed_position = True
    prefs.lat = '100'
    prefs.lon = '101'
    prefs.alt = '102'

    widget.prefs = prefs

    widget.run(port='foo2', interface='bar')

    fake_get_values.assert_called()



#def test_write_values(qtbot, capsys):
#    """Test write_values()"""
#    settings = Settings()
#    pos_form = PositionForm(settings)
#    widget = FixedPositionForm(pos_form)
#    qtbot.addWidget(settings)
#    qtbot.addWidget(pos_form)
#    qtbot.addWidget(widget)
#
#    widget.interface = MagicMock()
#
#    widget.write_values()
#
#    out, err = capsys.readouterr()
#    assert re.search(r'Set fixed_position to', out, re.MULTILINE)
#    assert re.search(r'lat:', out, re.MULTILINE)
#    assert re.search(r'lon:', out, re.MULTILINE)
#    assert re.search(r'alt:', out, re.MULTILINE)
#    assert err == ''
