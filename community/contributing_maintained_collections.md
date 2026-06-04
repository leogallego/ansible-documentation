# Contributing to Ansible-maintained Collections

The Ansible team welcomes community contributions to the collections maintained by Red Hat Ansible Engineering. This section describes how you can open issues and create PRs with the required testing before your PR can be merged.

## Ansible-maintained collections

The following table shows:

- **Ansible-maintained collection** - Click the link to the collection on Galaxy, then click the `repo` button in Galaxy to find the GitHub repository for this collection.
- **Related community collection** - Collection that holds community-created content (modules, roles, and so on) that may also be of interest to a user of the Ansible-maintained collection. You can, for example, add new modules to the community collection as a technical preview before the content is moved to the Ansible-maintained collection.
- **Sponsor** - Working group that manages the collections. You can join the meetings to discuss important proposed changes and enhancements to the collections.
- **Test requirements** - Testing required for any new or changed content for the Ansible-maintained collection.
- **Developer details** - Describes whether the Ansible-maintained collection accepts direct community issues and PRs for existing collection content, as well as more specific developer guidelines based on the collection type.

\* A ✓ under **Open to PRs** means the collection welcomes GitHub issues and PRs for any changes to existing collection content (plugins, roles, and so on).

\*\* Integration tests are required and unit tests are welcomed but not required for the AWS collections. An exception to this is made in cases where integration tests are logistically not feasible due to external requirements. An example of this is AWS Direct Connect, as this service can not be functionally tested without the establishment of network peering connections. Unit tests are therefore required for modules that interact with AWS Direct Connect. Exceptions to `amazon.aws` must be approved by Red Hat, and exceptions to `community.aws` must be approved by the AWS community.

\*\*\* `ansible.netcommon` contains all foundational components for enabling many network and security platform collections. It contains all connection and filter plugins required, and installs as a dependency when you install the platform collection.

\*\*\*\* Unit tests for Windows PowerShell modules are an exception to testing, but unit tests are valid and required for the remainder of the collection, including Ansible-side plugins.

## Deciding where your contribution belongs

We welcome contributions to Ansible-maintained collections. Because these collections are part of a downstream-supported Red Hat product, the criteria for contribution, testing, and release may be higher than other community collections. The related community collections (such as `community.general` and `community.network`) have less stringent requirements and are a great place for new functionality that may become part of the Ansible-maintained collection in a future release.

The following scenarios use the `arista.eos` to help explain when to contribute to the Ansible-maintained collection, and when to propose your change or idea to the related community collection:

1.  You want to fix a problem in the `arista.eos` Ansible-maintained collection. Create the PR directly in the [arista.eos collection GitHub repository](https://github.com/ansible-collections/arista.eos). Apply all the merge requirements.

2.  You want to add a new Ansible module for Arista. Your options are one of the following:

    > - Propose a new module in the `arista.eos` collection (requires approval from Arista and Red Hat).
    > - Propose a new collection in the `arista` namespace (requires approval from Arista and Red Hat).
    > - Propose a new module in the `community.network` collection (requires network community approval).
    > - Place your new module in a collection in your own namespace (no approvals required).

Most new content should go into either a related community collection or your own collection first so that is well established in the community before you can propose adding it to the `arista` namespace, where inclusion and maintenance criteria are much higher.

## Requirements to merge your PR

Your PR must meet the following requirements before it can merge into an Ansible-maintained collection:

1.  The PR is in the intended scope of the collection. Communicate with the appropriate Ansible sponsor listed in the Ansible-maintained collection table for help.
2.  For network and security domains, the PR follows the resource module development principles.
3.  Passes sanity tests and tox.
4.  Passes unit, and integration tests, as listed in the Ansible-maintained collection table and described in testing_resource_modules.
5.  Follows Ansible guidelines. See developing_modules and developing_collections.
6.  Addresses all review comments.
7.  Includes an appropriate changelog.
