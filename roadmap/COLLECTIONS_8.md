# Ansible project 8.0

This release schedule includes dates for the [ansible](https://pypi.org/project/ansible/) package, with a few dates for the [ansible-core](https://pypi.org/project/ansible-core/) package as well. All dates are subject to change. See the [ansible-core 2.15 Roadmap](https://docs.ansible.com/ansible-core/devel/roadmap/ROADMAP_2_15.html) for the most recent updates on `ansible-core`.

## Release schedule

2023-03-31  
ansible-core feature freeze, stable-2.15 branch created.

2023-04-03  
Start of ansible-core 2.15 betas (biweekly, as needed).

2023-04-04  
Ansible-8.0.0 alpha1 (roughly biweekly `ansible` alphas timed to coincide with `ansible-core-2.15` pre-releases).

2023-04-24  
First ansible-core 2.15 release candidate.

2023-05-02  
Another Ansible-8.0.0 alpha release.

2023-05-15  
Ansible-core-2.15.0 released.

2023-05-15  
Last day for collections to make backwards incompatible releases that will be accepted into Ansible-8. This includes adding new collections to Ansible 8.0.0; from now on new collections have to wait for 8.1.0 or later.

2023-05-16  
Ansible-8.0.0 beta1 -- feature freeze (weekly beta releases; collection owners and interested users should test for bugs).

2023-05-23  
Ansible-8.0.0 rc1 (weekly release candidates as needed; test and alert us to any blocker bugs). Blocker bugs will slip release.

2023-05-26  
Last day to trigger an Ansible-8.0.0rc2 release because of major defects in Ansible-8.0.0rc1.

2023-05-30  
Ansible-8.0.0rc2 when necessary, otherwise Ansible-8.0.0 release.

2023-06-06  
Ansible-8.0.0 release when Ansible-8.0.0rc2 was necessary.

2023-05-30 or 2023-06-06  
Create the ansible-build-data directory and files for Ansible-9.

2023-06-20  
Release of ansible-core 2.15.1.

2023-06-22  
Release of Ansible-8.1.0 (bugfix + compatible features: every four weeks.)

Breaking changes will be introduced in Ansible 8.0.0, although we encourage the use of deprecation periods that will show up in at least one Ansible release before the breaking change happens, this is not guaranteed.

In general, it is in the discretion of the release manager to delay a release by 1-2 days for reasons such as personal (schedule) problems, technical problems (CI/infrastructure breakdown), and so on. However, in case two releases are planned for the same day, a release of the latest stable version takes precedence. This means that if a stable Ansible 8 release collides with a pre-release of Ansible 9, the latter will be delayed. If a Ansible 8 release collides with a stable Ansible 9 release, including 9.0.0, the Ansible 8 release will be delayed.

## Ansible minor releases

Ansible 8.x minor releases will occur approximately every four weeks if changes to collections have been made or to align to a later ansible-core-2.15.x. Ansible 8.x minor releases may contain new features but not backwards incompatibilities. In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example, if Ansible-8.0.0 ships with community.crypto 2.3.0; Ansible-8.1.0 may ship with community.crypto 2.4.0 but would not ship with community.crypto 3.0.0.

Minor and patch releases will stop when Ansible-9 is released. See the Release and Maintenance Page for more information.

For more information, reach out on a mailing list or a chat channel - see communication for more details.
