# Author: Milan Kubik

import logging


log = logging.getLogger(__name__)

def create(topology, config, output):
    """Initialize backend and prepare configuration

    The function takes the parsed parameters and initializes
    and uses the configured backend.
    """

    pass


def delete(config):
    """Dispose of the resources

    The function instantiates the backend class
    and requests to remove any provisioned resources.

    The backend itself is responsible for managing caches.
    """
    pass
