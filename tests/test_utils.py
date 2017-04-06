# Author: Milan Kubik

from ipaqe_provision_hosts.utils import get_os_version


def test_get_os_version(fake_os_release):

    os_id, os_version = get_os_version()

    assert os_id == 'fedora'
    assert os_version == '25'
