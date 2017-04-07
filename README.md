# ipaqe-provision-hosts
Command line utility for FreeIPA multihost environment preparation

A wrapper script to allow integration with FreeIPA upstream CI
as defined in [the upstream ci repository][upstream-ci].


## Dependencies

See requirements.txt and setup.py

## Usage

The script reads a topology template specifying a domain for
the ipa installation and creating a configuration file for
[the multihost tests][ipa-int-tests] with the provisioned resources.

```yaml
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

```yaml
domains:
  - hosts:
      - name: master.ipa.test
        role: trust_master
    name: ipa.test
    type: TRUST_IPA
  - hosts:
      - name: ad.ad.test
        role: ad
      - name: child.child.ad.test
        role: ad_subdomain
      - name: tree.treedomain.ad.test
        role: ad_treedomain
    name: ad.test
    type: AD
```

The domain specifies a number of hosts, each assigned a role in the topology.
The type of domain is specific to a test.

Managed roles and domain types (master, replica, client; IPA domain) are provisioned by a configured backend.
Roles that are not recognized as managed are searched for in a static inventory.


## Configuration

### Main configuration

The configuration file is a simple yaml file.
There are three sections (keys) in the file (all mandatory):

**core** contains configuration of the tool itself.
Options:
Both options are optional

* static_resources -- path to static inventory (defaults to /etc/ipaqe-provision-hosts/static-domains.yaml)
* os_version -- tuple/list containing os name and version for static inventory

os_version is a tuple coresponding to ID and VERSION_ID keys of [os-release][os-release]
If the distribution does not have version (such as rolling updates distributions), use null value

**domain_settings** contains values for FreeIPA integration tests. The values here are directly applied onto
the resulting configuration file.

**backend** configures the backend specified by its name. The configuretion is passed
via the `config` key. The configuretion is backend specific.

#### Example configuration

```yaml
# The core key settings
core:
    # Set up path to staticly configured domains and hosts

    static_resources: /path/with/static/resources
    # os_version is a tuple with os-release values for
    # ID and ID_VERSION
    # if ID_VERSION is unavailable, use null value
    os_version: ['fedora', '25']

domain_settings:
    # All commented settings are as defaults used
    # in freeipa integration tests. Override needed ones.
    #
    #

    # admin_name: admin
    # admin_password: Secret123
    # dirman_name: cn=Directory Manager
    # dirman_password: Secret123
    # nisdomain: ipatest
    # ntp_server: 0.pool.ntp.org
    # ad_admin_name: Administrator
    # ad_admin_password: Secret123
    # domain_level: 1
    dns_forwarder: 8.8.8.8
    root_ssh_key_filename: /path/to/private/ssh/key


backend:
    # Backend specific configuration
    name: dummy
    config:
        url: http://example.com/api
        username: demo
        password: secret

```

### Static inventory

For non-managed resources there exists a concept of a static inventory.
When the tool finds a domain of non-managed type, a resolution in static
inventory is made. The exact format of the inventory is dependent on the
operation system version of the statically configured resources.

A static inventory is a dictionary with a schema:

```yaml
{"id": {"version_id": { "hosts": {}, "domains": {}}}}
```

or

```yaml
{"id": { "hosts": {}, "domains": {}}}
```

depending on availability of `ID_VERSION` in the particular distribution.
Keys correspond to ID and VERSION_ID option of [os release][os-release].

#### Static domain definition

A static domain is defined by its `TYPE` option (key)

```yaml
fedora:
    '25':
        domains:
            AD_TREE:
                name: dom-123.ad.example.com
                type: AD
```


#### Static host definition

Similar to a domain, a host in static inventory is accessed via
its role. This role must be unique in the inventory.

```yaml
fedora:
    '25':
        hosts:
            trust_master:
                ip: 192.168.1.10
                name: vm-010.private.example.com.
                external_hostname: vm-010.routable.example.com
                type: master
```


## Backend modules

The main purpose of the tool is to provide an api for managing resources in
some virtualization deployment. To allow to integrate with various types
of virtualization and specific deployments, the tool is designed as modular.

The actual work of dynamically providing resources is not done in the core
utility itself but in a `backend module`.

The backend module is a subclass of `ipaqe_provision_hosts.backend.base.IDMBackendBase`
class.

The backend module is required to implement the two methods `provision_resources` and
`delete_resources` and register itself as an entry point in the `ipaqe_provision_hosts.backends`
resource group via python setuptools.

### Data format of backend module

The `provision_resources` method is required to return a dictionary with a list of host entries.
Each host entry is required to have a `name` corresponding to a hostname used in the topology,
`domain_hint` specifying the domain delegated to the resource and optionally `external_hostname`,
if the `name` exists in an isolated network (e.g. openstack with private subnet).

The `domain_hint` option is **required** and should use the name of a domain delegated to a resource that will host the
domain controller (master server) by the forwarder configured for the test run.
More on [DNS configuration for IPA][ipa-dns].

```json
{"hosts":
    [
        {
            "name": "vm-123.domain.example.com",
            "ip": "192.168.42.12",
            "external_hostname": "vm-123.external.domain.example.com",
            "domain_hint": "dom-123.domain.example.com"
        }
    ]
}
```

[ipa-dns]: http://www.freeipa.org/page/DNS
[ipa-int-tests]: http://www.freeipa.org/page/Integration_testing_configuration
[os-release]: https://www.freedesktop.org/software/systemd/man/os-release.html
[upstream-ci]: https://github.com/freeipa/freeipa-ci
