# author: Milan Kubik
""" Backend base class

The class provides the contract for backend modules
implementing the provisioning of dynamic resources.
"""

from ipaqe_provision_hosts.errors import IPAQEProvisionerError

NOT_IMPLEMENTED_MSG = "You need to override this method in a subclass"


class VMsNotCreatedError(IPAQEProvisionerError):
    """Raise in case VMs could not be provisioned"""
    pass


class IDMBackendBase(object):
    """IDMBackendBase class

       This class represents a contract between the
       idm-prepare-hosts utility and a backend implementation.
    """
    def __init__(self, config=None):
        self._config = config or {}
        self._vms = []

    @property
    def vms(self):
        """The attribute returns a list of host entries"""

        if not self._vms:
            raise VMsNotCreatedError("No VMs were provisioned yet")
        else:
            return self._vms

    def provision_resources(self, vm_count):
        """Provision the hosts in a backend"""
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    def delete_resources(self):
        """Delete the resources provisioned by the backend"""
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
