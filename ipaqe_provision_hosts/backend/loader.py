# Author: Milan Kubik, 2017

import logging

from pkg_resources import iter_entry_points

RESOURCE_GROUP = "ipaqe_provision_hosts.backends"

log = logging.getLogger(__name__)


def load_backends(exclude=()):
    log.debug("Loading entry points from %s.", RESOURCE_GROUP)
    entry_points = {
        ep.name: ep.load() for ep in iter_entry_points(RESOURCE_GROUP)
        if ep.name not in exclude
    }
    return entry_points
