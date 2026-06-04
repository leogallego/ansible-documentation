# Ansible Collection Maintenance and Workflow

Each collection community can set its own rules and workflows for managing pull requests (PRs), bug reports, documentation issues, feature requests, as well as for adding and replacing maintainers.

Collection maintainers have `write` or higher access to a collection, allowing them to merge pull requests and perform other administrative tasks.

## Managing pull requests

Maintainers review and merge PRs according to the following guidelines:

- code_of_conduct
- maintainer_requirements
- Committer guidelines
- PR review checklist

## Releasing a collection

Collection maintainers are responsible for releasing new collection versions. The general release process includes:

1.  **Planning and announcement**: Define the release scope and communicate it.
2.  **Changelog generation**: Create a comprehensive list of changes.
3.  **Git tagging**: Create and push a release Git tag.
4.  **Automated publication**: The release tarball is automatically published on [Ansible Galaxy](https://galaxy.ansible.com/) via the [Zuul dashboard](https://dashboard.zuul.ansible.com/t/ansible/builds?pipeline=release) or a custom GitHub Actions workflow.
5.  **Final announcement**: Communicate the successful release.

See releasing_collections for more information.

## Backporting

Collection maintainers backport merged pull requests to stable branches if they exist. This process adheres to the collection's [semantic versioning](https://semver.org/) and release policies.

The manual backporting process mirrors the ansible-core backporting guidelines.

For streamlined backporting, GitHub bots like the [Patchback app](https://github.com/apps/patchback) can automate the process through labeling, as implemented in the [community.general](https://github.com/ansible-collections/community.general) collection.

## Including a collection in Ansible

To include a collection in the Ansible community package, maintainers create a discussion in the [ansible-collections/ansible-inclusion repository](https://github.com/ansible-collections/ansible-inclusion). See the [submission process](https://github.com/ansible-collections/ansible-inclusion/blob/main/README.md) and the Ansible community package collections requirements for details.

# Stepping down as a collection maintainer

If you can no longer continue as a collection maintainer, follow these steps:

1.  **Inform other maintainers**: Notify your co-maintainers.
2.  **Notify the community**: For collections under the `ansible-collections` GitHub organization, inform the relevant communication_irc channels, or email `ansible-community@redhat.com`.
3.  **Identify potential replacements**: Look for active contributors within the collection who could become new maintainers. Discuss these candidates with other maintainers or the [Ansible community team](https://forum.ansible.com/g/CommunityEngTeam).
4.  **Announce the need for maintainers (if no replacement is found)**: If you cannot find a replacement, create a pinned issue in the collection repository announcing the need for new maintainers.
5.  **Post in the Bullhorn newsletter**: Make the same announcement through the [Bullhorn newsletter](https://forum.ansible.com/t/about-the-newsletter-category/166).
6.  **Engage in candidate discussions**: Be available to discuss potential candidates identified by other maintainers or the community team.

Remember, this is a community and you are welcome to rejoin at any time.
