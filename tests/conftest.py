# Author: Milan Kubik

import copy
import pytest
import yaml

from tempfile import NamedTemporaryFile

from ipaqe_provision_hosts import paths


@pytest.fixture(scope='function')
def fake_os_release():
    """Monkey patch the paths variable OS_RELEASE"""
    content = "ID=fedora\nVERSION_ID=25\nNAME=Fedora\n"

    original = copy.copy(paths.OS_RELEASE)
    with NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(content)
        f.close()

        paths.OS_RELEASE = f.name

        yield paths.OS_RELEASE

        paths.OS_RELEASE = original
        f.unlink(f.name)


@pytest.fixture
def dummy_static_inventory(fake_os_release):
    data = {'fedora': {'25': {'domains': {}, 'hosts': {}}}}
    domains = {
            'dummy.domain.test':
                {'type': 'IPA',
                 'name': 'domain-123.domain.test'}
    }

    hosts = {
        'host_test':
        {'name': 'host-123.domain.test',
         'ip': '192.168.42.12',
         'external_hostname': 'host-123.example.com'}
    }


    data['fedora']['25']['domains'] = domains
    data['fedora']['25']['hosts'] = hosts

    with NamedTemporaryFile('w', delete=False) as f:
        yaml.safe_dump(data, f, default_flow_style=False)
        f.close()

        yield f.name

        f.unlink(f.name)
