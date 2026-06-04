# Should you develop a module?

Developing Ansible modules is easy, but often it is not necessary. Before you start writing a new module, ask:

1.  Does a similar module already exist?

An existing module may cover the functionality you want. Ansible collections include thousands of modules. Search our list of included collections or [Ansible Galaxy](https://galaxy.ansible.com) to see if an existing module does what you need.

2.  Should you use or develop an action plugin instead of a module?

An action plugin may be the best way to get the functionality you want. Action plugins run on the control node instead of on the managed node, and their functionality is available to all modules. For more information about developing plugins, read the developing plugins page.

3.  Should you use a role instead of a module?

A combination of existing modules may cover the functionality you want. You can write a role for this type of use case. Check out the roles documentation.

4.  Should you create a collection instead of a single module?

The functionality you want may be too large for a single module. If you want to connect Ansible to a new cloud provider, database, or network platform, you may need to develop a new collection.

- Each module should have a concise and well defined functionality. Basically, follow the UNIX philosophy of doing one thing well.
- A module should not require that a user know all the underlying options of an API/tool to be used. For example, if the legal values for a required module parameter cannot be documented, that's a sign that the module would be rejected.
- Modules should typically encompass much of the logic for interacting with a resource. A lightweight wrapper around an API that does not contain much logic would likely cause users to offload too much logic into a playbook, and for this reason the module would be rejected. Instead try creating multiple modules for interacting with smaller individual pieces of the API.

If your use case isn't covered by an existing module, an action plugin, or a role, and you don't need to create multiple modules, then you're ready to start developing a new module. Choose from the topics below for next steps:

- I want to get started on a new module.
- I want to review tips and conventions for developing good modules.
- I want to write a Windows module.
- I want an overview of Ansible's architecture.
- I want to document my module.
- I want to contribute my module to an existing Ansible collection.
- I want to add unit and integration tests to my module.
- I want to add Python 3 support to my module.
- I want to write multiple modules.
