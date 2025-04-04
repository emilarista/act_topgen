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
---
# defaults file for act-topgen

# Input/Output directories and AVD structured config file format
structured_folder: "intended/structured_configs/"
avd_structured_config_file_format: yml
output_folder: "act/"
output_filename: "topology.yml"

# Versions
act_eos_version: "4.30.4M"
act_generic_os_version: "Rocky-8.5"
act_tools_os_version: "ubuntu-2204-lts"
act_cvp_version: "2023.1.3"

# Device (veos/generic) user/pass
act_device_user: <some user>
act_device_password: <some password>
# List other ports that all EOS devices should have.
# These cannot clash with ports already defined through the topology.
act_default_ports: []
# Adds device models from structured config metadata if present
act_use_device_models: true

# Extra node parameters
act_cvp_user: <some user>
act_cvp_password: <some password>
act_cvp_instance_type: "singlenode"  # Currently the only supported type
act_cvp_ip: "192.168.0.5"
act_cvp_auto_configuration: true
act_cvp_size: medium # supported values are medium, large, xlarge
act_tools_server_ip: "192.168.0.6"
act_tools_server_size: medium # supported values are medium, large, xlarge
act_veos_size: medium # supported values are medium, large, xlarge

# Whether to add cvp and ansible node to topology
act_add_cvp: true
act_add_tools_server: true

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

act_connected_nodes_range: 192.168.0.128/25

# # Extra nodes to add
# act_additional_nodes: []

# Use older style ACT topology connections (nodes[].neighbors)
act_use_old_connections: false
```
