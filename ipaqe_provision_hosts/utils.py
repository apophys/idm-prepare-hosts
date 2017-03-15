# Author: Milan Kubik

import logging
import yaml

from ipaqe_provision_hosts.errors import IPAQEProvisionerError

log = logging.getLogger(__name__)


class ConfigLoadError(IPAQEProvisionerError):
    pass


def load_yaml(path):
    try:
        with open(path, mode='r') as f:
            return yaml.load(f)
    except OSError:
        log.error('Error reading file %s', path)
        raise ConfigLoadError
    except yaml.YAMLError as e:
        log.error("YAML error:\n%s", e)
        raise ConfigLoadError


def load_config(path=None):
    """Load configuration

    The configuration is loaded from the given path
    or from the default path in /etc.
    """

    etc_path = '/etc/ipaqe-provision-hosts/config.yaml'

    path = path or etc_path

    log.info("Loading configuration file %s", path)
    return load_yaml(path)


def load_topology(path):
    """Load the topology file"""
    log.info("Loading topology file %s", path)
    return load_yaml(path)
