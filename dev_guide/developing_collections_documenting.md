# Documenting collections

## Documenting modules and plugins

Documenting modules is thoroughly documented in module_documenting. Plugins can be documented the same way as modules, that is with `DOCUMENTATION`, `EXAMPLES`, and `RETURN` blocks.

## Documenting roles

To document a role, you have to add a role argument spec by creating a file `meta/argument_specs.yml` in your role. See role_argument_spec for details. As an example, you can look at [the argument specs file](https://github.com/telekom-mms/ansible-collection-icinga-director/blob/main/roles/ansible_icinga/meta/argument_specs.yml) of the `telekom_mms.icinga_director.ansible_icinga role <telekom_mms.icinga_director.ansible_icinga` on GitHub.

## Verifying your collection documentation

You can use `antsibull-docs` to lint your collection documentation. See [Linting collection documentation](https://ansible.readthedocs.io/projects/antsibull-docs/collection-docs/#linting-collection-docs). for details.

## Build a docsite with antsibull-docs

You can use [antsibull-docs](https://pypi.org/project/antsibull-docs) to build a Sphinx-based docsite for your collection:

1.  Create your collection and make sure you can use it with ansible-core by adding it to your COLLECTIONS_PATHS.
2.  Create a directory `dest` and run `antsibull-docs sphinx-init --use-current --dest-dir dest namespace.name`, where `namespace.name` is the name of your collection.
3.  Go into `dest` and run `pip install -r requirements.txt`. You might want to create a venv and activate it first to avoid installing this globally.
4.  Then run `./build.sh`.
5.  Open `build/html/index.html` in a browser of your choice.

See [antsibull-docs documentation](https://ansible.readthedocs.io/projects/antsibull-docs/) for complete details.

If you want to add additional documentation to your collection next to the plugin, module, and role documentation, see collections_doc_dir.
