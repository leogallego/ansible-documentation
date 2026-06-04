# Creating a new collection

Starting with Ansible 2.10, related modules should be developed in a collection. The Ansible Core team and community compiled these module development tips and tricks to help companies developing Ansible modules for their products and users developing Ansible modules for third-party products. See developing_collections for a more detailed description of the collections format and additional development guidelines.

**LICENSING REQUIREMENTS** Ansible enforces the following licensing requirements:

- Utilities (files in `lib/ansible/module_utils/`) may have one of two licenses:  
  - A file in `module_utils` used **only** for a specific vendor's hardware, provider, or service may be licensed under GPLv3+. Adding a new file under `module_utils` with GPLv3+ needs to be approved by the core team.
  - All other `module_utils` must be licensed under BSD, so GPL-licensed third-party and Galaxy modules can use them.
  - If there's doubt about the appropriate license for a file in `module_utils`, the Ansible Core Team will decide during an Ansible Core Community Meeting.

- All other files shipped with Ansible, including all modules, must be licensed under the GPL license (GPLv3 or later).

- Existing license requirements still apply to content in ansible/ansible (ansible-core).

- Content that was previously in ansible/ansible or a collection and has moved to a new collection must retain the license it had in its prior repository.

- Copyright entries by previous committers must also be kept in any moved files.

## Before you start coding

This list of prerequisites is designed to help ensure that you develop high-quality modules that work well with ansible-core and provide a seamless user experience.

- Read though all the pages linked off developing_modules_general; paying particular focus to the developing_modules_checklist.
- We encourage PEP 8 compliance. See testing_pep8 for more information.
- We encourage supporting Python 2.6+ and Python 3.5+.
- Look at Ansible Galaxy and review the naming conventions in your functional area (such as cloud, networking, databases).
- With great power comes great responsibility: Ansible collection maintainers have a duty to help keep content up to date and release collections they are responsible for regularly. As with all successful community projects, collection maintainers should keep a watchful eye for reported issues and contributions.
- We strongly recommend unit and/or integration tests. Unit tests are especially valuable when external resources (such as cloud or network devices) are required. For more information see developing_testing.

## Naming conventions

Fully Qualified Collection Names (FQCNs) for plugins and modules include three elements:

> - the Galaxy namespace, which generally represents the company or group
>
> - the collection name, which generally represents the product or OS
>
> - the plugin or module name  
>   - always in lower case
>   - words separated with an underscore (`_`) character
>   - singular, rather than plural, for example, `command` not `commands`

For example, `community.mongodb.mongodb_linux` or `cisco.meraki.meraki_device`.

It is convenient if the organization and repository names on GitHub (or elsewhere) match your namespace and collection names on Ansible Galaxy, but it is not required. The plugin names you select, however, are always the same in your code repository and in your collection artifact on Galaxy.

## Speak to us

Circulating your ideas before coding helps you adopt good practices and avoid common mistakes. After reading the "Before you start coding" section you should have a reasonable idea of the structure of your modules. Write a list of your proposed plugin and/or module names, with a short description of what each one does. Circulate that list on the Ansible Forum so the Ansible community can review your ideas for consistency and familiarity. Names and functionality that are consistent, predictable, and familiar make your collection easier to use.

## Where to get support

Ansible has a thriving and knowledgeable community of module developers that is a great resource for getting your questions answered. Visit the Ansible communication guide for details.

## Required files

Your collection should include the following files to be usable:

- an `__init__.py` file - An empty file to initialize namespace and allow Python to import the files. *Required*
- at least one plugin, for example, `/plugins/modules/$your_first_module.py`. *Required*
- if needed, one or more `/plugins/doc_fragments/$topic.py` files - Code documentation, such as details regarding common arguments. *Optional*
- if needed, one or more `/plugins/module_utils/$topic.py` files - Code shared between more than one module, such as common arguments. *Optional*

When you have these files ready, review the developing_modules_checklist again. If you are creating a new collection, you are responsible for all procedures related to your repository, including setting rules for contributions, finding reviewers, and testing and maintaining the code in your collection.

## New to Git or GitHub

We realize this may be your first use of Git or GitHub. The following guides may be of use:

- [How to create a fork of ansible/ansible](https://help.github.com/articles/fork-a-repo/)
- [How to sync (update) your fork](https://help.github.com/articles/syncing-a-fork/)
- [How to create a Pull Request (PR)](https://help.github.com/articles/about-pull-requests/)
