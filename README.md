# Ansible Documentation for AI

This branch contains the official [Ansible](https://docs.ansible.com/) documentation converted from RST to Markdown, optimized for consumption by AI coding assistants (Claude Code, Copilot, Cursor, etc.).

It is generated automatically by a CI pipeline. Do not edit files on this branch directly — they will be overwritten on the next build.

## Quick start

Fetch the manifest to discover available files:

```
https://raw.githubusercontent.com/leogallego/ansible-documentation/ai-docs/manifest.json
```

Then fetch individual files by combining the base URL with any `path` from the manifest:

```
https://raw.githubusercontent.com/leogallego/ansible-documentation/ai-docs/{path}
```

For example:

```
https://raw.githubusercontent.com/leogallego/ansible-documentation/ai-docs/playbook_guide/playbooks_intro.md
```

## What's here

- **454 Markdown files** covering playbooks, inventory, modules, plugins, collections, developer guides, porting guides, and more
- **57,897 total lines** of documentation
- **`manifest.json`** at the root — a machine-readable index of every file with metadata

## Manifest

`manifest.json` is the entry point for programmatic consumers. It contains metadata for every file so tools can decide what to fetch without downloading everything.

### Structure

```json
{
  "version": "1.0",
  "generated": "2026-04-15T04:38:04Z",
  "files": [
    {
      "path": "playbook_guide/playbooks_intro.md",
      "topic": "playbook_guide",
      "title": "Ansible playbooks",
      "audience": "author",
      "lines": 123,
      "core": true,
      "summary": "Playbooks are automation blueprints..."
    }
  ]
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `path` | string | File path relative to the branch root |
| `topic` | string | Topic area (parent directory) |
| `title` | string | Document title extracted from the first heading |
| `audience` | enum | `author`, `developer`, or `both` |
| `lines` | integer | Line count — useful for context budget decisions |
| `core` | boolean | Whether this file is in the curated essential set |
| `summary` | string | One-line description for relevance scoring |

## Core files

18 files are flagged `core: true` in the manifest. These cover the most commonly needed topics and are intended for bundling directly into AI skills or tools for zero-latency access:

| Topic | Files |
|-------|-------|
| collections_guide | `collections_installing` |
| dev_guide | `developing_modules_general`, `developing_plugins`, `testing` |
| inventory_guide | `connection_details`, `intro_inventory` |
| playbook_guide | `playbooks_conditionals`, `playbooks_error_handling`, `playbooks_handlers`, `playbooks_intro`, `playbooks_loops`, `playbooks_reuse_roles`, `playbooks_variables`, `playbooks_vars_facts` |
| porting_guides | `porting_guide_core_2.20`, `porting_guide_core_2.21` |
| reference_appendices | `YAMLSyntax`, `general_precedence` |

The core set is configured in `docs/ai-docs-core.yml` on the source branch.

## Topics

| Topic | Files |
|-------|------:|
| `dev_guide` | 112 |
| `user_guide` | 55 |
| `network` | 44 |
| `community` | 42 |
| `playbook_guide` | 38 |
| `porting_guides` | 35 |
| `roadmap` | 33 |
| `plugins` | 20 |
| `reference_appendices` | 14 |
| `os_guide` | 13 |
| `scenario_guides` | 8 |
| `collections_guide` | 6 |
| `getting_started` | 5 |
| `getting_started_ee` | 5 |
| `inventory_guide` | 4 |
| `module_plugin_guide` | 4 |
| `vault_guide` | 4 |
| `command_guide` | 3 |
| `installation_guide` | 3 |
| `galaxy` | 2 |
| `tips_tricks` | 2 |
| `collections` | 1 |
| `inventory` | 1 |

## How to use this in AI tools

### CLAUDE.md reference

Add to any project's `CLAUDE.md`:

````markdown
## Ansible Documentation

When answering Ansible questions or reviewing Ansible code, fetch docs from:
- Manifest: https://raw.githubusercontent.com/leogallego/ansible-documentation/ai-docs/manifest.json
- Files: https://raw.githubusercontent.com/leogallego/ansible-documentation/ai-docs/{path}
````

### Programmatic access

1. Fetch `manifest.json`
2. Filter files by `topic`, `audience`, or `core` flag
3. Fetch the relevant files by `path`
4. Use `lines` to stay within your context budget

## How this is generated

A CI pipeline on the source branch:

1. Preprocesses RST — strips Sphinx directives (`toctree`, `versionadded`, `deprecated`, `seealso`), converts Sphinx roles (`:ref:`, `:doc:`) to plain text, resolves `.. include::` directives
2. Converts to GitHub Flavored Markdown via [pandoc](https://pandoc.org/)
3. Post-processes — removes residual HTML artifacts from pandoc output
4. Generates `manifest.json` with extracted metadata
5. Force-pushes the output to this orphan branch

Source: [`docs/bin/build_ai_docs.py`](https://github.com/leogallego/ansible-documentation/blob/feat/ai-docs-pipeline/docs/bin/build_ai_docs.py)

## License

This content is derived from the [Ansible documentation](https://github.com/ansible/ansible-documentation) and is subject to the same license terms as the original project.
