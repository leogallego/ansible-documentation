# Modules

Modules are the main building blocks of Ansible playbooks. Although we do not generally speak of "module plugins", a module is a type of plugin. For a developer-focused description of the differences between modules and other plugins, see modules_vs_plugins.

## Enabling modules

You can enable a custom module by dropping it into one of these locations:

- any directory added to the `ANSIBLE_LIBRARY` environment variable (`$ANSIBLE_LIBRARY` takes a colon-separated list like `$PATH`)
- `~/.ansible/plugins/modules/`
- `/usr/share/ansible/plugins/modules/`

For more information on using local custom modules, see local_modules.

## Using modules

For information on using modules in ad hoc tasks, see intro_adhoc. For information on using modules in playbooks, see playbooks_intro.
