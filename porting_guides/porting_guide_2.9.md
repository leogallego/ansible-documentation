# Ansible 2.9 Porting Guide

This section discusses the behavioral changes between Ansible 2.8 and Ansible 2.9.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with [Ansible Changelog for 2.9](https://github.com/ansible/ansible/blob/stable-2.9/changelogs/CHANGELOG-v2.9.rst) to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at porting guides.

## Playbook

### Inventory

> - `hash_behaviour` now affects inventory sources. If you have it set to `merge`, the data you get from inventory might change and you will have to update playbooks accordingly. If you're using the default setting (`overwrite`), you will see no changes. Inventory was ignoring this setting.

### Loops

Ansible 2.9 handles "unsafe" data more robustly, ensuring that data marked "unsafe" is not templated. In previous versions, Ansible recursively marked all data returned by the direct use of `lookup()` as "unsafe", but only marked structured data returned by indirect lookups using `with_X` style loops as "unsafe" if the returned elements were strings. Ansible 2.9 treats these two approaches consistently.

As a result, if you use `with_dict` to return keys with templatable values, your templates may no longer work as expected in Ansible 2.9.

To allow the old behavior, switch from using `with_X` to using `loop` with a filter as described at migrating_to_loop.

## Command Line

- The location of the Galaxy token file has changed from `~/.ansible_galaxy` to `~/.ansible/galaxy_token`. You can configure both path and file name with the galaxy_token_path config.

## Deprecated

No notable changes

## Collection loader changes

The way to import a PowerShell or C# module util from a collection has changed in the Ansible 2.9 release. In Ansible 2.8 a util was imported with the following syntax:

``` powershell
#AnsibleRequires -CSharpUtil AnsibleCollections.namespace_name.collection_name.util_filename
#AnsibleRequires -PowerShell AnsibleCollections.namespace_name.collection_name.util_filename
```

In Ansible 2.9 this was changed to:

``` powershell
#AnsibleRequires -CSharpUtil ansible_collections.namespace_name.collection_name.plugins.module_utils.util_filename
#AnsibleRequires -PowerShell ansible_collections.namespace_name.collection_name.plugins.module_utils.util_filename
```

The change in the collection import name also requires any C# util namespaces to be updated with the newer name format. This is more verbose but is designed to make sure we avoid plugin name conflicts across separate plugin types and to standardise how imports work in PowerShell with how Python modules work.

## Modules

- The `win_get_url` and `win_uri` module now sends requests with a default `User-Agent` of `ansible-httpget`. This can be changed by using the `http_agent` key.
- The `apt` module now honors `update_cache=false` while installing its own dependency and skips the cache update. Explicitly setting `update_cache=true` or omitting the param `update_cache` will result in a cache update while installing its own dependency.
- Version 2.9.12 of Ansible changed the default mode of file-based tasks to `0o600 & ~umask` when the user did not specify a `mode` parameter on file-based tasks. This was in response to a CVE report which we have reconsidered. As a result, the mode change has been reverted in 2.9.13, and mode will now default to `0o666 & ~umask` as in previous versions of Ansible.
- If you changed any tasks to specify less restrictive permissions while using 2.9.12, those changes will be unnecessary (but will do no harm) in 2.9.13.
- To avoid the issue raised in CVE-2020-1736, specify a `mode` parameter in all file-based tasks that accept it.
- `dnf` and `yum` - As of version 2.9.13, the `dnf` module (and `yum` action when it uses `dnf`) now correctly validates GPG signatures of packages (CVE-2020-14365). If you see an error such as `Failed to validate GPG signature for [package name]`, please ensure that you have imported the correct GPG key for the DNF repository and/or package you are using. One way to do this is with the `rpm_key` module. Although we discourage it, in some cases it may be necessary to disable the GPG check. This can be done by explicitly adding `disable_gpg_check: yes` in your `dnf` or `yum` task.

### Renaming from `_facts` to `_info`

Ansible 2.9 renamed a lot of modules from `<something>_facts` to `<something>_info`, because the modules do not return Ansible facts. Ansible facts relate to a specific host. For example, the configuration of a network interface, the operating system on a unix server, and the list of packages installed on a Windows box are all Ansible facts. The renamed modules return values that are not unique to the host. For example, account information or region data for a cloud provider. Renaming these modules should provide more clarity about the types of return values each set of modules offers.

### Writing modules

- Module and module_utils files can now use relative imports to include other module_utils files. This is useful for shortening long import lines, especially in collections.

  Example of using a relative import in collections:

  ``` python
  # File: ansible_collections/my_namespace/my_collection/plugins/modules/my_module.py
  # Old way to use an absolute import to import module_utils from the collection:
  from ansible_collections.my_namespace.my_collection.plugins.module_utils import my_util
  # New way using a relative import:
  from ..module_utils import my_util
  ```

  Modules and module_utils shipped with Ansible can use relative imports as well but the savings are smaller:

  ``` python
  # File: ansible/modules/system/ping.py
  # Old way to use an absolute import to import module_utils from core:
  from ansible.module_utils.basic import AnsibleModule
  # New way using a relative import:
  from ...module_utils.basic import AnsibleModule
  ```

  Each single dot (`.`) represents one level of the tree (equivalent to `../` in filesystem relative links).

  

### Modules removed

The following modules no longer exist:

- Apstra's `aos_*` modules. See the new modules at <https://github.com/apstra>.
- ec2_ami_find use ec2_ami_facts instead.
- kubernetes use k8s instead.
- nxos_ip_interface use nxos_l3_interface instead.
- nxos_portchannel use nxos_linkagg instead.
- nxos_switchport use nxos_l2_interface instead.
- oc use k8s instead.
- panos_nat_policy use panos_nat_rule instead.
- panos_security_policy use panos_security_rule instead.
- vsphere_guest use vmware_guest instead.

### Deprecation notices

The following modules will be removed in Ansible 2.13. Please update update your playbooks accordingly.

- cs_instance_facts use cs_instance_info instead.
- cs_zone_facts use cs_zone_info instead.
- digital_ocean_sshkey_facts use digital_ocean_sshkey_info instead.
- eos_interface use eos_interfaces instead.
- eos_l2_interface use eos_l2_interfaces instead.
- eos_l3_interface use eos_l3_interfaces instead.
- eos_linkagg use eos_lag_interfaces instead.
- eos_lldp_interface use eos_lldp_interfaces instead.
- eos_vlan use eos_vlans instead.
- ios_interface use ios_interfaces instead.
- ios_l2_interface use ios_l2_interfaces instead.
- ios_l3_interface use ios_l3_interfaces instead.
- ios_vlan use ios_vlans instead.
- iosxr_interface use iosxr_interfaces instead.
- junos_interface use junos_interfaces instead.
- junos_l2_interface use junos_l2_interfaces instead.
- junos_l3_interface use junos_l3_interfaces instead.
- junos_linkagg use junos_lag_interfaces instead.
- junos_lldp use junos_lldp_global instead.
- junos_lldp_interface use junos_lldp_interfaces instead.
- junos_vlan use junos_vlans instead.
- lambda_facts use lambda_info instead.
- na_ontap_gather_facts use na_ontap_info instead.
- net_banner use the platform-specific [\[netos\]]()banner modules instead.
- net_interface use the new platform-specific [\[netos\]]()interfaces modules instead.
- net_l2_interface use the new platform-specific [\[netos\]]()l2_interfaces modules instead.
- net_l3_interface use the new platform-specific [\[netos\]]()l3_interfaces modules instead.
- net_linkagg use the new platform-specific [\[netos\]]()lag modules instead.
- net_lldp use the new platform-specific [\[netos\]]()lldp_global modules instead.
- net_lldp_interface use the new platform-specific [\[netos\]]()lldp_interfaces modules instead.
- net_logging use the platform-specific [\[netos\]]()logging modules instead.
- net_static_route use the platform-specific [\[netos\]]()static_route modules instead.
- net_system use the platform-specific [\[netos\]]()system modules instead.
- net_user use the platform-specific [\[netos\]]()user modules instead.
- net_vlan use the new platform-specific [\[netos\]]()vlans modules instead.
- net_vrf use the platform-specific [\[netos\]]()vrf modules instead.
- nginx_status_facts use nginx_status_info instead.
- nxos_interface use nxos_interfaces instead.
- nxos_l2_interface use nxos_l2_interfaces instead.
- nxos_l3_interface use nxos_l3_interfaces instead.
- nxos_linkagg use nxos_lag_interfaces instead.
- nxos_vlan use nxos_vlans instead.
- online_server_facts use online_server_info instead.
- online_user_facts use online_user_info instead.
- purefa_facts use purefa_info instead.
- purefb_facts use purefb_info instead.
- scaleway_image_facts use scaleway_image_info instead.
- scaleway_ip_facts use scaleway_ip_info instead.
- scaleway_organization_facts use scaleway_organization_info instead.
- scaleway_security_group_facts use scaleway_security_group_info instead.
- scaleway_server_facts use scaleway_server_info instead.
- scaleway_snapshot_facts use scaleway_snapshot_info instead.
- scaleway_volume_facts use scaleway_volume_info instead.
- vcenter_extension_facts use vcenter_extension_info instead.
- vmware_about_facts use vmware_about_info instead.
- vmware_category_facts use vmware_category_info instead.
- vmware_drs_group_facts use vmware_drs_group_info instead.
- vmware_drs_rule_facts use vmware_drs_rule_info instead.
- vmware_dvs_portgroup_facts use vmware_dvs_portgroup_info instead.
- vmware_guest_boot_facts use vmware_guest_boot_info instead.
- vmware_guest_customization_facts use vmware_guest_customization_info instead.
- vmware_guest_disk_facts use vmware_guest_disk_info instead.
- vmware_host_capability_facts use vmware_host_capability_info instead.
- vmware_host_config_facts use vmware_host_config_info instead.
- vmware_host_dns_facts use vmware_host_dns_info instead.
- vmware_host_feature_facts use vmware_host_feature_info instead.
- vmware_host_firewall_facts use vmware_host_firewall_info instead.
- vmware_host_ntp_facts use vmware_host_ntp_info instead.
- vmware_host_package_facts use vmware_host_package_info instead.
- vmware_host_service_facts use vmware_host_service_info instead.
- vmware_host_ssl_facts use vmware_host_ssl_info instead.
- vmware_host_vmhba_facts use vmware_host_vmhba_info instead.
- vmware_host_vmnic_facts use vmware_host_vmnic_info instead.
- vmware_local_role_facts use vmware_local_role_info instead.
- vmware_local_user_facts use vmware_local_user_info instead.
- vmware_portgroup_facts use vmware_portgroup_info instead.
- vmware_resource_pool_facts use vmware_resource_pool_info instead.
- vmware_target_canonical_facts use vmware_target_canonical_info instead.
- vmware_vmkernel_facts use vmware_vmkernel_info instead.
- vmware_vswitch_facts use vmware_vswitch_info instead.
- vultr_account_facts use vultr_account_info instead.
- vultr_block_storage_facts use vultr_block_storage_info instead.
- vultr_dns_domain_facts use vultr_dns_domain_info instead.
- vultr_firewall_group_facts use vultr_firewall_group_info instead.
- vultr_network_facts use vultr_network_info instead.
- vultr_os_facts use vultr_os_info instead.
- vultr_plan_facts use vultr_plan_info instead.
- vultr_region_facts use vultr_region_info instead.
- vultr_server_facts use vultr_server_info instead.
- vultr_ssh_key_facts use vultr_ssh_key_info instead.
- vultr_startup_script_facts use vultr_startup_script_info instead.
- vultr_user_facts use vultr_user_info instead.
- vyos_interface use vyos_interfaces instead.
- vyos_l3_interface use vyos_l3_interfaces instead.
- vyos_linkagg use vyos_lag_interfaces instead.
- vyos_lldp use vyos_lldp_global instead.
- vyos_lldp_interface use vyos_lldp_interfaces instead.

The following functionality will be removed in Ansible 2.12. Please update update your playbooks accordingly.

- `vmware_cluster` DRS, HA and VSAN configuration; use vmware_cluster_drs, vmware_cluster_ha and vmware_cluster_vsan instead.

The following functionality will be removed in Ansible 2.13. Please update update your playbooks accordingly.

- `openssl_certificate` deprecates the `assertonly` provider. Please see the openssl_certificate documentation examples on how to replace the provider with the openssl_certificate_info, openssl_csr_info, openssl_privatekey_info and assert modules.

For the following modules, the PyOpenSSL-based backend `pyopenssl` has been deprecated and will be removed in Ansible 2.13:

- get_certificate
- openssl_certificate
- openssl_certificate_info
- openssl_csr
- openssl_csr_info
- openssl_privatekey
- openssl_privatekey_info
- openssl_publickey

#### Renamed modules

The following modules have been renamed. The old name is deprecated and will be removed in Ansible 2.13. Please update update your playbooks accordingly.

- The `ali_instance_facts` module was renamed to ali_instance_info.
- The `aws_acm_facts` module was renamed to aws_acm_info.
- The `aws_az_facts` module was renamed to aws_az_info.
- The `aws_caller_facts` module was renamed to aws_caller_info.
- The `aws_kms_facts` module was renamed to aws_kms_info.
- The `aws_region_facts` module was renamed to aws_region_info.
- The `aws_s3_bucket_facts` module was renamed to aws_s3_bucket_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `aws_sgw_facts` module was renamed to aws_sgw_info.
- The `aws_waf_facts` module was renamed to aws_waf_info.
- The `azure_rm_aks_facts` module was renamed to azure_rm_aks_info.
- The `azure_rm_aksversion_facts` module was renamed to azure_rm_aksversion_info.
- The `azure_rm_applicationsecuritygroup_facts` module was renamed to azure_rm_applicationsecuritygroup_info.
- The `azure_rm_appserviceplan_facts` module was renamed to azure_rm_appserviceplan_info.
- The `azure_rm_automationaccount_facts` module was renamed to azure_rm_automationaccount_info.
- The `azure_rm_autoscale_facts` module was renamed to azure_rm_autoscale_info.
- The `azure_rm_availabilityset_facts` module was renamed to azure_rm_availabilityset_info.
- The `azure_rm_cdnendpoint_facts` module was renamed to azure_rm_cdnendpoint_info.
- The `azure_rm_cdnprofile_facts` module was renamed to azure_rm_cdnprofile_info.
- The `azure_rm_containerinstance_facts` module was renamed to azure_rm_containerinstance_info.
- The `azure_rm_containerregistry_facts` module was renamed to azure_rm_containerregistry_info.
- The `azure_rm_cosmosdbaccount_facts` module was renamed to azure_rm_cosmosdbaccount_info.
- The `azure_rm_deployment_facts` module was renamed to azure_rm_deployment_info.
- The `azure_rm_resourcegroup_facts` module was renamed to azure_rm_resourcegroup_info.
- The `bigip_device_facts` module was renamed to bigip_device_info.
- The `bigiq_device_facts` module was renamed to bigiq_device_info.
- The `cloudformation_facts` module was renamed to cloudformation_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `cloudfront_facts` module was renamed to cloudfront_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `cloudwatchlogs_log_group_facts` module was renamed to cloudwatchlogs_log_group_info.
- The `digital_ocean_account_facts` module was renamed to digital_ocean_account_info.
- The `digital_ocean_certificate_facts` module was renamed to digital_ocean_certificate_info.
- The `digital_ocean_domain_facts` module was renamed to digital_ocean_domain_info.
- The `digital_ocean_firewall_facts` module was renamed to digital_ocean_firewall_info.
- The `digital_ocean_floating_ip_facts` module was renamed to digital_ocean_floating_ip_info.
- The `digital_ocean_image_facts` module was renamed to digital_ocean_image_info.
- The `digital_ocean_load_balancer_facts` module was renamed to digital_ocean_load_balancer_info.
- The `digital_ocean_region_facts` module was renamed to digital_ocean_region_info.
- The `digital_ocean_size_facts` module was renamed to digital_ocean_size_info.
- The `digital_ocean_snapshot_facts` module was renamed to digital_ocean_snapshot_info.
- The `digital_ocean_tag_facts` module was renamed to digital_ocean_tag_info.
- The `digital_ocean_volume_facts` module was renamed to digital_ocean_volume_info.
- The `ec2_ami_facts` module was renamed to ec2_ami_info.
- The `ec2_asg_facts` module was renamed to ec2_asg_info.
- The `ec2_customer_gateway_facts` module was renamed to ec2_customer_gateway_info.
- The `ec2_eip_facts` module was renamed to ec2_eip_info.
- The `ec2_elb_facts` module was renamed to ec2_elb_info.
- The `ec2_eni_facts` module was renamed to ec2_eni_info.
- The `ec2_group_facts` module was renamed to ec2_group_info.
- The `ec2_instance_facts` module was renamed to ec2_instance_info.
- The `ec2_lc_facts` module was renamed to ec2_lc_info.
- The `ec2_placement_group_facts` module was renamed to ec2_placement_group_info.
- The `ec2_snapshot_facts` module was renamed to ec2_snapshot_info.
- The `ec2_vol_facts` module was renamed to ec2_vol_info.
- The `ec2_vpc_dhcp_option_facts` module was renamed to ec2_vpc_dhcp_option_info.
- The `ec2_vpc_endpoint_facts` module was renamed to ec2_vpc_endpoint_info.
- The `ec2_vpc_igw_facts` module was renamed to ec2_vpc_igw_info.
- The `ec2_vpc_nacl_facts` module was renamed to ec2_vpc_nacl_info.
- The `ec2_vpc_nat_gateway_facts` module was renamed to ec2_vpc_nat_gateway_info.
- The `ec2_vpc_net_facts` module was renamed to ec2_vpc_net_info.
- The `ec2_vpc_peering_facts` module was renamed to ec2_vpc_peering_info.
- The `ec2_vpc_route_table_facts` module was renamed to ec2_vpc_route_table_info.
- The `ec2_vpc_subnet_facts` module was renamed to ec2_vpc_subnet_info.
- The `ec2_vpc_vgw_facts` module was renamed to ec2_vpc_vgw_info.
- The `ec2_vpc_vpn_facts` module was renamed to ec2_vpc_vpn_info.
- The `ecs_service_facts` module was renamed to ecs_service_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ecs_taskdefinition_facts` module was renamed to ecs_taskdefinition_info.
- The `efs_facts` module was renamed to efs_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `elasticache_facts` module was renamed to elasticache_info.
- The `elb_application_lb_facts` module was renamed to elb_application_lb_info.
- The `elb_classic_lb_facts` module was renamed to elb_classic_lb_info.
- The `elb_target_facts` module was renamed to elb_target_info.
- The `elb_target_group_facts` module was renamed to elb_target_group_info.
- The `gcp_bigquery_dataset_facts` module was renamed to gcp_bigquery_dataset_info.
- The `gcp_bigquery_table_facts` module was renamed to gcp_bigquery_table_info.
- The `gcp_cloudbuild_trigger_facts` module was renamed to gcp_cloudbuild_trigger_info.
- The `gcp_compute_address_facts` module was renamed to gcp_compute_address_info.
- The `gcp_compute_backend_bucket_facts` module was renamed to gcp_compute_backend_bucket_info.
- The `gcp_compute_backend_service_facts` module was renamed to gcp_compute_backend_service_info.
- The `gcp_compute_disk_facts` module was renamed to gcp_compute_disk_info.
- The `gcp_compute_firewall_facts` module was renamed to gcp_compute_firewall_info.
- The `gcp_compute_forwarding_rule_facts` module was renamed to gcp_compute_forwarding_rule_info.
- The `gcp_compute_global_address_facts` module was renamed to gcp_compute_global_address_info.
- The `gcp_compute_global_forwarding_rule_facts` module was renamed to gcp_compute_global_forwarding_rule_info.
- The `gcp_compute_health_check_facts` module was renamed to gcp_compute_health_check_info.
- The `gcp_compute_http_health_check_facts` module was renamed to gcp_compute_http_health_check_info.
- The `gcp_compute_https_health_check_facts` module was renamed to gcp_compute_https_health_check_info.
- The `gcp_compute_image_facts` module was renamed to gcp_compute_image_info.
- The `gcp_compute_instance_facts` module was renamed to gcp_compute_instance_info.
- The `gcp_compute_instance_group_facts` module was renamed to gcp_compute_instance_group_info.
- The `gcp_compute_instance_group_manager_facts` module was renamed to gcp_compute_instance_group_manager_info.
- The `gcp_compute_instance_template_facts` module was renamed to gcp_compute_instance_template_info.
- The `gcp_compute_interconnect_attachment_facts` module was renamed to gcp_compute_interconnect_attachment_info.
- The `gcp_compute_network_facts` module was renamed to gcp_compute_network_info.
- The `gcp_compute_region_disk_facts` module was renamed to gcp_compute_region_disk_info.
- The `gcp_compute_route_facts` module was renamed to gcp_compute_route_info.
- The `gcp_compute_router_facts` module was renamed to gcp_compute_router_info.
- The `gcp_compute_ssl_certificate_facts` module was renamed to gcp_compute_ssl_certificate_info.
- The `gcp_compute_ssl_policy_facts` module was renamed to gcp_compute_ssl_policy_info.
- The `gcp_compute_subnetwork_facts` module was renamed to gcp_compute_subnetwork_info.
- The `gcp_compute_target_http_proxy_facts` module was renamed to gcp_compute_target_http_proxy_info.
- The `gcp_compute_target_https_proxy_facts` module was renamed to gcp_compute_target_https_proxy_info.
- The `gcp_compute_target_pool_facts` module was renamed to gcp_compute_target_pool_info.
- The `gcp_compute_target_ssl_proxy_facts` module was renamed to gcp_compute_target_ssl_proxy_info.
- The `gcp_compute_target_tcp_proxy_facts` module was renamed to gcp_compute_target_tcp_proxy_info.
- The `gcp_compute_target_vpn_gateway_facts` module was renamed to gcp_compute_target_vpn_gateway_info.
- The `gcp_compute_url_map_facts` module was renamed to gcp_compute_url_map_info.
- The `gcp_compute_vpn_tunnel_facts` module was renamed to gcp_compute_vpn_tunnel_info.
- The `gcp_container_cluster_facts` module was renamed to gcp_container_cluster_info.
- The `gcp_container_node_pool_facts` module was renamed to gcp_container_node_pool_info.
- The `gcp_dns_managed_zone_facts` module was renamed to gcp_dns_managed_zone_info.
- The `gcp_dns_resource_record_set_facts` module was renamed to gcp_dns_resource_record_set_info.
- The `gcp_iam_role_facts` module was renamed to gcp_iam_role_info.
- The `gcp_iam_service_account_facts` module was renamed to gcp_iam_service_account_info.
- The `gcp_pubsub_subscription_facts` module was renamed to gcp_pubsub_subscription_info.
- The `gcp_pubsub_topic_facts` module was renamed to gcp_pubsub_topic_info.
- The `gcp_redis_instance_facts` module was renamed to gcp_redis_instance_info.
- The `gcp_resourcemanager_project_facts` module was renamed to gcp_resourcemanager_project_info.
- The `gcp_sourcerepo_repository_facts` module was renamed to gcp_sourcerepo_repository_info.
- The `gcp_spanner_database_facts` module was renamed to gcp_spanner_database_info.
- The `gcp_spanner_instance_facts` module was renamed to gcp_spanner_instance_info.
- The `gcp_sql_database_facts` module was renamed to gcp_sql_database_info.
- The `gcp_sql_instance_facts` module was renamed to gcp_sql_instance_info.
- The `gcp_sql_user_facts` module was renamed to gcp_sql_user_info.
- The `gcp_tpu_node_facts` module was renamed to gcp_tpu_node_info.
- The `gcpubsub_facts` module was renamed to gcpubsub_info.
- The `github_webhook_facts` module was renamed to github_webhook_info.
- The `gluster_heal_facts` module was renamed to gluster_heal_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `hcloud_datacenter_facts` module was renamed to hcloud_datacenter_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `hcloud_floating_ip_facts` module was renamed to hcloud_floating_ip_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `hcloud_image_facts` module was renamed to hcloud_image_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `hcloud_location_facts` module was renamed to hcloud_location_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `hcloud_server_facts` module was renamed to hcloud_server_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `hcloud_server_type_facts` module was renamed to hcloud_server_type_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `hcloud_ssh_key_facts` module was renamed to hcloud_ssh_key_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `hcloud_volume_facts` module was renamed to hcloud_volume_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `hpilo_facts` module was renamed to hpilo_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `iam_mfa_device_facts` module was renamed to iam_mfa_device_info.
- The `iam_role_facts` module was renamed to iam_role_info.
- The `iam_server_certificate_facts` module was renamed to iam_server_certificate_info.
- The `idrac_redfish_facts` module was renamed to idrac_redfish_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `intersight_facts` module was renamed to intersight_info.
- The `jenkins_job_facts` module was renamed to jenkins_job_info.
- The `k8s_facts` module was renamed to k8s_info.
- The `memset_memstore_facts` module was renamed to memset_memstore_info.
- The `memset_server_facts` module was renamed to memset_server_info.
- The `one_image_facts` module was renamed to one_image_info.
- The `onepassword_facts` module was renamed to onepassword_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `oneview_datacenter_facts` module was renamed to oneview_datacenter_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `oneview_enclosure_facts` module was renamed to oneview_enclosure_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `oneview_ethernet_network_facts` module was renamed to oneview_ethernet_network_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `oneview_fc_network_facts` module was renamed to oneview_fc_network_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `oneview_fcoe_network_facts` module was renamed to oneview_fcoe_network_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `oneview_logical_interconnect_group_facts` module was renamed to oneview_logical_interconnect_group_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `oneview_network_set_facts` module was renamed to oneview_network_set_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `oneview_san_manager_facts` module was renamed to oneview_san_manager_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `os_flavor_facts` module was renamed to os_flavor_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `os_image_facts` module was renamed to os_image_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `os_keystone_domain_facts` module was renamed to os_keystone_domain_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `os_networks_facts` module was renamed to os_networks_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `os_port_facts` module was renamed to os_port_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `os_project_facts` module was renamed to os_project_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `os_server_facts` module was renamed to os_server_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `os_subnets_facts` module was renamed to os_subnets_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `os_user_facts` module was renamed to os_user_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_affinity_label_facts` module was renamed to ovirt_affinity_label_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_api_facts` module was renamed to ovirt_api_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_cluster_facts` module was renamed to ovirt_cluster_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_datacenter_facts` module was renamed to ovirt_datacenter_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_disk_facts` module was renamed to ovirt_disk_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_event_facts` module was renamed to ovirt_event_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_external_provider_facts` module was renamed to ovirt_external_provider_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_group_facts` module was renamed to ovirt_group_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_host_facts` module was renamed to ovirt_host_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_host_storage_facts` module was renamed to ovirt_host_storage_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_network_facts` module was renamed to ovirt_network_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_nic_facts` module was renamed to ovirt_nic_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_permission_facts` module was renamed to ovirt_permission_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_quota_facts` module was renamed to ovirt_quota_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_scheduling_policy_facts` module was renamed to ovirt_scheduling_policy_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_snapshot_facts` module was renamed to ovirt_snapshot_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_storage_domain_facts` module was renamed to ovirt_storage_domain_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_storage_template_facts` module was renamed to ovirt_storage_template_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_storage_vm_facts` module was renamed to ovirt_storage_vm_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_tag_facts` module was renamed to ovirt_tag_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_template_facts` module was renamed to ovirt_template_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_user_facts` module was renamed to ovirt_user_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_vm_facts` module was renamed to ovirt_vm_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `ovirt_vmpool_facts` module was renamed to ovirt_vmpool_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `python_requirements_facts` module was renamed to python_requirements_info.
- The `rds_instance_facts` module was renamed to rds_instance_info.
- The `rds_snapshot_facts` module was renamed to rds_snapshot_info.
- The `redfish_facts` module was renamed to redfish_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `redshift_facts` module was renamed to redshift_info.
- The `route53_facts` module was renamed to route53_info.
- The `smartos_image_facts` module was renamed to smartos_image_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `vertica_facts` module was renamed to vertica_info. When called with the new name, the module no longer returns `ansible_facts`. To access return values, register a variable.
- The `vmware_cluster_facts` module was renamed to vmware_cluster_info.
- The `vmware_datastore_facts` module was renamed to vmware_datastore_info.
- The `vmware_guest_facts` module was renamed to vmware_guest_info.
- The `vmware_guest_snapshot_facts` module was renamed to vmware_guest_snapshot_info.
- The `vmware_tag_facts` module was renamed to vmware_tag_info.
- The `vmware_vm_facts` module was renamed to vmware_vm_info.
- The `xenserver_guest_facts` module was renamed to xenserver_guest_info.
- The `zabbix_group_facts` module was renamed to zabbix_group_info.
- The `zabbix_host_facts` module was renamed to zabbix_host_info.

### Noteworthy module changes

- vmware_cluster was refactored for easier maintenance/bugfixes. Use the three new, specialized modules to configure clusters. Configure DRS with vmware_cluster_drs, HA with vmware_cluster_ha and vSAN with vmware_cluster_vsan.
- vmware_dvswitch accepts `folder` parameter to place dvswitch in user defined folder. This option makes `datacenter` as an optional parameter.
- vmware_datastore_cluster accepts `folder` parameter to place datastore cluster in user defined folder. This option makes `datacenter` as an optional parameter.
- mysql_db returns new `db_list` parameter in addition to `db` parameter. This `db_list` parameter refers to list of database names. `db` parameter will be deprecated in version 2.13.
- snow_record and snow_record_find now takes environment variables for `instance`, `username` and `password` parameters. This change marks these parameters as optional.
- The deprecated `force` option in `win_firewall_rule` has been removed.
- openssl_certificate's `ownca` provider creates authority key identifiers if not explicitly disabled with `ownca_create_authority_key_identifier: no`. This is only the case for the `cryptography` backend, which is selected by default if the `cryptography` library is available.
- openssl_certificate's `ownca` and `selfsigned` providers create subject key identifiers if not explicitly disabled with `ownca_create_subject_key_identifier: never_create` resp. `selfsigned_create_subject_key_identifier: never_create`. If a subject key identifier is provided by the CSR, it is taken; if not, it is created from the public key. This is only the case for the `cryptography` backend, which is selected by default if the `cryptography` library is available.
- openssh_keypair now applies the same file permissions and ownership to both public and private keys (both get the same `mode`, `owner`, `group`, and so on). If you need to change permissions / ownership on one key, use the file to modify it after it is created.

## Plugins

### Removed Lookup Plugins

- `redis_kv` use redis instead.

## Porting custom scripts

No notable changes

## Networking

### Network resource modules

Ansible 2.9 introduced the first batch of network resource modules. Sections of a network device's configuration can be thought of as a resource provided by that device. Network resource modules are intentionally scoped to configure a single resource and you can combine them as building blocks to configure complex network services. The older modules are deprecated in Ansible 2.9 and will be removed in Ansible 2.13. You should scan the list of deprecated modules above and replace them with the new network resource modules in your playbooks. See [Ansible Network Features in 2.9](https://www.ansible.com/blog/network-features-coming-soon-in-ansible-engine-2.9) for details.

### Improved `gather_facts` support for network devices

In Ansible 2.9, the `gather_facts` keyword now supports gathering network device facts in standardized key/value pairs. You can feed these network facts into further tasks to manage the network device. You can also use the new `gather_network_resources` parameter with the network `*_facts` modules (such as eos_facts) to return just a subset of the device configuration. See network_gather_facts for an example.

### Top-level connection arguments removed in 2.9

Top-level connection arguments like `username`, `host`, and `password` are removed in version 2.9.

**OLD** In Ansible \< 2.4

``` yaml
- name: example of using top-level options for connection properties
  ios_command:
    commands: show version
    host: "{{ inventory_hostname }}"
    username: cisco
    password: cisco
    authorize: yes
    auth_pass: cisco
```

Change your playbooks to the connection types `network_cli` and `netconf` using standard Ansible connection properties, and setting those properties in inventory by group. As you update your playbooks and inventory files, you can easily make the change to `become` for privilege escalation (on platforms that support it). For more information, see the using become with network modules guide and the platform documentation.
