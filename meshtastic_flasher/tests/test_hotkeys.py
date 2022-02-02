"""Test hotkeys
"""
import re

from PySide6.QtWidgets import QMessageBox

from meshtastic_flasher.installer import Form

def test_hotkey_h(qtbot, monkeypatch, capsys):
    """Test hot key 'h' """
    widget = Form()
    qtbot.addWidget(widget)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
    qtbot.keyPress(widget, "h")
    out, err = capsys.readouterr()
    assert re.search(r'hotkeys', out, re.MULTILINE)
    assert err == ''
