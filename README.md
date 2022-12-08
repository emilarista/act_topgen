# ACT Topology Generation

This role generates ACT topology files based on AVD structured config files.

The default is to look for structured configs in ./intended/structured_configs/ and output the result to ./act/

You have to build an AVD project first and run the eos_designs role to build the structured configs before this role can be used.

## Example Playbook

Use the same top level group you have for your fabric for hosts, modify the input variables to the role to make the topology you want.

```yaml
---
- name: Build Switch configuration
  hosts: MPLS_FABRIC
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

# Versions
act_eos_version: "4.27.6M"
act_generic_os_version: "Rocky-8.5"
act_cvp_version: "2022.2.0"

# Device (veos/generic) user/pass
act_device_user: "cvpadmin"
act_device_password: "arista1234"

# CVP user/pass
act_cvp_user: "root"
act_cvp_password: "cvproot"
act_cvp_instance_type: "singlenode" # Currently the only supported type
act_cvp_ip: < cvp node IP, default -> 192.168.0.5 >
act_ansible_ip: < cvp node IP, default -> 192.168.0.6 >

# Whether to add cvp and ansible node to topology
act_add_cvp: true
act_add_ansible_node: true
```
