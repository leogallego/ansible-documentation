# Ansible project 5.0

This release schedule includes dates for the [ansible](https://pypi.org/project/ansible/) package, with a few dates for the [ansible-core](https://pypi.org/project/ansible-core/) package as well. All dates are subject to change. See core_roadmap_2_12 for the most recent updates on `ansible-core`.

## Release schedule

2021-04-14  
New Collections can be reviewed for inclusion in Ansible 5. Submit a request to include a new collection in this [GitHub Discussion](https://github.com/ansible-collections/ansible-inclusion/discussions/new).

2021-09-24  
ansible-core feature freeze.

2021-09-27  
Start of ansible-core 2.12 betas (weekly, as needed).

2021-10-05  
Ansible-5.0.0 alpha1 (roughly biweekly `ansible` alphas timed to coincide with `ansible-core-2.12` pre-releases).

2021-10-12  
Last day for new collections to be submitted for inclusion in Ansible-5. Collections MUST be reviewed and approved before being included. There is no guarantee that we will review every collection. The earlier your collection is submitted, the more likely it will be that your collection will be reviewed and the necessary feedback can be addressed in time for inclusion.

2021-10-13  
Community Meeting topic: List any new collection reviews which block release. List any backwards incompatible collection releases that beta1 should try to accommodate.

2021-10-18  
First ansible-core release candidate, stable-2.12 branch created.

2021-10-19  
Ansible-5.0.0 alpha2.

2021-10-26  
Last day for new collections to be **reviewed and approved** for inclusion in Ansible-5.

2021-10-27  
Community Meeting topic: Decide what contingencies to activate for any blockers that do not meet the deadline.

2021-11-02  
Ansible-5.0.0 alpha3.

2021-11-08  
Ansible-core-2.12 released.

2021-11-08  
Last day for collections to make backwards incompatible releases that will be accepted into Ansible-5.

2021-11-09  
Create the ansible-build-data directory and files for Ansible-6. New collection approvals will target this.

2021-11-09  
Ansible-5.0.0 beta1 -- feature freeze (weekly beta releases; collection owners and interested users should test for bugs).

2021-11-16  
Ansible-5.0.0 beta2.

2021-11-23  
Ansible-5.0.0 rc1 (weekly release candidates as needed; test and alert us to any blocker bugs). Blocker bugs will slip release.

2021-11-30  
Ansible-5.0.0 release.

2021-12-21  
Release of Ansible-5.1.0 (bugfix + compatible features: every three weeks.)

Breaking changes will be introduced in Ansible 5.0.0, although we encourage the use of deprecation periods that will show up in at least one Ansible release before the breaking change happens, this is not guaranteed.

## Ansible minor releases

Ansible 5.x minor releases will occur approximately every three weeks if changes to collections have been made or if it is deemed necessary to force an upgrade to a later ansible-core-2.12.x. Ansible 5.x minor releases may contain new features but not backwards incompatibilities. In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example, if Ansible-5.0.0 ships with community.crypto 2.1.0; Ansible-5.1.0 may ship with community.crypto 2.2.0 but would not ship with community.crypto 3.0.0.

Minor releases will stop when Ansible-6 is released. See the Release and Maintenance Page for more information.

For more information, reach out on a mailing list or a chat channel - see communication for more details.
