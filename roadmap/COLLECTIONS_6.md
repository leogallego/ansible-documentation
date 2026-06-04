# Ansible project 6.0

This release schedule includes dates for the [ansible](https://pypi.org/project/ansible/) package, with a few dates for the [ansible-core](https://pypi.org/project/ansible-core/) package as well. All dates are subject to change. See the [ansible-core 2.13 Roadmap](https://docs.ansible.com/ansible-core/devel/roadmap/ROADMAP_2_13.html) for the most recent updates on `ansible-core`.

## Release schedule

2022-03-28  
ansible-core feature freeze, stable-2.13 branch created.

2022-04-11  
Start of ansible-core 2.13 betas (biweekly, as needed).

2022-04-12  
Ansible-6.0.0 alpha1 (roughly biweekly `ansible` alphas timed to coincide with `ansible-core-2.13` pre-releases).

2022-04-27  
Community Meeting topic: List any backwards incompatible collection releases that beta1 should try to accommodate.

2022-05-02  
First ansible-core release candidate.

2022-05-03  
Ansible-6.0.0 alpha2.

2022-05-11  
Community Meeting topic: Decide what contingencies to activate for any blockers that do not meet the deadline.

2022-05-16  
Ansible-core-2.13 released.

2022-05-17  
Ansible-6.0.0 alpha3.

2022-05-23  
Last day for collections to make backwards incompatible releases that will be accepted into Ansible-6. This includes adding new collections to Ansible 6.0.0; from now on new collections have to wait for 6.1.0 or later.

2022-05-24  
Create the ansible-build-data directory and files for Ansible-7.

2022-05-24  
Ansible-6.0.0 beta1 -- feature freeze (weekly beta releases; collection owners and interested users should test for bugs).

2022-05-31  
Ansible-6.0.0 beta2.

2022-06-07  
Ansible-6.0.0 rc1 (weekly release candidates as needed; test and alert us to any blocker bugs). Blocker bugs will slip release.

2022-06-21  
Ansible-6.0.0 release.

2022-07-12  
Release of Ansible-6.1.0 (bugfix + compatible features: every three weeks.)

Breaking changes will be introduced in Ansible 6.0.0, although we encourage the use of deprecation periods that will show up in at least one Ansible release before the breaking change happens, this is not guaranteed.

## Ansible minor releases

Ansible 6.x minor releases will occur approximately every three weeks if changes to collections have been made or if it is deemed necessary to force an upgrade to a later ansible-core-2.13.x. Ansible 6.x minor releases may contain new features but not backwards incompatibilities. In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example, if Ansible-6.0.0 ships with community.crypto 2.3.0; Ansible-6.1.0 may ship with community.crypto 2.4.0 but would not ship with community.crypto 3.0.0.

Minor releases will stop when Ansible-7 is released. See the Release and Maintenance Page for more information.

For more information, reach out on a mailing list or a chat channel - see communication for more details.

## Planned work

More details can be found in [the community-topics planning issue](https://github.com/ansible-community/community-topics/issues/56).

- Remove compatibility code which prevents parallel install of Ansible 6 with Ansible 2.9 or ansible-base 2.10
- Stop installing files (such as tests and development artifacts like editor configs) we have no use for
- Ship Python wheels (as ansible-core 2.13 will likely also do) to improve installation performance
