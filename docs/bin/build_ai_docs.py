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
    "https://raw.githubusercontent.com/leogallego/"
    "ansible-documentation/ai-docs/docs/docsite/ai-docs"
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
    text = _DIV_BLOCK_RE.sub("", text)
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


def preprocess_rst(text: str, rst_file: pathlib.Path) -> str:
    """Full pre-processing pipeline: includes -> directives -> roles."""
    text = resolve_includes(text, rst_file)
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
    preprocessed = preprocess_rst(rst_text, rst_file)
    md_text = convert_rst_to_md(preprocessed)
    md_text = postprocess_md(md_text)

    if not md_text.strip():
        return None

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md_text, encoding="utf-8")
    return out_path


def run() -> None:
    """Run the full conversion pipeline."""
    import shutil

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    rst_files = discover_rst_files(RST_DIR)
    print(f"Found {len(rst_files)} RST files to convert.")

    converted = 0
    for rst_file in rst_files:
        rel = rst_file.relative_to(RST_DIR)
        result = convert_file(rst_file, RST_DIR, OUTPUT_DIR)
        if result:
            converted += 1
            print(f"  {rel} -> {result.relative_to(OUTPUT_DIR)}")
        else:
            print(f"  {rel} -> (skipped, empty output)")

    print(f"\nConverted {converted}/{len(rst_files)} files.")

    core_files = load_core_config(CORE_CONFIG)
    manifest = generate_manifest(OUTPUT_DIR, core_files)

    manifest_path = OUTPUT_DIR / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest written to {manifest_path} ({len(manifest['files'])} entries).")


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
    parse_args()
    run()


if __name__ == "__main__":
    main()
