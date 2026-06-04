# Ansible project 12.0

This release schedule includes dates for the [ansible](https://pypi.org/project/ansible/) package, with a few dates for the [ansible-core](https://pypi.org/project/ansible-core/) package as well. All dates are subject to change. See the [ansible-core 2.19 Roadmap](https://docs.ansible.com/ansible-core/devel/roadmap/ROADMAP_2_19.html) for the most recent updates on `ansible-core`.

## Release schedule

The schedule has been updated to match the ansible-core 2.19 release schedule. If that one gets modified again, the Ansible 12 pre-release and release dates will be shifted accordingly, and potentially more pre-releases will be inserted.

2025-04-14  
ansible-core feature freeze, stable-2.19 branch created.

2025-04-14  
Start of ansible-core 2.19 betas.

2025-04-16  
Ansible-12.0.0 alpha1; there will be more alpha releases usually following additional ansible-core 2.19 betas.

2025-06-30  
First ansible-core 2.19 release candidate.

2025-07-01  
Ansible-12.0.0 alphaX; there might be more alpha releases following additional ansible-core 2.19 release candidates.

2025-07-21  
Ansible-core-2.19.0 released.

2025-07-21  
Last day for collections to make backwards incompatible releases that will be accepted into Ansible-12. This includes adding new collections to Ansible 12.0.0; from now on new collections have to wait for 12.1.0 or later.

2025-07-22  
Ansible-12.0.0 beta1 -- feature freeze (collection owners and interested users should test for bugs).

2025-07-29  
Ansible-12.0.0 rc1 (weekly release candidates as needed; test and alert us to any blocker bugs). Blocker bugs will slip release.

2025-08-01  
Last day to trigger an Ansible-12.0.0rc2 release because of major defects in Ansible-12.0.0rc1.

2025-08-05  
Ansible-12.0.0rc2 when necessary, otherwise Ansible-12.0.0 release.

2025-08-12  
Ansible-12.0.0 release when Ansible-12.0.0rc2 was necessary.

2025-08-05 or 2025-08-12  
Create the ansible-build-data directory and files for Ansible-13.

2025-08-18  
Release of ansible-core 2.19.1.

2025-08-19  
Release of Ansible-12.1.0 (bugfix + compatible features: every four weeks.)

Breaking changes will be introduced in Ansible 12.0.0. We encourage the use of deprecation periods that give advance notice of breaking changes at least one Ansible release before they are introduced. However, deprecation notices are not guaranteed to take place.

In general, it is in the discretion of the release manager to delay a release by 1-2 days for reasons such as personal (schedule) problems, technical problems (CI/infrastructure breakdown), and so on. However, in case two releases are planned for the same day, a release of the latest stable version takes precedence. This means that if a stable Ansible 12 release collides with a pre-release of Ansible 13, the latter will be delayed. If an Ansible 12 release collides with a stable Ansible 13 release, including 13.0.0, the Ansible 12 release will be delayed.

## Planned major changes

- The inspur.sm collection will be removed as it is unmaintained (<https://github.com/ansible-community/ansible-build-data/issues/424>).
- The netapp.storagegrid collection will be removed as it is unmaintained (<https://github.com/ansible-community/ansible-build-data/issues/434>).
- The frr.frr collection will be removed as it is unmaintained (<https://github.com/ansible-community/ansible-build-data/issues/437>).
- The openvswitch.openvswitch collection will be removed as it is unmaintained (<https://github.com/ansible-community/ansible-build-data/issues/437>).

You can install removed collections manually with `ansible-galaxy collection install <collection_name>`.

## Ansible minor releases

Ansible 12.x follows ansible-core-2.19.x releases, so releases will occur approximately every four weeks. If ansible-core delays a release for whatever reason, the next Ansible 12.x minor release will be delayed accordingly.

Ansible 12.x minor releases may contain new features (including new collections) but not backwards incompatibilities. In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example, if Ansible-12.0.0 ships with community.crypto 2.3.0, Ansible-12.1.0 could ship with community.crypto 2.4.0 but not community.crypto 3.0.0.

Minor and patch releases will stop when Ansible-13 is released. See the Release and Maintenance Page for more information.

We will not provide bugfixes or security fixes for collections that do not provide updates for their major release cycle included in Ansible 12.

## Communication

You can submit feedback on the current roadmap by creating a community topic.

Visit the Ansible communication guide for details on how to join and use Ansible communication platforms.
