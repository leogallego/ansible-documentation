# Ansible project 7.0

This release schedule includes dates for the [ansible](https://pypi.org/project/ansible/) package, with a few dates for the [ansible-core](https://pypi.org/project/ansible-core/) package as well. All dates are subject to change. See the [ansible-core 2.14 Roadmap](https://docs.ansible.com/ansible-core/devel/roadmap/ROADMAP_2_14.html) for the most recent updates on `ansible-core`.

## Release schedule

2022-09-19  
ansible-core feature freeze, stable-2.14 branch created.

2022-09-26  
Start of ansible-core 2.14 betas (biweekly, as needed).

2022-09-27  
Ansible-7.0.0 alpha1 (roughly biweekly `ansible` alphas timed to coincide with `ansible-core-2.14` pre-releases).

2022-10-12  
Community topic: List any backwards incompatible collection releases that beta1 should try to accommodate.

2022-10-17  
First ansible-core 2.14 release candidate.

2022-10-25  
Ansible-7.0.0 alpha2.

2022-10-26  
Community Meeting topic: Decide what contingencies to activate for any blockers that do not meet the deadline.

2022-11-07  
Ansible-core-2.14.0 released.

2022-11-07  
Last day for collections to make backwards incompatible releases that will be accepted into Ansible-7. This includes adding new collections to Ansible 7.0.0; from now on new collections have to wait for 7.1.0 or later.

2022-11-08  
Create the ansible-build-data directory and files for Ansible-8.

2022-11-08  
Ansible-7.0.0 beta1 -- feature freeze (weekly beta releases; collection owners and interested users should test for bugs).

2022-11-15  
Ansible-7.0.0 rc1 (weekly release candidates as needed; test and alert us to any blocker bugs). Blocker bugs will slip release.

2022-11-18  
Last day to trigger an Ansible-7.0.0rc2 release because of major defects in Ansible-7.0.0rc1.

2022-11-22  
Ansible-7.0.0rc2 when necessary, otherwise Ansible-7.0.0 release.

2022-11-29  
Ansible-7.0.0 release when Ansible-7.0.0rc2 was necessary.

2022-12-05  
Release of ansible-core 2.14.1.

2022-12-06  
Release of Ansible-7.1.0 (bugfix + compatible features: every four weeks.)

Breaking changes will be introduced in Ansible 7.0.0, although we encourage the use of deprecation periods that will show up in at least one Ansible release before the breaking change happens, this is not guaranteed.

## Ansible minor releases

Ansible 7.x minor releases will occur approximately every four weeks if changes to collections have been made or to align to a later ansible-core-2.14.x. Ansible 7.x minor releases may contain new features but not backwards incompatibilities. In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example, if Ansible-7.0.0 ships with community.crypto 2.3.0; Ansible-7.1.0 may ship with community.crypto 2.4.0 but would not ship with community.crypto 3.0.0.

Minor releases will stop when Ansible-8 is released. See the Release and Maintenance Page for more information.

For more information, reach out on a mailing list or a chat channel - see communication for more details.
