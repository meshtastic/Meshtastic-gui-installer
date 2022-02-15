"""Tests for EsptoolForm()"""

import re

from meshtastic_flasher.esptool_form import EsptoolForm, Worker


def test_EsptoolForm(qtbot):
    """Test EsptoolForm()"""
    widget = EsptoolForm()
    qtbot.addWidget(widget)
    widget.start(port='foo', device_file='bar',
                 system_info_file='baz', bin_file='bam',
                 test=True)

def test_Worker_run_full(capsys):
    """Test Worker().run()"""
    a_worker = Worker(update_only=False, port='foo', device_file='bar',
                      system_info_file='baz', bin_file='bam',
                      test=True)
    a_worker.run()
    out, err = capsys.readouterr()
    assert re.search(r'Step 1/4 esp32 full', out, re.MULTILINE)
    assert re.search(r'Step 2/4 esp32 full', out, re.MULTILINE)
    assert re.search(r'Step 3/4 esp32 full', out, re.MULTILINE)
    assert re.search(r'Step 4/4 esp32 full', out, re.MULTILINE)
    assert err == ''


def test_Worker_run_update(capsys):
    """Test Worker().run()"""
    a_worker = Worker(update_only=True, port='foo', device_file='bar',
                      system_info_file='baz', bin_file='bam',
                      test=True)
    a_worker.run()
    out, err = capsys.readouterr()
    assert re.search(r'Step 1/2 esp32 update', out, re.MULTILINE)
    assert re.search(r'Step 2/2 esp32 update', out, re.MULTILINE)
    assert err == ''


def test_Worker_isatty():
    """Test Worker().isatty()"""
    a_worker = Worker(test=True)
    assert a_worker.isatty() is False
