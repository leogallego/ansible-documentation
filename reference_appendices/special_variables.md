# Special Variables

## Magic variables

These variables cannot be set directly by the user; Ansible will always override them to reflect internal state.

## Facts

These are variables that contain information pertinent to the current host (<span class="title-ref">inventory_hostname</span>). They are only available if gathered first. See vars_and_facts for more information.

## Connection variables

Connection variables are normally used to set the specifics on how to execute actions on a target. Most of them correspond to connection plugins, but not all are specific to them; other plugins like shell, terminal and become are normally involved. Only the common ones are described as each connection/become/shell/etc plugin can define its own overrides and specific variables. See general_precedence_rules for how connection variables interact with configuration settings, command-line options, and playbook keywords.

