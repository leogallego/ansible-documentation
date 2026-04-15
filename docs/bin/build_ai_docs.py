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

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
RST_DIR = ROOT / "docs" / "docsite" / "rst"
OUTPUT_DIR = ROOT / "docs" / "docsite" / "ai-docs"
CORE_CONFIG = ROOT / "docs" / "ai-docs-core.yml"

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


def resolve_includes(text: str, rst_file: pathlib.Path) -> str:
    """Resolve ``.. include::`` directives by inlining referenced content.

    *rst_file* is the path to the RST file that contains the includes —
    relative paths inside ``.. include::`` are resolved against its parent
    directory.  Missing files are silently removed (replaced with nothing).

    Resolution is non-recursive: includes inside included content are not
    expanded.
    """

    def _replace(match: re.Match[str]) -> str:
        rel_path = match.group(1).strip()
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


def main() -> None:
    """Entry point — implemented in later tasks."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
