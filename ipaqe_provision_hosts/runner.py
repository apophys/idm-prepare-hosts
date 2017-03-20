# Author: Milan Kubik

import logging
import yaml

from ipaqe_provision_hosts.utils import load_config, load_topology
from ipaqe_provision_hosts.errors import IPAQEProvisionerError
from ipaqe_provision_hosts.backend.loader import load_backends
from ipaqe_provision_hosts.static_inventory import StaticInventory
from ipaqe_provision_hosts.topology_manager import TopologyInventory

from ipaqe_provision_hosts import paths

log = logging.getLogger(__name__)


def create(topology, config, output):
    """Initialize backend and prepare configuration

    The function takes the parsed parameters and initializes
    and uses the configured backend.
    """

    log.debug("Running the create command")

    try:
        # Load configuration files
        config = load_config(config)
        topology_template = load_topology(topology)

        # Initialize backend map
        backends = load_backends()

        # Prepare relevant parts of configuration
        # Instantiate backend according to configuration
        try:
            b_config = config['backend']
            backend = backends[b_config['name']](b_config['config'])
        except KeyError as e:
            log.error(
                "Problem accessing backend configuration "
                "or instantiating a backend")
            raise IPAQEProvisionerError

        log.debug("Retrieving static inventory file path")
        static_resources_path = (
            config['core'].get('static_resources',
                               paths.DEFAULT_STATIC_INVENTORY)
        )
        static_resources_os_version = (
            config['core'].get('os_version')
        )
        static_inventory = StaticInventory(
            static_resources_path, os_version=static_resources_os_version)

        # Instantiate the TopologyManager
        inventory = TopologyInventory(backend, static_inventory)

        dns_forwarder, provisioned_domains = (
            inventory.provision_topology(topology_template))
        config['domain_settings']['dns_forwarder'] = dns_forwarder

        multihost_config = {}

        multihost_config['domains'] = provisioned_domains
        multihost_config.update(config['domain_settings'])

        with open(output, mode='w') as f:
            log.debug("Writing the configuration file to %s", output)
            yaml.safe_dump(multihost_config, f, default_flow_style=False)

    except IPAQEProvisionerError as e:
        log.debug("Aborting create call: %s", e.message)
        raise


def delete(config):
    """Dispose of the resources

    The function instantiates the backend class
    and requests to remove any provisioned resources.

    The backend itself is responsible for managing caches.
    """
    log.debug("Running the delete command")

    try:
        # Load configuration files
        config = load_config(config)
        # Initialize backend map
        backends = load_backends()

        # Prepare relevant parts of configuration
        # Instantiate backend according to configuration
        try:
            b_config = config['backend']
            backend = backends[b_config['name']](b_config['config'])
        except KeyError as e:
            log.error(
                "Problem accessing backend configuration "
                "or instantiating a backend")
            raise IPAQEProvisionerError

        backend.delete_resources()

    except IPAQEProvisionerError as e:
        log.debug("Aborting delete call: %s", e.message)
        raise
