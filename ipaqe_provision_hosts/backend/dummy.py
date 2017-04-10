# Author: Milan Kubik

import logging

from ipaqe_provision_hosts.backend.base import IDMBackendBase

log = logging.getLogger(__name__)


class DummyBackend(IDMBackendBase):

    def __init__(self, config=None):
        log.debug("Instantiating DummyBackend")
        super(DummyBackend, self).__init__(config)

    def provision_resources(self, n):
        log.debug("Generating %d dummy hosts", n)
        data = {
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

        self._vms = data

        return data

    def delete_resources(self):
        log.debug("DummyBackend.delete_resources called")
        return True
