"""Utility functions for meshtastic-flasher"""
import os
import sys
import re
import urllib
import ssl
import json
import zipfile
import requests

from github import Github

from meshtastic.util import findPorts, detect_supported_devices, detect_windows_needs_driver, active_ports_on_supported_devices

import meshtastic_flasher.version

MESHTATIC_REPO = 'meshtastic/Meshtastic-device'


# see https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
# but had to tweak for pypi
def get_path(filename):
    """return the path to the logo file"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    # return path to where this file is located
    path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(path, filename)


def wrapped_findPorts():
    """Run findPorts()
       These wrappers are because I could not figure out how to patch
       meshtastic.util.findPorts(). But, if I wrap it, here,
       I can patch this function.
    """
    return findPorts(True)


def wrapped_detect_supported_devices():
    """Run detect_supported_devices()"""
    return detect_supported_devices()


def wrapped_detect_windows_needs_driver(device, want_output):
    """Run detect_windows_needs_driver()"""
    return detect_windows_needs_driver(device, want_output)


def wrapped_active_ports_on_supported_devices(supported_devices):
    """Run active_ports_on_supported_devices()"""
    return active_ports_on_supported_devices(supported_devices, True)


def populate_tag_in_firmware_dropdown(tag):
    """Populate this tag in the firmware dropdown?"""
    retval = False
    if re.search(r"v1.2.5[2-9]", tag):
        retval = True
    print(f'tag:{tag} populate in dropdown?:{retval}')
    return retval


def tag_to_version(tag):
    """Return version from a tag by dropping the leading 'v'."""
    version = ""
    if len(tag) > 0:
        if tag.startswith('v'):
            version = tag[1:]
        else:
            version = tag
    return version


def tags_to_versions(tags):
    """Return a collection of versions from a collection of tags."""
    versions = []
    for tag in tags:
        versions.append(tag_to_version(tag))
    return versions


def get_tags_from_github():
    """Get tags from GitHub"""
    tags = []
    try:
        token = Github()
        repo = token.get_repo(MESHTATIC_REPO)
        releases = repo.get_releases()
        count = 0
        for release in releases:
            r = repo.get_release(release.id)
            tags.append(r.tag_name)
            count = count + 1
            if count > 20:
                break
    except Exception as e:
        print(e)
    return tags


def get_tags():
    """Ensure we have some tag to use."""
    tags = []
    tags_from_github = get_tags_from_github()
    for tag in tags_from_github:
        #print(f'tag:{tag}')
        if populate_tag_in_firmware_dropdown(tag):
            tags.append(tag)
    if len(tags) == 0:
        tags.append('v1.2.53.19c1f9f')
    return tags


def zip_file_name_from_version(version):
    """Get the filename for a zip file for a version."""
    # zip filename from version
    zip_file_name = "firmware-"
    zip_file_name += version
    zip_file_name += ".zip"
    return zip_file_name


def download_if_zip_does_not_exist(zip_file_name, version):
    """Download the zip_file_name"""
    # if the file is not already downloaded, download it
    if not os.path.exists(zip_file_name):
        print("Need to download...")

        # Note: Probably should use the browser_download_url. Sample url
        #   https://github.com/meshtastic/Meshtastic-device/releases/download/v1.2.53.19c1f9f/firmware-1.2.53.19c1f9f.zip
        zip_file_url = f'https://github.com/meshtastic/Meshtastic-device/releases/download/v{version}/firmware-{version}.zip'
        print(f'zip_file_url:{zip_file_url}')

        print("downloading...")
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve(zip_file_url, zip_file_name)
            print("done downloading")
        except:
            print('could not download')


def unzip_if_necessary(directory, zip_file_name):
    """Unzip the zip_file_name into the directory"""
    if not os.path.exists(directory):
        if os.path.exists(zip_file_name):
            print("Unzipping files now...")
            with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
                zip_ref.extractall(directory)
            print("done unzipping")


def check_if_newer_version():
    """Check pip to see if we are running the latest version."""
    is_newer_version = False
    pypi_version = None
    try:
        url = "https://pypi.org/pypi/meshtastic-flasher/json"
        data = requests.get(url).json()
        pypi_version = data["info"]["version"]
        print(f"pypi_version:{pypi_version}")
    except Exception as e:
        print(f"could not get version from pypi e:{e}")
    print(f'running: {meshtastic_flasher.version.__version__}')
    if pypi_version and meshtastic_flasher.version.__version__ != pypi_version:
        is_newer_version = True
    return is_newer_version


def zero_if_blank(some_input):
    """If some_input is blank, then return '0' else return a string after converting to an integer."""
    retval = 0
    if some_input is None or some_input == '':
        retval = 0
    else:
        try:
            retval = int(some_input)
        except:
            pass
    return f'{retval}'


def load_fields():
    """Get field info from json file"""
    fields = None
    with open(get_path('fields.json'), encoding='utf-8') as json_file:
        fields = json.load(json_file)
    return fields
