# Ansible project 3.0

This release schedule includes dates for the [ansible](https://pypi.org/project/ansible/) package, with a few dates for the [ansible-base](https://pypi.org/project/ansible-base/) package as well. All dates are subject to change. Ansible 3.x.x includes `ansible-base` 2.10. See base_roadmap_2_10 for the most recent updates on `ansible-base`.

## Release schedule

Ansible is switching from its traditional versioning scheme to [semantic versioning](https://semver.org/) starting with this release. So this version is 3.0.0 instead of 2.11.0.

2020-12-16  
Finalize rules for net-new collections submitted for the ansible release.

2021-01-27  
Final day for new collections to be **reviewed and approved**. They MUST be submitted prior to this to give reviewers a chance to look them over and for collection owners to fix any problems.

2021-02-02  
Ansible-3.0.0-beta1 -- feature freeze

2021-02-09  
Ansible-3.0.0-rc1 -- final freeze

2021-02-16  
Release of Ansible-3.0.0

2021-03-09  
Release of Ansible-3.1.0 (bugfix + compatible features: every three weeks)

Breaking changes may be introduced in Ansible 3.0.0, although we encourage collection owners to use deprecation periods that will show up in at least one Ansible release before the breaking change happens.

## Ansible minor releases

Ansible 3.x.x minor releases will occur approximately every three weeks if changes to collections have been made or if it is deemed necessary to force an upgrade to a later ansible-base-2.10.x. Ansible 3.x.x minor releases may contain new features but not backwards incompatibilities. In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example, if Ansible-3.0.0 ships with community-crypto-2.1.0; Ansible-3.1.0 may ship with community-crypto-2.2.0 but would not ship with community-crypto-3.0.0).

Minor releases will stop when Ansible-4 is released. See the Release and Maintenance Page for more information.

For more information, reach out on a mailing list or a chat channel - see communication for more details.

## ansible-base release

Ansible 3.x.x works with `ansible-base` 2.10. See base_roadmap_2_10 for details.
