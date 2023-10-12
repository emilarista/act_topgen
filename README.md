# ACT Topology Generation

This role generates ACT topology files based on AVD structured config files.

The default is to look for structured configs in ./intended/structured_configs/ and output the result to ./act/

You have to build an AVD project first and run the eos_designs role to build the structured configs before this role can be used.

## Example Playbook

Use the same top level group you have for your fabric for hosts, modify the input variables to the role to make the topology you want.

```yaml
---
- name: Build ACT Topology
  hosts: ACT_FABRIC
  connection: local
  gather_facts: false

  tasks:
    - name: Generate ACT Topology File
      import_role:
        name: act-topgen
```

## Role Defaults

```yaml
# Input/Output directories and AVD structured config file format
structured_folder: "intended/structured_configs/"
avd_structured_config_file_format: yml
output_folder: "act/"
output_filename: "topology.yml"

# Versions
act_eos_version: "4.28.1.1F"
act_generic_os_version: "Rocky-8.5"
act_cvp_version: "2022.2.2"

# Device (veos/generic) user/pass
act_device_user: "cvpadmin"
act_device_password: "arista1234"
# List other ports that all EOS devices should have.
# These cannot clash with ports already defined through the topology.
act_default_ports: []

# CVP user/pass
act_cvp_user: "root"
act_cvp_password: "cvproot"
act_cvp_instance_type: "singlenode" # Currently the only supported type
act_cvp_ip: < cvp node IP, default -> 192.168.0.5 >
act_ansible_ip: < cvp node IP, default -> 192.168.0.6 >
act_cvp_auto_configuration: < true, false , default -> true>

# Whether to add cvp and ansible node to topology
act_add_cvp: true
act_add_ansible_node: true

# Whether to add nodes that are not defined in the fabric
# Example l3 peers, servers and other endpoints
act_add_connected_nodes: false
# For each peer_type that should be added,
# the ACT node_type needs to be defined
# Any peer_type that is not defined in this list
# will not be added as a node in the topology
act_connected_nodes_map:
  other: 'veos'
  # server: 'generic'
  # network_port: 'generic'
  # <peer_type in AVD>: <node_type in ACT>

# Range for assigning OOB IP addresses to connected nodes.
act_connected_nodes_range: 192.168.0.128/25

# Use older style ACT topology connections (nodes[].neighbors)
act_use_old_connections: false
```
