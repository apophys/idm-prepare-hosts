# Author: Milan Kubik

import pytest

from ipaqe_provision_hosts.static_inventory import (
    StaticInventory, UnknownHostDomainError)

class TestStaticInventory(object):

    def test_empty_directory(self):
        inv = StaticInventory()

        assert isinstance(inv.hosts, dict)
        assert isinstance(inv.domains, dict)

    def test_empty_direcory_os_version(self, fake_os_release):
        inv = StaticInventory()

        assert 'fedora' in inv._inventory
        assert '25' in inv._inventory['fedora']

    def test_inventory_lookup(self, dummy_static_inventory):
        inv = StaticInventory(dummy_static_inventory)

        dom = inv.lookup_domain('dummy.domain.test')
        host = inv.lookup_host('host_test')

    def test_failed_inventory_lookup(self, dummy_static_inventory):
        inv = StaticInventory(dummy_static_inventory)

        with pytest.raises(KeyError):
            inv.lookup_domain('foo')

        with pytest.raises(KeyError):
            inv.lookup_host('bar')
