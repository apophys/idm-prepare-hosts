# idm-prepare-hosts
Command line utility for FreeIPA multihost environment preparation

A wrapper script to allow integration with FreeIPA upstream CI
as defined in [the upstream ci repository][upstream-ci].


## Dependencies

See requirements.txt

## Usage

The script reads a topology template specifying a domain for
the ipa installation.

```
domains:
  - hosts:
      - name: master.ipa.test
        role: master
      - name: replica.ipa.test
        role: replica
      - name: replica.ipa.test
        role: replica
    name: ipa.test
    type: IPA

```

The domain specifies a number of hosts, each assigned a role in the topology.
The type of domain is specific to a test.


[upstream-ci]: https://github.com/freeipa/freeipa-ci
