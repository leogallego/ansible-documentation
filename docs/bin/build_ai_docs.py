#!/usr/bin/env python
"""
Convert RST documentation to AI-friendly Markdown.

Reads RST files from docs/docsite/rst/, strips Sphinx-specific markup,
converts to GitHub Flavored Markdown via pandoc, and writes output to
docs/docsite/ai-docs/ with a manifest.json.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from datetime import datetime, timezone

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
RST_DIR = ROOT / "docs" / "docsite" / "rst"
OUTPUT_DIR = ROOT / "docs" / "docsite" / "ai-docs"
CORE_CONFIG = ROOT / "docs" / "ai-docs-core.yml"

BASE_URL = (
    "https://raw.githubusercontent.com/leogallego/" "ansible-documentation/ai-docs"
)

# Top-level files to exclude (navigation-only)
EXCLUDE_FILES = {"ansible_index.rst", "core_index.rst"}

# Directories to skip entirely
EXCLUDE_DIRS = {"images", "shared_snippets"}

# Filename patterns to skip
EXCLUDE_NAMES = {"index.rst"}

# Audience classification by topic directory
AUDIENCE_MAP: dict[str, str] = {
    "dev_guide": "developer",
    "playbook_guide": "author",
    "inventory_guide": "author",
    "getting_started": "author",
    "getting_started_ee": "author",
    "vault_guide": "author",
    "tips_tricks": "author",
    "command_guide": "author",
}

# ---------------------------------------------------------------------------
# Directives to strip (Sphinx-only, not useful in Markdown output)
# ---------------------------------------------------------------------------
_STRIP_DIRECTIVES = (
    "toctree",
    "versionadded",
    "versionchanged",
    "deprecated",
    "seealso",
    "contents",
    "meta",
    "raw",
    "only",
)

# Build one compiled regex per directive.
# Pattern matches ``.. name::`` plus all indented continuation lines
# (lines that are indented more than the directive or blank).
_DIRECTIVE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(
        rf"^\.\. {name}::(?:[^\n]*)(?:\n(?:[ \t]+[^\n]*|[ \t]*))*",
        re.MULTILINE,
    )
    for name in _STRIP_DIRECTIVES
]

# Target labels:  .. _some-label:
_TARGET_LABEL_RE = re.compile(r"^\.\. _[^:]+:\s*$", re.MULTILINE)

# Substitution definitions:  .. |name| replace:: ...
_SUBSTITUTION_RE = re.compile(
    r"^\.\. \|[^|]+\|[^\n]*\n(?:[ \t]+[^\n]*\n)*", re.MULTILINE
)

# RST comments — lines starting with ``..`` that are NOT directives,
# targets, or substitutions.  A comment has ``.. `` followed by text
# that does NOT match ``word::`` (directive), ``_`` (target), or ``|`` (subst).
_COMMENT_RE = re.compile(
    r"^\.\. (?![\w-]+::)(?!_)(?!\|)([^\n]*)\n(?:[ \t]+[^\n]*\n)*",
    re.MULTILINE,
)

# Collapse three or more consecutive newlines to exactly two.
_EXCESS_NEWLINES_RE = re.compile(r"\n{3,}")

# Pandoc GFM post-processing patterns
_SPAN_ID_RE = re.compile(r'<span id="[^"]*"></span>')
_DIV_BLOCK_RE = re.compile(r"<div[^>]*>.*?</div>", re.DOTALL)


def strip_directives(text: str) -> str:
    """Remove Sphinx-only directives, targets, substitutions, and comments."""
    for pattern in _DIRECTIVE_PATTERNS:
        text = pattern.sub("", text)

    text = _TARGET_LABEL_RE.sub("", text)
    text = _SUBSTITUTION_RE.sub("", text)
    text = _COMMENT_RE.sub("", text)
    text = _EXCESS_NEWLINES_RE.sub("\n\n", text)

    return text


# ---------------------------------------------------------------------------
# Sphinx role conversion
# ---------------------------------------------------------------------------

# Roles whose content should become plain text (display text if present).
_REF_ROLES = frozenset({"ref", "doc", "term", "guilabel"})

# Roles whose content should be wrapped in double backticks.
_CODE_ROLES = frozenset(
    {
        "mod",
        "func",
        "class",
        "meth",
        "attr",
        "command",
        "file",
        "envvar",
        "option",
        "program",
        "literal",
        "code",
    }
)

# Ansible-specific roles that extract part of the value.
_ANS_PLUGIN_ROLES = frozenset({"ansplugin"})
_ANS_OPT_ROLES = frozenset({"ansopt", "ansretval", "ansoptref"})

# Master pattern matching  :role:`content`
_ROLE_RE = re.compile(r":(\w+):`([^`]+)`")


def _convert_role_match(match: re.Match[str]) -> str:
    """Replace a single Sphinx role match with Markdown-friendly text."""
    role = match.group(1)
    content = match.group(2)

    if role in _REF_ROLES:
        # :ref:`Display Text <target>` → Display Text
        # :ref:`target` → target
        angle = content.find("<")
        if angle != -1 and content.endswith(">"):
            return content[:angle].rstrip()
        return content

    if role in _CODE_ROLES:
        return f"``{content}``"

    if role in _ANS_PLUGIN_ROLES:
        # :ansplugin:`fqcn#type` → ``fqcn``
        value = content.split("#")[0]
        return f"``{value}``"

    if role in _ANS_OPT_ROLES:
        # :ansopt:`fqcn#type:option` → ``option``
        # :ansopt:`option` → ``option``
        colon_pos = content.rfind(":")
        if colon_pos != -1:
            value = content[colon_pos + 1 :]
        else:
            value = content
        return f"``{value}``"

    if role == "abbr":
        # :abbr:`YAML (expansion)` → YAML
        paren = content.find("(")
        if paren != -1:
            return content[:paren].rstrip()
        return content

    # Unknown role — return content as-is.
    return content


def convert_roles(text: str) -> str:
    """Convert Sphinx interpreted text roles to plain text or inline code."""
    return _ROLE_RE.sub(_convert_role_match, text)


# ---------------------------------------------------------------------------
# Include resolution
# ---------------------------------------------------------------------------

_INCLUDE_RE = re.compile(r"^\.\. include:: (.+)$", re.MULTILINE)


def resolve_includes(
    text: str,
    rst_file: pathlib.Path,
    rst_dir: pathlib.Path | None = None,
) -> str:
    """Resolve ``.. include::`` directives by inlining referenced content.

    *rst_file* is the path to the RST file that contains the includes —
    relative paths inside ``.. include::`` are resolved against its parent
    directory.  Paths starting with ``/`` are resolved relative to *rst_dir*
    (the RST source root), matching Sphinx convention.

    Missing files are silently removed (replaced with nothing).
    Resolution is non-recursive: includes inside included content are not
    expanded.
    """

    def _replace(match: re.Match[str]) -> str:
        rel_path = match.group(1).strip()
        if rel_path.startswith("/") and rst_dir is not None:
            target = (rst_dir / rel_path.lstrip("/")).resolve()
        else:
            target = (rst_file.parent / rel_path).resolve()
        if target.is_file():
            return target.read_text()
        return ""

    return _INCLUDE_RE.sub(_replace, text)


# ---------------------------------------------------------------------------
# RST file discovery
# ---------------------------------------------------------------------------


def discover_rst_files(rst_dir: pathlib.Path) -> list[pathlib.Path]:
    """Return a sorted list of convertible RST files under *rst_dir*.

    Exclusion rules:
    1. Top-level files (directly in *rst_dir*, no subdirectory).
    2. Files inside ``EXCLUDE_DIRS`` directories.
    3. Files whose name appears in ``EXCLUDE_FILES`` or ``EXCLUDE_NAMES``.
    """
    results: list[pathlib.Path] = []
    for rst_file in sorted(rst_dir.rglob("*.rst")):
        rel = rst_file.relative_to(rst_dir)
        # Skip top-level files (no subdirectory)
        if len(rel.parts) == 1:
            continue
        # Skip excluded directories
        if rel.parts[0] in EXCLUDE_DIRS:
            continue
        # Skip excluded file names
        if rst_file.name in EXCLUDE_FILES or rst_file.name in EXCLUDE_NAMES:
            continue
        results.append(rst_file)
    return results


def convert_rst_to_md(rst_text: str) -> str:
    """Convert RST text to GitHub Flavored Markdown using pandoc."""
    try:
        result = subprocess.run(
            ["pandoc", "-f", "rst", "-t", "gfm", "--wrap=none"],
            input=rst_text,
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        print("Error: pandoc is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def postprocess_md(text: str) -> str:
    """Clean up pandoc GFM output: strip HTML artifacts, collapse blank lines."""
    text = _SPAN_ID_RE.sub("", text)
    # Strip div blocks (may be nested — apply repeatedly until stable)
    while _DIV_BLOCK_RE.search(text):
        text = _DIV_BLOCK_RE.sub("", text)
    # Strip any orphan closing tags left after nested div removal
    text = text.replace("</div>", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


# ---------------------------------------------------------------------------
# Metadata extraction
# ---------------------------------------------------------------------------

_TITLE_RE = re.compile(r"^# (.+)$", re.MULTILINE)


def extract_title(md_text: str) -> str:
    """Extract the first H1 heading from markdown text."""
    match = _TITLE_RE.search(md_text)
    if match:
        return match.group(1).strip()
    return "Untitled"


def get_audience(topic: str) -> str:
    """Classify audience from topic directory name."""
    return AUDIENCE_MAP.get(topic, "both")


def extract_summary(md_text: str) -> str:
    """Extract a one-line summary from the first paragraph after the title."""
    parts = md_text.split("\n\n")
    for part in parts:
        text = part.strip()
        if not text or text.startswith("#"):
            continue
        # Take first sentence (up to first period followed by space or end)
        sentence_match = re.match(r"^(.+?\.)\s", text)
        if sentence_match:
            summary = sentence_match.group(1)
        else:
            summary = text
        if len(summary) > 120:
            return summary[:117] + "..."
        return summary
    return ""


def load_core_config(config_path: pathlib.Path) -> set[str]:
    """Load the set of core file paths from the YAML config."""
    if not config_path.is_file():
        return set()
    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return set(data.get("core_files", []))


def generate_manifest(
    output_dir: pathlib.Path,
    core_files: set[str],
) -> dict:
    """Generate manifest.json data from the converted markdown files."""
    files: list[dict] = []
    for md_file in sorted(output_dir.rglob("*.md")):
        rel_path = str(md_file.relative_to(output_dir))
        content = md_file.read_text(encoding="utf-8")
        topic = md_file.relative_to(output_dir).parts[0]
        files.append(
            {
                "path": rel_path,
                "topic": topic,
                "title": extract_title(content),
                "audience": get_audience(topic),
                "lines": content.count("\n") + 1,
                "core": rel_path in core_files,
                "summary": extract_summary(content),
            }
        )
    return {
        "version": "1.0",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "base_url": BASE_URL,
        "files": files,
    }


def preprocess_rst(
    text: str,
    rst_file: pathlib.Path,
    rst_dir: pathlib.Path | None = None,
) -> str:
    """Full pre-processing pipeline: includes -> directives -> roles."""
    text = resolve_includes(text, rst_file, rst_dir)
    text = strip_directives(text)
    text = convert_roles(text)
    return text


def convert_file(
    rst_file: pathlib.Path,
    rst_dir: pathlib.Path,
    output_dir: pathlib.Path,
) -> pathlib.Path | None:
    """Convert a single RST file to Markdown. Returns output path or None."""
    rel = rst_file.relative_to(rst_dir).with_suffix(".md")
    out_path = output_dir / rel

    rst_text = rst_file.read_text(encoding="utf-8")
    preprocessed = preprocess_rst(rst_text, rst_file, rst_dir)
    md_text = convert_rst_to_md(preprocessed)
    md_text = postprocess_md(md_text)

    if not md_text.strip():
        return None

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md_text, encoding="utf-8")
    return out_path


def generate_readme(manifest: dict, output_dir: pathlib.Path) -> None:
    """Write a README.md into the output directory for the ai-docs branch."""
    files = manifest["files"]
    total_lines = sum(f["lines"] for f in files)
    core_files = [f for f in files if f.get("core")]

    # Topic stats sorted by count descending
    topic_counts: dict[str, int] = {}
    for f in files:
        topic_counts[f["topic"]] = topic_counts.get(f["topic"], 0) + 1

    topic_rows = "\n".join(
        f"| `{topic}` | {count} |"
        for topic, count in sorted(
            topic_counts.items(), key=lambda x: x[1], reverse=True
        )
    )

    # Core files grouped by topic
    core_by_topic: dict[str, list[str]] = {}
    for f in core_files:
        stem = pathlib.PurePosixPath(f["path"]).stem
        core_by_topic.setdefault(f["topic"], []).append(stem)
    core_rows = "\n".join(
        f"| {topic} | {', '.join(f'`{s}`' for s in stems)} |"
        for topic, stems in sorted(core_by_topic.items())
    )

    json_example = """\
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
```"""

    readme = f"""\
# Ansible Documentation for AI

This branch contains the official [Ansible](https://docs.ansible.com/) \
documentation converted from RST to Markdown, optimized for consumption by \
AI coding assistants (Claude Code, Copilot, Cursor, etc.).

It is generated automatically by a CI pipeline. Do not edit files on this \
branch directly — they will be overwritten on the next build.

## Quick start

Fetch the manifest to discover available files:

```
https://raw.githubusercontent.com/leogallego/ansible-documentation/ai-docs/manifest.json
```

Then fetch individual files by combining the base URL with any `path` \
from the manifest:

```
https://raw.githubusercontent.com/leogallego/ansible-documentation/ai-docs/{{path}}
```

For example:

```
https://raw.githubusercontent.com/leogallego/ansible-documentation/ai-docs/playbook_guide/playbooks_intro.md
```

## What's here

- **{len(files)} Markdown files** covering playbooks, inventory, modules, \
plugins, collections, developer guides, porting guides, and more
- **{total_lines:,} total lines** of documentation
- **`manifest.json`** at the root — a machine-readable index of every file \
with metadata

## Manifest

`manifest.json` is the entry point for programmatic consumers. It contains \
metadata for every file so tools can decide what to fetch without \
downloading everything.

### Structure

{json_example}

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

{len(core_files)} files are flagged `core: true` in the manifest. These \
cover the most commonly needed topics and are intended for bundling directly \
into AI skills or tools for zero-latency access:

| Topic | Files |
|-------|-------|
{core_rows}

The core set is configured in `docs/ai-docs-core.yml` on the source branch.

## Topics

| Topic | Files |
|-------|------:|
{topic_rows}

## How to use this in AI tools

### CLAUDE.md reference

Add to any project's `CLAUDE.md`:

````markdown
## Ansible Documentation

When answering Ansible questions or reviewing Ansible code, fetch docs from:
- Manifest: https://raw.githubusercontent.com/leogallego/ansible-documentation/ai-docs/manifest.json
- Files: https://raw.githubusercontent.com/leogallego/ansible-documentation/ai-docs/{{path}}
````

### Programmatic access

1. Fetch `manifest.json`
2. Filter files by `topic`, `audience`, or `core` flag
3. Fetch the relevant files by `path`
4. Use `lines` to stay within your context budget

## How this is generated

A CI pipeline on the source branch:

1. Preprocesses RST — strips Sphinx directives (`toctree`, `versionadded`, \
`deprecated`, `seealso`), converts Sphinx roles (`:ref:`, `:doc:`) to plain \
text, resolves `.. include::` directives
2. Converts to GitHub Flavored Markdown via [pandoc](https://pandoc.org/)
3. Post-processes — removes residual HTML artifacts from pandoc output
4. Generates `manifest.json` with extracted metadata
5. Force-pushes the output to this orphan branch

Source: \
[`docs/bin/build_ai_docs.py`]\
(https://github.com/leogallego/ansible-documentation/blob/feat/ai-docs-pipeline/docs/bin/build_ai_docs.py)

## License

This content is derived from the \
[Ansible documentation](https://github.com/ansible/ansible-documentation) \
and is subject to the same license terms as the original project.
"""
    readme_path = output_dir / "README.md"
    readme_path.write_text(readme, encoding="utf-8")
    print(f"README written to {readme_path}.")


def run(
    rst_dir: pathlib.Path = RST_DIR,
    output_dir: pathlib.Path = OUTPUT_DIR,
    core_config: pathlib.Path = CORE_CONFIG,
) -> None:
    """Run the full conversion pipeline."""
    import shutil

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    rst_files = discover_rst_files(rst_dir)
    print(f"Found {len(rst_files)} RST files to convert.")

    converted = 0
    for rst_file in rst_files:
        rel = rst_file.relative_to(rst_dir)
        result = convert_file(rst_file, rst_dir, output_dir)
        if result:
            converted += 1
            print(f"  {rel} -> {result.relative_to(output_dir)}")
        else:
            print(f"  {rel} -> (skipped, empty output)")

    print(f"\nConverted {converted}/{len(rst_files)} files.")

    core_files = load_core_config(core_config)
    manifest = generate_manifest(output_dir, core_files)

    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest written to {manifest_path} ({len(manifest['files'])} entries).")

    generate_readme(manifest, output_dir)


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rst-dir",
        type=pathlib.Path,
        default=RST_DIR,
        help="RST source directory (default: %(default)s)",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=OUTPUT_DIR,
        help="Output directory for Markdown files (default: %(default)s)",
    )
    return parser.parse_args(args)


def main() -> None:
    """CLI entry point."""
    args = parse_args()
    run(rst_dir=args.rst_dir, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
