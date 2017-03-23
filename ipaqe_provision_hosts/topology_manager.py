# Author: Milan Kubik

import logging

from ipaqe_provision_hosts import errors
from ipaqe_provision_hosts.backend.base import IDMBackendBase
from ipaqe_provision_hosts.static_inventory import (
    StaticInventory, UnknownHostDomainError)


log = logging.getLogger(__name__)


class TopologyInventoryError(errors.IPAQEProvisionerError):
    pass


class TopologyInventory(object):
    """The topology inventory

    The class manages the dynamic and static
    inventories and provides an interface for
    assigning resources to provided topology template.
    """
    MANAGED_DOMAINS = ('IPA',)
    MANAGED_ROLES = ('master', 'replica', 'client', 'other')

    def __init__(self, dynamic_backend, static_inventory=None):
        log.debug("Initializing TopologyInventory")
        self._dynamic_backend = dynamic_backend
        if not isinstance(self._dynamic_backend, IDMBackendBase):
            raise TopologyInventoryError(
                "Cannot create inventory, %r is not an instance of %r",
                dynamic_backend, IDMBackendBase)
        log.debug("Using backend %r", dynamic_backend.__class__)

        self._static_inventory = static_inventory or StaticInventory()
        if not isinstance(self._static_inventory, StaticInventory):
            raise TopologyInventoryError(
                "Cannot create inventory, %r is not an instance of %r",
                static_inventory, StaticInventory)

    def provision_topology(self, topology_template):
        """Provision topology based on a topology template

        The function takes a topology template and builds
        a topology dictionary by calling the backend and
        retrieving resources for managed domain types
        or looging up resources in the static inventory.

        At first, staticly configured domains are processed.
        If errors happen during static domain processing,
        dynamic backend is not called, saving time and resources.
        """

        provisioned_domains = []

        dynamic_domains_to_process = []

        log.debug("Processing the topology template")
        for domain in topology_template['domains']:
            log.debug('Found domain of type %s', domain['type'])
            if domain['type'] in self.MANAGED_DOMAINS:
                log.debug('Managed domain %s of type %s found, adding to queue',
                          domain['name'], domain['type'])
                dynamic_domains_to_process.append(domain)
            else:
                log.debug("Processing unmanaged domain %s", domain['type'])
                d = self._process_non_managed_domain(domain)
                provisioned_domains.append(d)

        # Count hosts required for managed domains
        required_hosts = sum(
            len(domain['hosts']) for domain in dynamic_domains_to_process)
        log.debug("Requesting %d hosts from the dynamic backend.",
                  required_hosts)

        try:
            backend_data = (
                self._dynamic_backend.provision_resources(required_hosts))
            dns_forwarder = backend_data['dns']
            log.debug("Backends DNS forwarder is %s", dns_forwarder)
            host_pool = backend_data['hosts']
        except (KeyError, TypeError) as e:
            log.error("Malformed data from the backend.\n%s", e)
            raise errors.IPAQEProvisionerError

        self._validate_domain_hint(host_pool)

        log.debug("Processing managed domains")
        for domain in dynamic_domains_to_process:
            dom_hosts_count = len(domain['hosts'])
            dom_hosts = host_pool[:dom_hosts_count]
            host_pool = host_pool[dom_hosts_count:]

            log.debug("Assigning hosts to domain %s", domain['name'])
            self._assign_hosts_to_domain(domain, dom_hosts)
            provisioned_domains.append(domain)

        return dns_forwarder, provisioned_domains

    def _process_non_managed_domain(self, domain):
        log.debug("Processing domain of type %s", domain['type'])
        dom = self._static_inventory.lookup_domain(domain['type'])
        dom['hosts'] = []

        log.debug("Processing %d hosts in the domain",
                  len(domain['hosts']))
        for host in domain['hosts']:
            if host['role'] in self.MANAGED_ROLES:
                log.error("Static domains can only be composed"
                          " of statically defined resources.")
                raise TopologyInventoryError
            else:
                try:
                    h = self._static_inventory.lookup_host(host['role'])
                    dom['hosts'].append(h)
                except UnknownHostDomainError:
                    log.error(
                        "Host of role %s was not found "
                        "in static inventory",
                        host['role'])
                    raise errors.IPAQEProvisionerError

        return dom

    @staticmethod
    def _validate_domain_hint(hosts):
        log.debug("Validating domain_hint for hosts")
        if not all('domain_hint' in host for host in hosts):
            log.error("Not all dynamically provisioned hosts "
                      "provide domain hint value.")
            raise TopologyInventoryError

    @staticmethod
    def _assign_hosts_to_domain(domain, hosts):
        for dom_host in domain['hosts']:
            dom_host.update(hosts.pop())
            if dom_host['role'] == 'master':
                domain['name'] = dom_host['domain_hint']
                log.debug("Assigning domain a name %s", domain['name'])
            dom_host.pop('domain_hint')
