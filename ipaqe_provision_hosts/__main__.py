#!/usr/bin/env python

from __future__ import print_function

import argparse
import logging
import sys

from ipaqe_provision_hosts.runner import create, delete
from ipaqe_provision_hosts.errors import IPAQEProvisionerError


CONFIG_HELP_MSG = (
    'Configuration file for the topology. Must contain core configuration as '
    ' well as configuration for backend. If not specified, the tool checks '
    'the configuration from /etc/ipaqe-provision-hosts/config.yaml')


def main():
    parser = argparse.ArgumentParser(description='FreeIPA provisioning')
    parser.add_argument('-d', '--debug', dest='loglevel',
                        help='Set logging level. Default level is ERROR',
                        metavar='LEVEL')

    subparsers = parser.add_subparsers(dest="command")

    parser_create = subparsers.add_parser("create")
    parser_create.add_argument("--topology", required=True, metavar='FILE',
                               help="The topology template file")
    parser_create.add_argument("--output", required=True, metavar='FILE',
                               help="File to print final configuration into")
    parser_create.add_argument("--config", required=False, metavar='FILE',
                               help=CONFIG_HELP_MSG)

    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument("--config", required=False, metavar='FILE',
                               help=CONFIG_HELP_MSG)

    args = parser.parse_args()

    loglevel = None
    if args.loglevel:
        try:
            loglevel = getattr(logging, args.loglevel.upper())
        except AttributeError:
            loglevel = logging.ERROR
        finally:
            logging.basicConfig(level=loglevel)

    log = logging.getLogger(__name__)
    log.debug('Setting log level to {}'.format(logging.getLevelName(loglevel)))

    try:
        if args.command == "create":
            create(args.topology, args.config, args.output)
        elif args.command == "delete":
            delete()
    except IPAQEProvisionerError:
        # Backend exception should be handled by now
        sys.exit(1)
    except Exception as e:
        log.error("Unhandled exception: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
