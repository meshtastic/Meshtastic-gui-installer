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


def test_update_status(qtbot):
    """Test update_status()"""
    widget = EsptoolForm()
    qtbot.addWidget(widget)
    assert widget.status_label.text() != 'foo'
    widget.update_status('foo')
    assert widget.status_label.text() == 'foo'


def test_do_finished(qtbot):
    """Test do_finished()"""
    widget = EsptoolForm()
    qtbot.addWidget(widget)
    assert widget.status_label.text() != ''
    assert widget.ok_button.isHidden() is True
    widget.do_finished()
    assert widget.status_label.text() == ''
    assert widget.ok_button.isHidden() is False


def test_receive_data(qtbot):
    """Test receive_data()"""
    widget = EsptoolForm()
    qtbot.addWidget(widget)
    assert widget.text.toPlainText() == ''
    widget.receive_data('foo')
    assert widget.text.toPlainText() == 'foo'
    # ensure no blank lines are added
    widget.receive_data('\n')
    assert widget.text.toPlainText() == 'foo'
    widget.receive_data('bar\n')
    assert widget.text.toPlainText() == 'foo\nbar'
