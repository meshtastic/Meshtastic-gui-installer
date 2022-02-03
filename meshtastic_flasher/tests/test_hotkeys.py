"""Test hotkeys
"""
import re

from unittest.mock import patch

from PySide6.QtWidgets import QMessageBox

from meshtastic_flasher.installer import Form

def test_hotkey_a(qtbot, capsys):
    """Test hot key 'a' """
    widget = Form()
    qtbot.addWidget(widget)
    qtbot.keyPress(widget, "a")
    widget.advanced_form.close_advanced_options()
    out, err = capsys.readouterr()
    assert re.search(r'A was pressed', out, re.MULTILINE)
    assert re.search(r'OK button was clicked in advanced options', out, re.MULTILINE)
    assert err == ''


@patch('meshtastic_flasher.installer.unzip_if_necessary')
@patch('meshtastic_flasher.installer.download_if_zip_does_not_exist')
@patch('meshtastic_flasher.installer.get_tags_from_github', return_value=['v1.2.53aa', 'v1.2.53fff', 'v1.2.51f'])
def test_hotkey_g(fake_get_tags, fake_download, fake_unzip, qtbot, capsys):
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


def test_hotkey_h(qtbot, monkeypatch, capsys):
    """Test hot key 'h' """
    widget = Form()
    qtbot.addWidget(widget)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
    qtbot.keyPress(widget, "h")
    out, err = capsys.readouterr()
    assert re.search(r'hotkeys', out, re.MULTILINE)
    assert re.search(r'H was pressed', out, re.MULTILINE)
    assert err == ''


def test_hotkey_q(qtbot, capsys):
    """Test hot key 'q' """
    widget = Form()
    qtbot.addWidget(widget)
    qtbot.keyPress(widget, "q")
    out, err = capsys.readouterr()
    assert re.search(r'Q was pressed', out, re.MULTILINE)
    assert err == ''
