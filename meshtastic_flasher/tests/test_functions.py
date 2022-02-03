""" Test functions in installer.py
"""

from unittest.mock import patch

from meshtastic_flasher.installer import (get_path, populate_tag_in_firmware_dropdown,
                                          tag_to_version, tags_to_versions, get_tags)

def test_get_path():
    """Test get_path()"""
    assert get_path("foo.file").endswith("foo.file")
    assert len(get_path("foo.file")) > 10

def test_populate_tag_in_firmware_dropdown():
    """Test populate_tag_in_firmware_dropdown()"""
    assert populate_tag_in_firmware_dropdown("v1.2.52.foo")
    assert not populate_tag_in_firmware_dropdown("v1.2.51.foo")

def test_tag_to_version():
    """Test tag to version"""
    assert tag_to_version('') == ''
    assert tag_to_version('v123') == '123'
    assert tag_to_version('123') == '123'

def test_tags_to_versions():
    """Test tags to versions"""
    assert not tags_to_versions([])
    assert tags_to_versions(['v123','v234']) == ['123', '234']
    assert tags_to_versions(['123','234']) == ['123', '234']

@patch('meshtastic_flasher.installer.get_tags_from_github', return_value=[])
def test_get_tags_got_no_tags(fake_get_tags):
    """Test get_tags() when we got no tags"""
    tags = get_tags()
    assert len(tags) == 1
    fake_get_tags.assert_called()

@patch('meshtastic_flasher.installer.get_tags_from_github', return_value=['v1.2.53aa', 'v1.2.53fff', '1.2.51f'])
def test_get_tags_got_some_tags(fake_get_tags):
    """Test get_tags() when we got some tags"""
    tags = get_tags()
    assert len(tags) == 2
    fake_get_tags.assert_called()
