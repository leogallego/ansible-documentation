# Ansible project 4.0

This release schedule includes dates for the [ansible](https://pypi.org/project/ansible/) package, with a few dates for the [ansible-core](https://pypi.org/project/ansible-core/) package as well. All dates are subject to change. See base_roadmap_2_11 for the most recent updates on `ansible-core`.

## Release schedule

2021-01-26  
New Collections will be reviewed for inclusion in Ansible 4. Submit a request to include a new collection in this [GitHub Discussion](https://github.com/ansible-collections/ansible-inclusion/discussions/new).

2021-03-03  
Ansible-4.0.0 alpha1 (biweekly `ansible` alphas. These are timed to coincide with the start of the `ansible-core-2.11` pre-releases).

2021-03-16  
Ansible-4.0.0 alpha2

2021-03-30  
Ansible-4.0.0 alpha3

2021-04-13  
Last day for new collections to be submitted for inclusion in Ansible 4. Note that collections MUST be reviewed and approved before being included. There is no guarantee that we will review every collection. The earlier your collection is submitted, the more likely it will be that your collection will be reviewed and the necessary feedback can be addressed in time for inclusion.

2021-04-13  
Ansible-4.0.0 alpha4

2021-04-14  
Community Meeting topic: list any new collection reviews which block release. List any backwards incompatible collection releases that beta1 should try to accommodate.

2021-04-21  
Community Meeting topic: Decide what contingencies to activate for any blockers that do not meet the deadline.

2021-04-26  
Last day for new collections to be **reviewed and approved** for inclusion in Ansible 4.

2021-04-26  
Last day for collections to make backwards incompatible releases that will be accepted into Ansible 4.

2021-04-27  
Ansible-4.0.0 beta1 -- feature freeze (weekly beta releases. Collection owners and interested users should test for bugs).

2021-05-04  
Ansible-4.0.0 beta2

2021-05-11  
Ansible-4.0.0 rc1 (weekly release candidates as needed. Test and alert us to any blocker bugs).

2021-05-18  
Ansible-4.0.0 release

2021-06-08  
Release of Ansible-4.1.0 (bugfix + compatible features: every three weeks)

Breaking changes will be introduced in Ansible 4.0.0, although we encourage the use of deprecation periods that will show up in at least one Ansible release before the breaking change happens, this is not guaranteed.

## Ansible minor releases

Ansible 4.x minor releases will occur approximately every three weeks if changes to collections have been made or if it is deemed necessary to force an upgrade to a later ansible-core-2.11.x. Ansible 4.x minor releases may contain new features but not backwards incompatibilities. In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example, if Ansible-4.0.0 ships with community-crypto-2.1.0; Ansible-4.1.0 may ship with community-crypto-2.2.0 but would not ship with community-crypto-3.0.0).

Minor releases will stop when Ansible-5 is released. See the Release and Maintenance Page for more information.

For more information, reach out on a mailing list or a chat channel - see communication for more details.
