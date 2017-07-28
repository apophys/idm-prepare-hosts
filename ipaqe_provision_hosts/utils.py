# Author: Milan Kubik

import logging
import yaml

from ipaqe_provision_hosts.errors import IPAQEProvisionerError
from ipaqe_provision_hosts import paths

log = logging.getLogger(__name__)


class ConfigLoadError(IPAQEProvisionerError):
    pass


def load_yaml(path, logger=None):
    _log = logger or log
    try:
        with open(path, mode='r') as f:
            return yaml.load(f)
    except OSError:
        _log.error('Error reading file %s', path)
        raise ConfigLoadError
    except yaml.YAMLError as e:
        _log.error("YAML error:\n%s", e)
        raise ConfigLoadError


def load_config(path=None, logger=None):
    """Load configuration

    The configuration is loaded from the given path
    or from the default path in /etc.
    """
    _log = logger or log
    path = path or paths.SYSTEM_CONFIG_PATH

    _log.info("Loading configuration file %s", path)
    return load_yaml(path)


def load_topology(path, logger=None):
    """Load the topology file"""
    _log = logger or log
    _log.info("Loading topology file %s", path)
    return load_yaml(path)


def get_os_version(logger=None):
    """Get the OS version from /etc/os-release

    The function returns pair (ID, VERSION_ID).
    If the OS does not have VERSION_ID, it will be None
    """
    _log = logger or log

    try:
        _log.debug('Reading os-release')
        with open(paths.OS_RELEASE) as f:
            os_release = dict([
                line.strip().split('=')
                for line in f.readlines() if line.strip()
            ])
        os_id, os_ver = os_release['ID'], os_release.get('VERSION_ID')
        if os_ver:
            _log.debug("Detected OS %s %s", os_id, os_ver)
        else:
            _log.debug("Detected OS %s", os_id)

        return os_id, os_ver
    except IOError:
        _log.error('The file %s was not found.', paths.OS_RELEASE)
        raise IPAQEProvisionerError
    except KeyError:
        _log.error("The key ID of os-release was not found.")
        raise IPAQEProvisionerError
