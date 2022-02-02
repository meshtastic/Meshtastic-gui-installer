""" Test functions in installer.py
"""

from meshtastic_flasher.installer import get_path, populate_tag_in_firmware_dropdown

def test_get_path():
    """Test get_path()"""
    assert get_path("foo.file").endswith("foo.file")
    assert len(get_path("foo.file")) > 10

def test_populate_tag_in_firmware_dropdown():
    """Test populate_tag_in_firmware_dropdown()"""
    assert populate_tag_in_firmware_dropdown("v1.2.52.foo")
    assert not populate_tag_in_firmware_dropdown("v1.2.51.foo")
