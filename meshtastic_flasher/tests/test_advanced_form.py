"""tests for AdvancedForm"""
import re

from pytestqt.qt_compat import qt_api

from PySide6.QtWidgets import QMessageBox

from meshtastic_flasher.form import Form
from meshtastic_flasher.advanced_form import AdvancedForm

def test_advanced_form(qtbot, monkeypatch, capsys):
    """Test for AdvancedForm"""
    f = Form()
    af = AdvancedForm(f)
    qtbot.addWidget(f)
    qtbot.addWidget(af)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
    qtbot.mouseClick(af.ok_button, qt_api.QtCore.Qt.MouseButton.LeftButton)
    out, err = capsys.readouterr()
    assert re.search(r'OK button was clicked', out, re.MULTILINE)
    assert err == ''
