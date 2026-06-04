# Reporting bugs and requesting features

## Reporting a bug

### Security bugs

Ansible practices responsible disclosure. To report security-related bugs, send an email to <security@ansible.com> for an immediate response. Do not submit a ticket or post to any public groups.

### Bugs in ansible-core

Before reporting a bug, search in GitHub for [already reported issues](https://github.com/ansible/ansible/issues) and [open pull requests](https://github.com/ansible/ansible/pulls) to see if someone has already addressed your issue. Unsure if you found a bug? Discuss the behavior with the community on the Ansible Forum.

Also, use the Ansible Forum to discuss whether the problem is in `ansible-core` or a collection, and for "how do I do this" type questions.

You need a free GitHub account to [report bugs](https://github.com/ansible/ansible/issues) that affect:

- multiple plugins
- a plugin that remained in the ansible/ansible repo
- the overall functioning of Ansible

### How to write a good bug report

If you find a bug, open an issue using the [issue template](https://github.com/ansible/ansible/issues/new?assignees=&labels=&template=bug_report.yml).

Fill out the issue template as completely and as accurately as possible. Include:

- your Ansible version
- the expected behavior and what you've tried, including the exact commands you were using or tasks you are running.
- the current behavior and why you think it is a bug
- the steps to reproduce the bug
- a minimal reproducible example and comments describing examples
- any relevant configurations and the components you used
- any relevant output plus `ansible -vvvv` (debugging) output
- add the output of `ansible-test-env --show` when filing bug reports involving `ansible-test`.

When sharing YAML in playbooks, ensure that you preserve formatting using [code blocks](https://help.github.com/articles/creating-and-highlighting-code-blocks/). For multiple-file content, use gist.github.com, more durable than Pastebin content.

## Requesting a feature

Before you request a feature, check what is planned for future Ansible Releases. Check [existing pull requests tagged with feature](https://github.com/ansible/ansible/issues?q=is%3Aissue+is%3Aopen+label%3Afeature).

To get your feature into Ansible, submit a pull request, either against ansible-core or a collection. See also ansible_collection_merge_requirements. For `ansible-core`, you can also open an issue in [ansible/ansible](https://github.com/ansible/ansible/issues) or in a corresponding collection repository (To find the correct issue tracker, refer to Bugs in collections ).
