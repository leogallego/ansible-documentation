# Building an inventory

Inventories organize managed nodes in centralized files that provide Ansible with system information and network locations. Using an inventory file, Ansible can manage a large number of hosts with a single command.

To complete the following steps, you will need the IP address or fully qualified domain name (FQDN) of at least one host system. For demonstration purposes, the host could be running locally in a container or a virtual machine. You must also ensure that your public SSH key is added to the `authorized_keys` file on each host.

Continue getting started with Ansible and build an inventory as follows:

1.  Create a file named `inventory.ini` in the `ansible_quickstart` directory that you created in the preceding step.

2.  Add a new `[myhosts]` group to the `inventory.ini` file and specify the IP address or fully qualified domain name (FQDN) of each host system.

    ``` ini
    [myhosts]
    192.0.2.50
    192.0.2.51
    192.0.2.52
    ```

3.  Verify your inventory.

    ``` bash
    ansible-inventory -i inventory.ini --list
    ```

4.  Ping the `myhosts` group in your inventory.

    ``` bash
    ansible myhosts -m ping -i inventory.ini
    ```

    

    Pass the `-u` option with the `ansible` command if the username is different on the control node and the managed node(s).

    

    

Congratulations, you have successfully built an inventory. Continue getting started with Ansible by creating a playbook.

## Inventories in INI or YAML format

You can create inventories in either `INI` files or in `YAML`. In most cases, such as the example in the preceding steps, `INI` files are straightforward and easy to read for a small number of managed nodes.

Creating an inventory in `YAML` format becomes a sensible option as the number of managed nodes increases. For example, the following is an equivalent of the `inventory.ini` that declares unique names for managed nodes and uses the `ansible_host` field:

## Tips for building inventories

- Ensure that group names are meaningful and unique. Group names are also case sensitive.
- Avoid spaces, hyphens, and preceding numbers (use `floor_19`, not `19th_floor`) in group names.
- Group hosts in your inventory logically according to their **What**, **Where**, and **When**.
  What  
  Group hosts according to the topology, for example: db, web, leaf, spine.

  Where  
  Group hosts by geographic location, for example: datacenter, region, floor, building.

  When  
  Group hosts by stage, for example: development, test, staging, production.

### Use metagroups

Create a metagroup that organizes multiple groups in your inventory with the following syntax:

``` yaml
metagroupname:
  children:
```

The following inventory illustrates a basic structure for a data center. This example inventory contains a `network` metagroup that includes all network devices and a `datacenter` metagroup that includes the `network` group and all webservers.

### Create variables

Variables set values for managed nodes, such as the IP address, FQDN, operating system, and SSH user, so you do not need to pass them when running Ansible commands.

Variables can apply to specific hosts.

Variables can also apply to all hosts in a group.

