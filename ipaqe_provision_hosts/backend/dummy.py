# Author: Milan Kubik

import logging

from ipaqe_provision_hosts.backend.base import IDMBackendBase

log = logging.getLogger(__name__)


class DummyBackend(IDMBackendBase):

    def __init__(self, config):
        log.debug("Instantiating DummyBackend")

    def provision_resources(self, n):
        log.debug("Generating %d dummy hosts", n)
        data = {
            'dns': '8.8.8.8',
            'hosts': [
                {
                    'name':
                    'dummy-host-{index:03d}.example.com'.format(index=i),
                    'domain_hint':
                    'dummy-domain-{index:03d}.example.com'.format(index=i),
                }
                for i in range(n)
            ]
        }

        return data

    def delete_resources(self):
        log.debug("DummyBackend.delete_resources called")
        return True
