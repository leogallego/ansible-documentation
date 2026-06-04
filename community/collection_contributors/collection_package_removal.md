# Ansible Community Package Collections Removal Process

## Overview

Sometimes the Ansible community removes a collection from the Ansible package for stability, legal, or security reasons. This document describes why we might remove a collection from the [Ansible community package](https://pypi.org/project/ansible/) ([build data](https://github.com/ansible-community/ansible-build-data/)).

In cases of emergency (for example, a serious security vulnerability that is not fixed in a collection) the Ansible Community Engineering Steering Committee can vote on emergency exceptions. In most cases, we follow the rules listed on this page.

## General processes

The general process of removing a collection follows these steps:

1.  Announcing an upcoming removal of a collection.
2.  Removing the collection.
3.  When appropriate, re-adding the collection.

### Announcing upcoming removal

1.  [Announce upcoming removal in the Ansible changelog](https://ansible.readthedocs.io/projects/ansible-build-data/policies/#announce-removal-of-a-collection-deprecation). Note that if the collection has already been deprecated, and the deprecation was canceled / the collection was re-added, a [slightly different procedure has to be followed](https://ansible.readthedocs.io/projects/ansible-build-data/policies/#re-deprecating-a-collection).
2.  Announce upcoming removal in the collection's issue tracker if possible.
3.  Announce upcoming removal in The Bullhorn.

### Removing a collection

To remove a collection from Ansible version X.0.0, [follow the procedure documented in ansible-build-data](https://ansible.readthedocs.io/projects/ansible-build-data/policies/#removing-a-collection)

### Re-adding a collection

There are two processes:

- If the collection was not yet removed from `ansible.in` or no pre-release has been made for that Ansible version, look at [Cancel deprecation of a collection](https://ansible.readthedocs.io/projects/ansible-build-data/policies/#cancel-deprecation-of-a-collection).
- If the collection has already been removed from `ansible.in` and a pre-release has already been made for that Ansible version, look at [Re-adding a already removed collection](https://ansible.readthedocs.io/projects/ansible-build-data/policies/#re-adding-a-already-removed-collection).

## Broken collections

The community can remove a collection from the Ansible community package if the collection is broken.

### Identifying and removing a broken collection

#### Conditions for removal

A collection is considered broken if one of the following conditions is true:

1.  It depends on another collection included in X.0.0 but does not work with the actual version of it that is included, and there is no content in the collection that still works.

We remove broken collections from Ansible (X+1).0.0 under the following conditions:

1.  The collection seems to be unmaintained and nobody fixes the problems.
2.  The plan to remove the collection in the next major Ansible release is publicized at least two months before the (X+1).0.0 release, and at least one month before the first (X+1).0.0 beta release (feature freeze).

#### Process

The announcement mentioned below must state the reasons for the proposed removal and alert maintainers and the Ansible community that, to prevent the removal, the collection urgently needs new maintainers who can fix the problems.

1.  [Announce upcoming removal in Ansible X+1]().
2.  [Remove collection from Ansible X+1]().

### Canceling removal of a broken collection

#### Conditions

1.  The issues have to be fixed and a new release (bugfix, minor or major) has to be made before the Ansible X+1 feature freeze.
2.  Someone has to promise to maintain the collection and prevent a similar situation at least for some time.

#### Process

1.  Update the removal issue in the collection's issue tracker and close the issue.
2.  Announce canceled removal in The Bullhorn.
3.  [Re-add collection to Ansible X+1]().

### Re-adding collection to Ansible

#### Conditions

Conditions under which the collections can be re-included in the Ansible package without going through the [full inclusion process](https://github.com/ansible-collections/ansible-inclusion/):

1.  The issues have to be fixed and a new release has to be made before the Ansible X+2 feature freeze.
2.  Someone has to promise to maintain the collection and prevent a similar situation at least for some time.

#### Process

1.  Follow [regular process of adding a new collection to Ansible](https://github.com/ansible-community/ansible-build-data/#adding-a-new-collection).

## Unmaintained collections

### Removing a collection that has been explicitly deprecated or abandoned by its (former) maintainers

#### Process

If the current major release is X and there hasn't been a feature freeze release of the next major version X+1, remove the collection from Y=(X+1).0.0. If there already has been a feature freeze release of the next major version X+1, remove the collection from Y=(X+2).0.0.

1.  [Announce upcoming removal from the Y Ansible release]().
2.  [Remove collection from the Y Ansible release]().

See [the example pull request](https://github.com/ansible-community/ansible-build-data/pull/374/files) in the `ansible-build-data` repository to learn how to remove the collection.

### Identifying and removing an unmaintained collection that has not been deprecated by its maintainers

#### Conditions for removal

A collection is considered unmaintained if multiple of the following conditions are satisfied:

1.  There has been no maintainer's activity in the collection repository for several months (for example, pull request merges and releases).
2.  CI has stopped passing (or even has not been running) for several months.
3.  Bug reports and bugfix PRs start piling up without being reviewed.

There is no complete formal definition of an unmaintained collection.

#### Process

1.  The appearance that the collection is no longer maintained and might be removed from the Ansible package has to be announced both in The Bullhorn and in the collection's issue tracker.
2.  At least four weeks after the notice appeared in The Bullhorn and the collection's issue tracker, the Ansible Community Engineering Steering Committee (SC) must look at the collection and vote that it considers it unmaintained. The vote must be open for at least one week.
3.  If the SC does not vote that the collection seems to be unmaintained, the process is stopped. The issue needs to be updated accordingly.
4.  If X.0.0 will be released next, set Y=X+1. If X.0.0 has already been released, but (X+1).0.0 has not yet been released, set Y=X+2.
5.  [Announce upcoming removal from Ansible Y]().
6.  [Remove collection from Ansible Y]().

### Canceling removal of an unmaintained collection

#### Conditions

1.  Ansible Y has not yet been released.
2.  One or multiple maintainers step up, or return, to clean up the collection's state.
3.  There have been concrete results made by new maintainers (for example, CI has been fixed, the collection has been released, pull request authors have got meaningful feedback).

#### Process

1.  The Steering Committee votes on whether the result is acceptable.
2.  A negative vote must come with a good explanation why the clean up work has not been sufficient. In that case, this process stops.
3.  If the Steering Committee does not vote against still removing the collection (this includes the case that the vote did not reach quorum), proceed as follows.
4.  [Re-add collection to Ansible Y]().

### Re-adding collection to Ansible

There is no simplified process. Once the collection has been removed from Ansible Y.0.0, it needs to go through the full inclusion process to be re-added to the Ansible package. Exceptions are only possible if the Steering Committee votes on them. The Steering Committee can approve or deny a fast re-entry without going through the full review process.

## Collections not satisfying the Collection requirements

A collection can be removed from the package if it violates one or more of the Collection requirements without resolving the violations within the time allowed.

This section is not applicable to cases of broken or unmaintained collections. Instead, see the corresponding paragraphs of this document.

### Identifying and removing a collection

#### Conditions for removal

1.  A collection violates one or more of the Collection requirements.
2.  Collection maintainers have not fixed the violations and have not released a fixed version of the collection within the time period established by this document.

#### Process

1.  Any community member who finds a collection that violates one or more of the Collection requirements may file an issue against said collection's repository. If the reporter is unsure whether something constitutes a violation or believes that the apparently violated guideline is unclear, they should consult with the steering committee by filing a community topic before proceeding.
2.  The issue filed against the collection's repository should include the following information:

> - References to the corresponding Collection requirements the collection violates.
> - Actions collection maintainers need to do to make the collection comply with the requirements.

1.  A default term for the collection to solve the issue is four weeks since the issue was created. It can vary depending on a requirement violated, SC opinions or other circumstances.
2.  If the violation is not fixed or there is a disagreement between the reporter and the maintainers, the reporter or another person creates a community topic.
3.  Two SC members check the reported circumstances and confirm in the topic that the violation is present from their point of view, and is one that must be fixed.
4.  The Community and SC vote on considering the collection violating the requirements and removing it from the package. The vote must be open for at least one week.
5.  If SC votes that the collection does NOT violate the requirements, the process is stopped. The issue needs to be updated accordingly.
6.  If X.0.0 will be released next, set Y=X+1. If X.0.0 has already been released, but (X+1).0.0 has not yet been released, set Y=X+2.
7.  Announce upcoming removal from Ansible Y in the original issue in the collection's repository.
8.  [Announce upcoming removal from Ansible Y]().
9.  [Remove collection from Ansible Y]().

### Canceling removal

#### Conditions

1.  Ansible Y has not yet been released.
2.  All the requirements violations have been fixed.

#### Process

1.  SC votes on whether the result is acceptable.
2.  A negative vote must come with a good explanation why the actions done by collection maintainers have not been sufficient.
3.  If SC does not vote against the removal of the collection (this includes the case that the vote did not reach quorum), the removal will continue.
4.  If SC votes to cancel the removal, [re-add collection to Ansible Y]().

### Re-adding collection to Ansible

There is no simplified process. Once the collection has been removed from Ansible Y.0.0, it needs to go through the full inclusion process to be re-added to the Ansible package. Exceptions are only possible if SC votes on them. SC can approve or deny a fast re-entry without going through the full review process.
