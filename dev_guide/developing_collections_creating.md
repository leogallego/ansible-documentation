# Creating collections

To create a collection:

1.  Create a new collection, optionally using a custom collection template, with the `ansible-galaxy collection init` command.
2.  Add modules and other content to the collection.
3.  Build the collection into a collection artifact with ansible-galaxy collection build.
4.  Publish the collection artifact to Galaxy with ansible-galaxy collection publish.

A user can then install your collection on their systems.

## Naming your collection

Collection names consist of a namespace and a name, separated by a period (`.`). Both namespace and name should be valid Python identifiers. This means that they should consist of ASCII letters, digits, and underscores.

Usually namespaces and names use lower-case letters, digits, and underscores, but no upper-case letters.

You should make sure that the namespace you use is not registered by someone else by checking on [Ansible Galaxy's namespace list](https://galaxy.ansible.com/ui/namespaces/). If you chose a namespace or even a full collection name that collides with another collection on Galaxy, it can happen that if you or someone else runs `ansible-galaxy collection install` with your collection name, you end up with another collection. Even if the namespace currently does not exist, it could be created later by someone else.

If you want to request a new namespace on Ansible Galaxy, [create an issue on github.com/ansible/galaxy](https://github.com/ansible/galaxy/issues/new?assignees=thedoubl3j%2C+alisonlhart%2C+chynasan%2C+traytorous&labels=area%2Fnamespace&projects=&template=New_namespace.md&title=namespace%3A+FIXME).

There are a few special namespaces:

ansible  

> The [ansible namespace](https://galaxy.ansible.com/ui/namespaces/ansible/) is owned by Red Hat and reserved for official Ansible collections. Two special members are the synthetic `ansible.builtin` and `ansible.legacy` collections. These cannot be found on Ansible Galaxy, but are built-in into ansible-core.

community  

> The [community namespace](https://galaxy.ansible.com/ui/namespaces/community/) is owned by the Ansible community. Collections from this namespace generally live in the [GitHub ansible-collection organization](https://github.com/ansible-collections/). If you want to create a collection in this namespace, request it on the forum.

local  

> The [local namespace](https://galaxy.ansible.com/ui/namespaces/local/) does not contain any collection on Ansible Galaxy, and the intention is that this will never change. You can use the `local` namespace for collections that are locally on your machine or locally in your Git repositories, without having to fear collisions with actually existing collections on Ansible Galaxy.

## Creating a new collection

Create your collection skeleton in a path that includes `ansible_collections`, for example <span class="title-ref">collections/ansible_collections/</span>.

To start a new collection, run the following command in your collections directory:

``` bash
ansible_collections#> ansible-galaxy collection init my_namespace.my_collection
```

Both the namespace and collection names use the same strict set of requirements. Both are limited to alphanumeric characters and underscores, must have a minimum length of three characters, and cannot start with an underscore.

It will create the structure `[my_namespace]/[my_collection]/[collection skeleton]`.

If Git is used for version control, the corresponding repository should be initialized in the collection directory.

Once the collection exists, you can populate the directories with the content you want inside the collection. See [ansible-collections](https://github.com/ansible-collections/) GitHub Org to get a better idea of what you can place inside a collection.

Reference: the `ansible-galaxy collection` command

Currently the `ansible-galaxy collection` command implements the following sub commands:

- `init`: Create a basic collection based on the default template included with Ansible or your own template.
- `build`: Create a collection artifact that can be uploaded to Galaxy or your own repository.
- `publish`: Publish a built collection artifact to Galaxy.
- `install`: Install one or more collections.

To learn more about the `ansible-galaxy` command-line tool, see the ansible-galaxy man page.

## Creating a collection from a custom template

The built-in collection template is a simple example of a collection that works with `ansible-core`, but if you want to simplify your development process you may want to create a custom collection template to pass to `ansible-galaxy collection init`.

A collection skeleton is a directory that looks like a collection directory but any `.j2` files (excluding those in `templates/` and `roles/*/templates/`) will be templated by `ansible-galaxy collection init`. The skeleton's `galaxy.yml.j2` file should use the variables `namespace` and `collection_name` which are derived from `ansible-galaxy init namespace.collection_name`, and will populate the metadata in the initialized collection's `galaxy.yml` file. There are a few additional variables available by default (for example, `version` is `1.0.0`), and these can be supplemented/overridden using `--extra-vars`.

An example `galaxy.yml.j2` file that accepts an optional dictionary variable `dependencies` could look like this:

``` jinja
namespace: {{ namespace }}
name: {{ collection_name }}
version: {{ (version|quote) is version('0.0.0', operator='gt', version_type='semver')|ternary(version, undef('version must be a valid semantic version greater than 0.0.0')) }}
dependencies: {{ dependencies | default({}, true) }}
```

To initialize a collection using the new template, pass the path to the skeleton with `ansible-galaxy collection init`:

``` bash
ansible_collections#> ansible-galaxy collection init --collection-skeleton /path/to/my/namespace/skeleton --extra-vars "@my_vars_file.json" my_namespace.my_collection
```

Before `ansible-core` 2.17, collection skeleton templating is limited to the few hardcoded variables including `namespace`, `collection_name`, and `version`.

The default collection skeleton uses an internal filter `comment_ify` that isn't accessibly to `--collection-skeleton`. Use `ansible-doc -t filter|test --list` to see available plugins.

## Creating collections with ansible-creator

[ansible-creator](https://ansible.readthedocs.io/projects/creator/) is designed to quickly scaffold an Ansible collection project.

The [Ansible Development Tools](https://ansible.readthedocs.io/projects/dev-tools/) package offers a convenient way to install `ansible-creator` along with a curated set of tools for developing automation content.

After [installing](https://ansible.readthedocs.io/projects/creator/installing) `ansible-creator` you can initialize a project in one of the following ways:

- Use the `init` subcommand.
- Use `ansible-creator` with the [Ansible extension](https://ansible.readthedocs.io/projects/creator/collection_creation/#step-1-installing-ansible-creator-in-the-environment) in Visual Studio Code.
