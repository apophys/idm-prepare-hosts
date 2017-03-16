# Author: Milan Kubik

import logging

from ipaqe_provision_hosts.errors import IPAQEProvisionerError
from ipaqe_provision_hosts.utils import load_yaml, get_os_version


log = logging.getLogger(__name__)


class UnknownHostDomainError(IPAQEProvisionerError):
    pass


class StaticInventory(object):
    """Staticly configured topology resources

    The class provides an interface to a static inventory
    that can work with resources that are not managed
    by the tool.

    The format of the static inventory file must follow the
    following schema:

    The file is a yaml serialized dictionary:

        OS_ID:
            OS_VERSION:
                domains: {}
                hosts: {}

    or

        OS_ID:
            domains: {}
            hosts: {}

    The OS_VERSION key is optional and depends on its
    avilability in the os-release [1]


    [1]: https://www.freedesktop.org/software/systemd/man/os-release.html
    """

    def __init__(self, path=None, os_version=None):
        log.debug("Instantiating static inventory")
        self._inventory_path = path
        os_id, os_version = os_version or get_os_version()
        self._os_id = os_id
        self._os_version = os_version
        self._inventory = {}
        self._initialize_empty_directory(os_id, os_version)
        if path:
            log.debug("Loading static inventory from file %s", path)
            self._load_static_inventory(load_yaml(path))
        log.debug("Static inventory initialized")

    def _initialize_empty_directory(self, os_name, os_version):
        if os_version:
            log.debug("Initialized inventory for %s %s", os_name, os_version)
            inv = {os_name: {os_version: {'hosts': {}, 'domains': {}}}}
        else:
            log.debug("Initialized inventory for %s", os_name)
            inv = {os_name: {'hosts': {}, 'domains': {}}}
        self._inventory.update(inv)

    def _load_static_inventory(self, inventory):
        log.debug("Loading content of static inventory")
        self._inventory.update(inventory)

    def _get_resource_type_dict(self, dict_name):
        try:
            log.debug("Accessing inventory for %s dictionary", dict_name)
            if self._os_version:
                log.debug("Accessing %s for os %s %s",
                          dict_name, self._os_id, self._os_version)
                return (
                    self._inventory[self._os_id][self._os_version][dict_name]
                )
            else:
                log.debug("Accessing %s for os %s", dict_name, self._os_id)
                return self._inventory[self._os_id][dict_name]
        except KeyError as e:
            log.error("Malformed static inventory: %s\nFile: %s",
                      e.message, self._inventory_path)
            raise IPAQEProvisionerError

    @property
    def domains(self):
        return self._get_resource_type_dict('domains')

    @property
    def hosts(self):
        return self._get_resource_type_dict('hosts')

    def lookup_domain(self, domain_type):
        try:
            log.debug("Looking up domain with type %s", domain_type)
            return self.domains[domain_type]
        except KeyError:
            log.error("Could not find domain with type %s", domain_type)
            raise

    def lookup_host(self, role_name):
        try:
            log.debug("Looking up host with role %s", role_name)
            return self.hosts[role_name]
        except KeyError:
            log.error("Could not find host with role %s", role_name)
            raise
