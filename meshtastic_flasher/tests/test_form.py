"""Tests for Form()"""

import re


from unittest.mock import patch, MagicMock

from pytestqt.qt_compat import qt_api
from PySide6.QtWidgets import QMessageBox

from meshtastic.supported_device import SupportedDevice
#from meshtastic.serial_interface import SerialInterface

from meshtastic_flasher.installer import Form


def test_Form_title(qtbot):
    """Test for title var in Form"""
    widget = Form()
    qtbot.addWidget(widget)
    assert re.search(r'Meshtastic Flasher v1.0.', widget.windowTitle(), re.MULTILINE)


def test_buttons_and_combo_boxes(qtbot):
    """Test initial state of buttons and combo boxes in Form"""
    widget = Form()
    qtbot.addWidget(widget)

    # ensure buttons are present and enabled
    assert widget.get_versions_button.isEnabled()
    assert widget.select_detect.isEnabled()

    # ensure these are not enabled
    assert not widget.select_firmware_version.isEnabled()
    assert not widget.select_port.isEnabled()
    assert not widget.select_device.isEnabled()
    assert not widget.select_flash.isEnabled()


@patch('webbrowser.open')
def test_logo_clicked(fake_open, qtbot, capsys):
    """Test logo clicked in Form"""
    widget = Form()
    qtbot.addWidget(widget)
    qtbot.mouseClick(widget.logo, qt_api.QtCore.Qt.MouseButton.LeftButton)
    out, err = capsys.readouterr()
    assert re.search(r'The logo was clicked', out, re.MULTILINE)
    assert err == ''
    fake_open.assert_called()


@patch('esptool.main')
@patch('meshtastic_flasher.installer.Form.confirm_flash_question', return_value=True)
def test_flash_esp32_full_clicked_user_said_yes(fake_confirm, fake_esp, monkeypatch, qtbot, capsys):
    """Test clicked Flash in Form"""
    widget = Form()
    qtbot.addWidget(widget)

    # do some setup
    assert widget.select_port.count() == 0
    widget.select_port.addItem('fake1')
    assert widget.select_port.count() == 1

    assert widget.select_device.count() == 0
    widget.select_device.addItem('fake2')
    assert widget.select_device.count() == 1

    widget.select_flash.setEnabled(True)

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    qtbot.mouseClick(widget.select_flash, qt_api.QtCore.Qt.MouseButton.LeftButton)
    out, err = capsys.readouterr()
    assert re.search(r'Flash was clicked', out, re.MULTILINE)
    assert re.search(r'update only is not checked', out, re.MULTILINE)
    assert re.search(r'Step 1/4 esp32 full', out, re.MULTILINE)
    assert re.search(r'Step 2/4 esp32 full', out, re.MULTILINE)
    assert re.search(r'Step 3/4 esp32 full', out, re.MULTILINE)
    assert re.search(r'Step 4/4 esp32 full', out, re.MULTILINE)
    assert re.search(r'esp32 full complete', out, re.MULTILINE)
    assert err == ''
    fake_confirm.assert_called()
    fake_esp.assert_called()


@patch('esptool.main')
@patch('meshtastic_flasher.installer.Form.confirm_flash_question', return_value=True)
def test_flash_esp32_update_only_clicked_user_said_yes(fake_confirm, fake_esp, monkeypatch, qtbot, capsys):
    """Test clicked Flash in Form"""
    widget = Form()
    qtbot.addWidget(widget)

    # do some setup
    assert widget.select_port.count() == 0
    widget.select_port.addItem('fake1')
    assert widget.select_port.count() == 1

    assert widget.select_device.count() == 0
    widget.select_device.addItem('fake2')
    assert widget.select_device.count() == 1

    widget.advanced_form.update_only_cb.setChecked(True)
    widget.select_flash.setEnabled(True)

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    qtbot.mouseClick(widget.select_flash, qt_api.QtCore.Qt.MouseButton.LeftButton)
    out, err = capsys.readouterr()
    assert re.search(r'Flash was clicked', out, re.MULTILINE)
    assert re.search(r'update only is checked', out, re.MULTILINE)
    assert re.search(r'Step 1/2 esp32 update_only', out, re.MULTILINE)
    assert re.search(r'Step 2/2 esp32 update_only', out, re.MULTILINE)
    assert re.search(r'esp32 update_only complete', out, re.MULTILINE)
    assert err == ''
    fake_confirm.assert_called()
    fake_esp.assert_called()


@patch('shutil.copyfile')
@patch('meshtastic_flasher.installer.Form.confirm_flash_question', return_value=True)
def test_flash_nrf_clicked_user_said_yes(fake_confirm, fake_copy, monkeypatch, qtbot, capsys):
    """Test clicked Flash in Form"""
    widget = Form()
    qtbot.addWidget(widget)

    # do some setup
    assert widget.select_port.count() == 0
    widget.select_port.addItem('fake1')
    assert widget.select_port.count() == 1

    assert widget.select_device.count() == 0
    widget.select_device.addItem('fake2')
    assert widget.select_device.count() == 1

    widget.select_flash.setEnabled(True)
    widget.nrf = True

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    qtbot.mouseClick(widget.select_flash, qt_api.QtCore.Qt.MouseButton.LeftButton)
    out, err = capsys.readouterr()
    assert re.search(r'Flash was clicked', out, re.MULTILINE)
    assert re.search(r'Flash nrf52', out, re.MULTILINE)
    assert re.search(r'nrf52 file was copied', out, re.MULTILINE)
    assert err == ''
    fake_confirm.assert_called()
    fake_copy.assert_called()


@patch('meshtastic_flasher.installer.wrapped_detect_supported_devices', return_value=[])
def test_detect_devices_none_found(faked, capsys, monkeypatch, qtbot):
    """Test detect_devices()"""
    widget = Form()
    qtbot.addWidget(widget)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    widget.detect_devices()
    faked.assert_called()
    out, err = capsys.readouterr()
    assert re.search(r'No devices detected', out, re.MULTILINE)
    assert err == ''


@patch('meshtastic_flasher.installer.wrapped_detect_supported_devices')
def test_detect_devices_some_found(faked, capsys, monkeypatch, qtbot):
    """Test detect_devices()"""
    widget = Form()
    qtbot.addWidget(widget)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]
    faked.return_value = fake_supported_devices

    widget.detect_devices()
    faked.assert_called()
    out, err = capsys.readouterr()
    assert re.search(r'Detected', out, re.MULTILINE)
    assert err == ''
    assert widget.select_device.currentText() == "rak4631_5005"


@patch('meshtastic_flasher.installer.wrapped_detect_windows_needs_driver')
@patch('meshtastic_flasher.installer.wrapped_findPorts', return_value=[])
def test_detect_ports_using_find_ports_none_found(faked, faked_windows, monkeypatch, qtbot, capsys):
    """Test detect_ports_using_find_ports()"""
    widget = Form()
    qtbot.addWidget(widget)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]
    widget.detect_ports_using_find_ports([], fake_supported_devices)
    assert widget.select_port.count() == 0
    faked.assert_called()
    faked_windows.assert_called()
    out, err = capsys.readouterr()
    assert re.search(r'Warning: Could not find any ports', out, re.MULTILINE)
    assert err == ''


@patch('meshtastic_flasher.installer.wrapped_findPorts', return_value=['/dev/fake1','/dev/fake2'])
def test_detect_ports_using_find_ports_some_found(faked, monkeypatch, qtbot):
    """Test detect_ports_using_find_ports()"""
    widget = Form()
    qtbot.addWidget(widget)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]
    widget.detect_ports_using_find_ports([], fake_supported_devices)
    assert widget.select_port.count() == 2
    faked.assert_called()


@patch('meshtastic_flasher.installer.wrapped_findPorts', return_value=[])
def test_update_ports_for_weird_tlora_no_ports(faked, monkeypatch, qtbot):
    """Test update_ports_for_weird_tlora()"""
    widget = Form()
    qtbot.addWidget(widget)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
    ports = widget.update_ports_for_weird_tlora()
    assert len(ports) == 0
    faked.assert_called()


@patch('meshtastic_flasher.installer.wrapped_findPorts')
def test_update_ports_for_weird_tlora_two_ports(faked, monkeypatch, qtbot):
    """Test update_ports_for_weird_tlora()"""
    widget = Form()
    qtbot.addWidget(widget)
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
    faked.return_value = ['/dev/cu.usbmodem533C0052151', '/dev/cu.wchusbserial533C0052151']
    ports = widget.update_ports_for_weird_tlora()
    assert len(ports) == 2
    assert widget.select_port.currentText() == '/dev/cu.wchusbserial533C0052151'
    faked.assert_called()


# TODO: grp is not available on any system other than Linux... change?
#@patch('grp.getgrall')
#@patch('os.getlogin', return_value="bob")
#@patch('platform.system', return_value="Linux")
#def test_warn_linux_users_if_not_in_dialout_group(faked_system, faked_getlogin, faked_gr, capsys, monkeypatch, qtbot):
#    """Test update_ports_for_weird_tlora()"""
#    widget = Form()
#    qtbot.addWidget(widget)
#    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)
#
#    widget.warn_linux_users_if_not_in_dialout_group()
#
#    faked_system.assert_called()
#    faked_getlogin.assert_called()
#    faked_gr.assert_called()
#    out, err = capsys.readouterr()
#    assert re.search(r'user is not in dialout group', out, re.MULTILINE)
#    assert err == ''

@patch('meshtastic_flasher.installer.wrapped_active_ports_on_supported_devices')
def test_detect_ports_on_supported_devices_none_found(faked, qtbot):
    """Test detect_ports_on_supported_devices()"""
    widget = Form()
    qtbot.addWidget(widget)
    faked.return_value = set()
    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]
    ports = widget.detect_ports_on_supported_devices(fake_supported_devices)
    faked.assert_called()
    assert len(ports) == 0


@patch('meshtastic_flasher.installer.Form.update_ports_for_weird_tlora')
@patch('meshtastic_flasher.installer.wrapped_active_ports_on_supported_devices')
def test_detect_ports_on_supported_devices_some_found(faked_active_ports, faked_update_ports, qtbot):
    """Test detect_ports_on_supported_devices()"""
    widget = Form()
    qtbot.addWidget(widget)
    faked_active_ports.return_value = ('/dev/fake_usbmodem', '/dev/fake2')
    faked_update_ports.return_value = ['/dev/fake_usbmodem']
    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]

    ports = widget.detect_ports_on_supported_devices(fake_supported_devices)
    print(ports)

    faked_active_ports.assert_called()
    faked_update_ports.assert_called()
    assert len(ports) == 1


@patch('subprocess.getstatusoutput')
@patch('platform.system', return_value='Linux')
@patch('psutil.disk_partitions')
def test_detect_nrf_stuff_with_rak_and_current_bootloader_on_linux(fake_partitions, fake_system,
                                                                   fake_subprocess, monkeypatch,
                                                                   qtbot, capsys):
    """Test detect_nrf_stuff()"""

    # setup
    widget = Form()
    qtbot.addWidget(widget)

    mock_partition1 = MagicMock()
    mock_partition1.mountpoint = '/dev/fakevolume'
    mock_partition2 = MagicMock()
    mock_partition2.mountpoint = '/dev/RAK4631'
    mock_partitions = [mock_partition1, mock_partition2]
    fake_partitions.return_value = mock_partitions

    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]

    fake_subprocess.return_value = None , 'some fake stuff\nDate: Dec  1 2021\neven more'

    assert not widget.nrf

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    # make the call under test
    widget.detect_nrf_stuff(fake_supported_devices)

    assert widget.nrf
    fake_partitions.assert_called()
    fake_system.assert_called()
    fake_subprocess.assert_called()
    out, err = capsys.readouterr()
    assert re.search(r'nrf52 device detected', out, re.MULTILINE)
    assert re.search(r'partition:', out, re.MULTILINE)
    assert re.search(r'found RAK4631', out, re.MULTILINE)
    assert re.search(r'Bootloader info', out, re.MULTILINE)
    assert re.search(r'rak bootloader is current', out, re.MULTILINE)
    assert err == ''


@patch('subprocess.getstatusoutput')
@patch('platform.system', return_value='Linux')
@patch('psutil.disk_partitions')
def test_detect_nrf_stuff_with_techo_and_current_bootloader_on_linux(fake_partitions, fake_system,
                                                                     fake_subprocess, monkeypatch,
                                                                     qtbot, capsys):
    """Test detect_nrf_stuff()"""

    # setup
    widget = Form()
    qtbot.addWidget(widget)

    mock_partition1 = MagicMock()
    mock_partition1.mountpoint = '/dev/fakevolume'
    mock_partition2 = MagicMock()
    mock_partition2.mountpoint = '/dev/TECHOBOOT'
    mock_partitions = [mock_partition1, mock_partition2]
    fake_partitions.return_value = mock_partitions

    fake_device = SupportedDevice(name='b', for_firmware='t-echo')
    fake_supported_devices = [fake_device]

    fake_subprocess.return_value = None , 'some fake stuff\nDate: Oct 13 2021\neven more\nModel: LilyGo T-Echo\nfoo'

    assert not widget.nrf

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    # make the call under test
    widget.detect_nrf_stuff(fake_supported_devices)

    assert widget.nrf
    fake_partitions.assert_called()
    fake_system.assert_called()
    fake_subprocess.assert_called()
    out, err = capsys.readouterr()
    assert re.search(r'nrf52 device detected', out, re.MULTILINE)
    assert re.search(r'partition:', out, re.MULTILINE)
    assert re.search(r'definitely a T-Echo', out, re.MULTILINE)
    assert re.search(r't-echo bootloader is current', out, re.MULTILINE)
    assert err == ''


@patch('meshtastic_flasher.installer.wrapped_findPorts', return_value=['/dev/fake'])
@patch('urllib.request.urlretrieve')
@patch('os.path.exists', return_value=False)
@patch('subprocess.getstatusoutput')
@patch('platform.system', return_value='Linux')
@patch('psutil.disk_partitions')
def test_detect_nrf_stuff_with_rak_and_old_bootloader_on_linux(fake_partitions, fake_system,
                                                               fake_subprocess, fake_exists,
                                                               fake_url, fake_find_ports, monkeypatch,
                                                               qtbot, capsys):
    """Test when advanced option update RAK boot loader is checked"""

    # setup
    widget = Form()
    qtbot.addWidget(widget)

    widget.advanced_form.rak_bootloader_cb.setChecked(True)

    mock_partition1 = MagicMock()
    mock_partition1.mountpoint = '/dev/fakevolume'
    mock_partition2 = MagicMock()
    mock_partition2.mountpoint = '/dev/RAK4631'
    mock_partitions = [mock_partition1, mock_partition2]
    fake_partitions.return_value = mock_partitions

    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]

    fake_subprocess.return_value = None , 'some fake stuff\nDate: Sep  1 2020\neven more'

    assert not widget.nrf

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    # make the call under test
    widget.detect_nrf_stuff(fake_supported_devices)

    assert widget.nrf
    fake_partitions.assert_called()
    fake_system.assert_called()
    fake_subprocess.assert_called()
    fake_exists.assert_called()
    fake_url.assert_called()
    fake_find_ports.assert_called()
    out, err = capsys.readouterr()
    assert re.search(r'nrf52 device detected', out, re.MULTILINE)
    assert re.search(r'partition:', out, re.MULTILINE)
    assert re.search(r'found RAK4631', out, re.MULTILINE)
    assert re.search(r'Bootloader info', out, re.MULTILINE)
    #assert re.search(r'rak bootloader is not current', out, re.MULTILINE)
    assert re.search(r'Checking boot loader version', out, re.MULTILINE)
    assert re.search(r'Need to download', out, re.MULTILINE)
    assert re.search(r'done downloading', out, re.MULTILINE)
    assert err == ''


@patch('subprocess.getstatusoutput')
@patch('platform.system', return_value='Windows')
@patch('psutil.disk_partitions')
def test_detect_nrf_stuff_with_rak_and_current_bootloader_on_windows(fake_partitions, fake_system,
                                                                     fake_subprocess, monkeypatch,
                                                                     qtbot, capsys):
    """Test detect_nrf_stuff()"""

    # setup
    widget = Form()
    qtbot.addWidget(widget)

    mock_partition1 = MagicMock()
    mock_partition1.mountpoint = 'some fake windows drive'
    mock_partition2 = MagicMock()
    mock_partition2.mountpoint = 'RAK4631'
    mock_partitions = [mock_partition1, mock_partition2]
    fake_partitions.return_value = mock_partitions

    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]

    # Note: There are two calls to the subprocess, I'm just making one output work for both
    fake_subprocess.return_value = None , 'some fake stuff\nDate: Dec  1 2021\neven more\nRAK4631\n'

    assert not widget.nrf

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    # make the call under test
    widget.detect_nrf_stuff(fake_supported_devices)

    assert widget.nrf
    fake_partitions.assert_called()
    fake_system.assert_called()
    fake_subprocess.assert_called()
    out, err = capsys.readouterr()
    assert re.search(r'nrf52 device detected', out, re.MULTILINE)
    assert re.search(r'found partition on windows', out, re.MULTILINE)
    assert re.search(r'Bootloader info', out, re.MULTILINE)
    assert re.search(r'rak bootloader is current', out, re.MULTILINE)
    assert err == ''

@patch('platform.system', return_value='Linux')
@patch('psutil.disk_partitions')
def test_detect_nrf_stuff_partition_not_found_on_linux(fake_partitions, fake_system,
                                                       monkeypatch,
                                                       qtbot, capsys):
    """Test detect_nrf_stuff()"""

    # setup
    widget = Form()
    qtbot.addWidget(widget)

    mock_partition1 = MagicMock()
    mock_partition1.mountpoint = '/dev/fakevolume'
    mock_partition2 = MagicMock()
    mock_partition2.mountpoint = '/dev/foo'
    mock_partitions = [mock_partition1, mock_partition2]
    fake_partitions.return_value = mock_partitions

    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]

    assert not widget.nrf

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    # make the call under test
    widget.detect_nrf_stuff(fake_supported_devices)

    assert widget.nrf
    fake_partitions.assert_called()
    fake_system.assert_called()
    out, err = capsys.readouterr()
    assert re.search(r'nrf52 device detected', out, re.MULTILINE)
    assert re.search(r'Could not find the partition', out, re.MULTILINE)
    assert err == ''


@patch('subprocess.getstatusoutput')
@patch('platform.system', return_value='Linux')
@patch('psutil.disk_partitions')
def test_detect_nrf_stuff_with_rak_and_not_current_bootloader_on_linux(fake_partitions, fake_system,
                                                                       fake_subprocess, monkeypatch,
                                                                       qtbot, capsys):
    """Test detect_nrf_stuff()"""

    # setup
    widget = Form()
    qtbot.addWidget(widget)

    mock_partition1 = MagicMock()
    mock_partition1.mountpoint = '/dev/fakevolume'
    mock_partition2 = MagicMock()
    mock_partition2.mountpoint = '/dev/RAK4631'
    mock_partitions = [mock_partition1, mock_partition2]
    fake_partitions.return_value = mock_partitions

    fake_device = SupportedDevice(name='a', for_firmware='rak4631_5005')
    fake_supported_devices = [fake_device]

    fake_subprocess.return_value = None , 'some fake stuff\neven more'

    assert not widget.nrf

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    # make the call under test
    widget.detect_nrf_stuff(fake_supported_devices)

    assert widget.nrf
    fake_partitions.assert_called()
    fake_system.assert_called()
    fake_subprocess.assert_called()
    out, err = capsys.readouterr()
    assert re.search(r'nrf52 device detected', out, re.MULTILINE)
    assert re.search(r'partition:', out, re.MULTILINE)
    assert re.search(r'found RAK4631', out, re.MULTILINE)
    assert re.search(r'Bootloader info', out, re.MULTILINE)
    assert re.search(r'rak bootloader is not current', out, re.MULTILINE)
    assert err == ''


def test_confirm_flash_question_not_nrf(qtbot, capsys, monkeypatch):
    """Test confirm_flash_question()"""
    # setup
    widget = Form()
    qtbot.addWidget(widget)

    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)

    widget.confirm_flash_question("")

    out, err = capsys.readouterr()
    assert re.search(r'User confirmed they want to flash', out, re.MULTILINE)
    assert err == ''


def test_confirm_flash_question_nrf(qtbot, capsys, monkeypatch):
    """Test confirm_flash_question()"""
    # setup
    widget = Form()
    qtbot.addWidget(widget)

    widget.nrf = True

    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)

    widget.confirm_flash_question("")

    out, err = capsys.readouterr()
    assert re.search(r'User confirmed they want to flash', out, re.MULTILINE)
    assert err == ''


@patch('glob.glob')
@patch('os.path.exists', return_value=True)
def test_all_devices(fake_exists, fake_glob, qtbot):
    """Test all_devices()"""
    # setup
    widget = Form()
    qtbot.addWidget(widget)
    widget.firmware_version = '1.2.3'
    items = ['1.2.3/firmware-heltec-2.0-1.2.3abacdf.bin', '1.2.3/firmware-heltec-2.1-1.2.3abacdf.bin']
    fake_glob.return_value = iter(items)
    assert widget.select_device.count() == 0
    widget.all_devices()
    # 'Detected', 'All', and 2 devices above
    assert widget.select_device.count() == 4
    fake_exists.assert_called()
    fake_glob.assert_called()


# TODO: not sure why this is not patching
#@patch('meshtastic.serial_interface.SerialInterface')
#def test_version_and_device_from_info_with_ports(faked, qtbot):
#    """Test version_and_device_from_info()"""
#    # setup
#    widget = Form()
#    qtbot.addWidget(widget)
#    faked = MagicMock(autospec=SerialInterface)
#    ports=['/dev/fake1']
#
#    widget.version_and_device_from_info(ports)
#
#    faked.assert_called()


def test_update_device_dropdown(qtbot):
    """Test all_devices()"""
    widget = Form()
    qtbot.addWidget(widget)
    assert widget.select_device.count() == 0
    device='foo'
    widget.update_device_dropdown(device)
    # 'Detected' and the device 'foo'
    assert widget.select_device.count() == 2


def test_hwModel_to_device(qtbot):
    """Test hwModel_to_device()"""
    widget = Form()
    qtbot.addWidget(widget)
    assert widget.hwModel_to_device("HELTEC_V1") == "heltec-v1"
    assert widget.hwModel_to_device("HELTEC_V2_1") == "heltec-v2.1"
    assert widget.hwModel_to_device("HELTEC_V2_0") == "heltec-v2.0"
    assert widget.hwModel_to_device("MESHTASTIC_DIY_V1") == "meshtastic-diy-v1"
    assert widget.hwModel_to_device("RAK4631") == "rak4631_5005"
    assert widget.hwModel_to_device("T_ECHO") == "t-echo"
    assert widget.hwModel_to_device("TBEAM") == "tbeam"
    assert widget.hwModel_to_device("TBEAM0_7") == "tbeam0.7"
    assert widget.hwModel_to_device("TLORA_V1") == "tlora-v1"
    assert widget.hwModel_to_device("TLORA_V2") == "tlora-v2"
    assert widget.hwModel_to_device("TLORA_V2_1_1.6") == "tlora-v2-1-1.6"
    assert widget.hwModel_to_device("TLORA_V1_3") == "tlora_v1_3"
