# Generating changelogs and porting guide entries in a collection

You can create and share changelog and porting guide entries for your collection. If your collection is part of the Ansible Community package, we recommend that you use the [antsibull-changelog](https://github.com/ansible-community/antsibull-changelog) tool to generate Ansible-compatible changelogs. The Ansible changelog uses the output of this tool to collate all the collections included in an Ansible release into one combined changelog for the release.

Ansible here refers to the Ansible 2.10 or later release that includes a curated set of collections.

## Understanding antsibull-changelog

The `antsibull-changelog` tool allows you to create and update changelogs for Ansible collections that are compatible with the combined Ansible changelogs. This is an update to the changelog generator used in prior Ansible releases. The tool adds three new changelog fragment categories: `breaking_changes`, `security_fixes` and `trivial`. The tool also generates the `changelog.yaml` file that Ansible uses to create the combined `CHANGELOG.rst` file and Porting Guide for the release.

See changelogs_how_to and the [antsibull-changelog documentation](https://github.com/ansible-community/antsibull-changelog/tree/main/docs) for complete details.

The collection maintainers set the changelog policy for their collections. See the individual collection contributing guidelines for complete details.

### Generating changelogs

To initialize changelog generation:

1.  Install `antsibull-changelog`: `pip install antsibull-changelog`.
2.  Initialize changelogs for your repository: `antsibull-changelog init <path/to/your/collection>`.
3.  Optionally, edit the `changelogs/config.yaml` file to customize the location of the generated changelog `.rst` file or other options. See [Bootstrapping changelogs for collections](https://ansible.readthedocs.io/projects/antsibull-changelog/changelogs/) for details.

To generate changelogs from the changelog fragments you created:

1.  Optionally, validate your changelog fragments: `antsibull-changelog lint`.
2.  Generate the changelog for your release: `antsibull-changelog release [--version version_number]`.

Add the `--reload-plugins` option if you ran the `antsibull-changelog release` command previously and the version of the collection has not changed. `antsibull-changelog` caches the information on all plugins and does not update its cache until the collection version changes.

### Porting Guide entries from changelog fragments

The Ansible changelog generator automatically adds several changelog fragment categories to the Ansible Porting Guide:

- `major_changes`
- `breaking_changes`
- `deprecated_features`
- `removed_features`

## Including collection changelogs into Ansible

If your collection is part of Ansible, use one of the following three options to include your changelog into the Ansible release changelog:

- Use the `antsibull-changelog` tool.
- If are not using this tool, include the properly formatted `changelog.yaml` file into your collection. See the [changelog.yaml format](https://github.com/ansible-community/antsibull-changelog/blob/main/docs/changelog.yaml-format.md) for details.
- Add a link to own changelogs or release notes in any format by opening an issue at <https://github.com/ansible-community/ansible-build-data/> with the HTML link to that information.

For the first two options, Ansible pulls the changelog details from Galaxy so your changelogs must be included in the collection version on Galaxy that is included in the upcoming Ansible release.

